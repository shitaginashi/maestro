import bpy
import yaml
import os
import subprocess
import numpy as np
import math

class MaestroEngineV3:
    def __init__(self):
        self.version = "3.2-STABLE"
        print(f"--- [ACTUAL SOURCE] ENGINE {self.version} START ---")

        # 1. FORCED PATH CALIBRATION
        self.root = "/mnt/forge/forge/maestro"
        self.soundtrack_wav = os.path.join(self.root, "soundtrack.wav")
        self.spine_path = os.path.join(self.root, "spine.yml") 

        # Lane Mapping for VSE Channels
        self.lane_map = {"A": 7, "B": 8, "C": 9}
        self.audio_channel_map = {"A": 3, "B": 4, "C": 5}

        print(f"MAESTRO: Targeted Spine -> {self.spine_path}")

    def materialize_with_statistical_rarity(self):
        """Processes the Spine and populates the Blender VSE."""
        # 0. INITIALIZE LOCAL SCOPE
        rarity_weights = {}
        counts = {"A": 0, "B": 0, "C": 0}

        scene = bpy.context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()

        # 1. GROUND TRUTH (The Soundtrack Floor)
        if os.path.exists(self.soundtrack_wav):
            for s in list(scene.sequence_editor.sequences):
                if s.channel == 1:
                    scene.sequence_editor.sequences.remove(s)

            snd = scene.sequence_editor.sequences.new_sound(
                name="SOUNDTRACK", filepath=self.soundtrack_wav, channel=1, frame_start=1
            )
            max_f = int(snd.frame_duration)
            scene.frame_start = 1
            scene.frame_end = max_f
            print(f"MAESTRO: Soundtrack synced. Endframe: {max_f}")
        else:
            print(f"MAESTRO ERROR: Soundtrack not found at {self.soundtrack_wav}")
            return False

        # 2. DATA INGESTION
        if not os.path.exists(self.spine_path):
            print(f"MAESTRO ERROR: Spine not found at {self.spine_path}")
            return False

        with open(self.spine_path, "r") as f:
            data = yaml.safe_load(f)
            all_beats = data.get("beats", [])

        total_beats = len(all_beats)
        if total_beats == 0:
            print("MAESTRO: No beats found in spine.")
            return False

        # 3. STATISTICAL CALCULATIONS (Rarity Weighting)
        for b in all_beats:
            l = b.get("lane", "A")
            if l in counts:
                counts[l] += 1

        for l, val in counts.items():
            # Applying the Square Root Dampener: rarity_weight = sqrt(total / count)
            rarity_weights[l] = math.sqrt(total_beats / max(val, 1))

        # 4. RANKING & CULLING
        candidates = []
        for b in all_beats:
            l = b.get("lane", "A")
            integrity = b.get("integrity", 0)
            # T-Delta is in seconds; convert to frames (assuming 24fps)
            t_start = int(b.get("t_delta", 0) * 24)

            weight = rarity_weights.get(l, 1.0)
            rank = integrity * weight
            candidates.append({"frame": t_start, "lane": l, "rank": rank})

        # Sort by rank descending so we prioritize high-integrity/rare beats
        candidates.sort(key=lambda x: x["rank"], reverse=True)

        final_spine = []
        occupied_ranges = []

        for c in candidates:
            c_start = c["frame"]
            c_end = c_start + 400  # 16.6 second safety window

            is_blocked = False
            for o_start, o_end in occupied_ranges:
                if not (c_end < o_start or c_start > o_end):
                    is_blocked = True
                    break

            if not is_blocked:
                final_spine.append(c)
                occupied_ranges.append((c_start, c_end))

        # 5. MATERIALIZATION (Drawing the V31 Strips)
        for s in list(scene.sequence_editor.sequences):
            if s.name.startswith("V31_") or s.name.startswith("SND_"):
                scene.sequence_editor.sequences.remove(s)

        for i, c in enumerate(final_spine):
            l = c["lane"]
            f_start = c["frame"]
            chan = self.lane_map.get(l, 2)

            # Color Strip Placeholder
            strip = scene.sequence_editor.sequences.new_effect(
                name=f"V31_{l}_{i}",
                type="COLOR",
                channel=chan,
                frame_start=f_start,
                frame_end=f_start + 400,
            )

            # --- NEW AUDIO COMPLEMENTS ---
            target_chan = self.audio_channel_map.get(l, 3)
            # Pathing check for assets directory
            asset_path = os.path.join(self.root, "assets", f"hit_{l}.wav")

            if os.path.exists(asset_path):
                scene.sequence_editor.sequences.new_sound(
                    name=f"SND_{l}_{i}",
                    filepath=asset_path,
                    channel=target_chan,
                    frame_start=f_start,
                )

            # Visual Lane Identification
            if l == "A": strip.color = (1, 0, 0) # Red
            elif l == "B": strip.color = (0, 1, 0) # Green
            else: strip.color = (0, 0, 1) # Blue

        bpy.context.view_layer.update()
        print(f"MAESTRO: Materialization complete. {len(final_spine)} hits placed.")
        return True

    def ingest_soundtrack(self):
        """Converts ANY .mp3 in the directory to the working wav."""
        import glob
        # We use root here to stay consistent
        mp3_files = glob.glob(os.path.join(self.root, "*.mp3"))
        if not mp3_files:
            print("MAESTRO: No MP3 found.")
            return False

        source_mp3 = mp3_files[0]
        cmd = ["ffmpeg", "-y", "-i", source_mp3, "-ar", "48000", "-ac", "2", self.soundtrack_wav]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"MAESTRO: Ingested {os.path.basename(source_mp3)}")
            return True
        except Exception as e:
            print(f"MAESTRO: FFmpeg error: {e}")
            return False

    def export_to_edl(self):
        scene = bpy.context.scene
        if not scene.sequence_editor: return

        strips = [s for s in scene.sequence_editor.sequences_all if s.name.startswith("V31_")]
        if not strips: return

        for lane in ["A", "B", "C"]:
            edl_path = os.path.join(self.root, f"maestro_{lane}.edl")
            lane_strips = [s for s in strips if s.name.startswith(f"V31_{lane}")]
            lane_strips.sort(key=lambda x: x.frame_start)

            with open(edl_path, "w") as f:
                f.write(f"TITLE: MAESTRO_V3_LANE_{lane}\n\n")
                for i, clip in enumerate(lane_strips):
                    f.write(f"{str(i+1).zfill(3)}  V     C        {clip.frame_start} {clip.frame_final_end}\n")

        print(f"MAESTRO: EDLs materialized in {self.root}")