import bpy
import yaml
import os
import subprocess
import numpy as np

class MaestroEngineV3:
    def __init__(self):
        self.version = "3.2-STABLE"
        print(f"--- [ACTUAL SOURCE] ENGINE {self.version} START ---")
        
        # 1. FORCED PATH CALIBRATION (Based on your realpath output)
        self.root = "/mnt/forge/forge/maestro"
        self.soundtrack_wav = os.path.join(self.root, "soundtrack.wav")
        self.spine_path = os.path.join(self.root, "spine.yml") # FIXED EXTENSION
        
        self.lane_map = {"A": 7, "B": 8, "C": 9}
        
        print(f"MAESTRO: Targeted Spine -> {self.spine_path}")

    def materialize_with_statistical_rarity(self):
        print("!!! RUNNING RARITY ENGINE: THE GHOST IS GONE !!!")
        
        scene = bpy.context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()

        # 1. GROUND TRUTH (The Soundtrack Floor)
        if os.path.exists(self.soundtrack_wav):
            # Clear Channel 1 to prevent "stacking" soundtracks on re-runs
            for s in list(scene.sequence_editor.sequences):
                if s.channel == 1: 
                    scene.sequence_editor.sequences.remove(s)
            
            # Place the WAV
            snd = scene.sequence_editor.sequences.new_sound(
                name="SOUNDTRACK", 
                filepath=self.soundtrack_wav, 
                channel=1, 
                frame_start=1
            )
            
            # CALIBRATION: Set the project length to the song length
            max_f = int(snd.frame_duration)
            scene.frame_start = 1
            scene.frame_end = max_f
            
            print(f"MAESTRO: Soundtrack synced. Endframe: {max_f}")
        else:
            print(f"MAESTRO ERROR: Soundtrack not found at {self.soundtrack_wav}")
            return False

        # 2. DATA INGESTION
        with open(self.spine_path, 'r') as f:
            data = yaml.safe_load(f)
            all_beats = data.get('beats', [])
        
        print(f"MAESTRO: Ingested {len(all_beats)} beats from Spine.")
        
        # 3. STATISTICAL RARITY & CULLING
        counts = {"A": 0, "B": 0, "C": 0}
        for b in all_beats:
            l = b.get('lane', 'A')
            if l in counts: counts[l] += 1
        
        total_beats = len(all_beats)
        # Weight = how rare the lane is. 
        # Using math.sqrt here to nudge us closer to 14 hits instead of 7.
        import math
        rarity_weights = {l: math.sqrt(total_beats / max(count, 1)) for l, count in counts.items()}
        
        candidates = []
        for b in all_beats:
            l = b.get('lane', 'A')
            t_start = int(b.get('t_delta', 0) * 24) # Assuming 24fps
            integrity = b.get('integrity', 0)
            
            # Rank = Integrity * Scarcity
            rank = integrity * rarity_weights.get(l, 1.0)
            candidates.append({'frame': t_start, 'lane': l, 'rank': rank})

        # Sort by Rank (Highest priority first)
        candidates.sort(key=lambda x: x['rank'], reverse=True)
        
        final_spine = [] # <--- THIS DEFINES THE MISSING VARIABLE
        occupied_ranges = [] 

        for c in candidates:
            c_start = c['frame']
            c_end = c_start + 400 # 16.6 second safety window
            
            # Conflict resolution: Check if this spot is taken by a higher-rank beat
            is_blocked = False
            for (o_start, o_end) in occupied_ranges:
                if not (c_end < o_start or c_start > o_end):
                    is_blocked = True
                    break
            
            if not is_blocked:
                final_spine.append(c)
                occupied_ranges.append((c_start, c_end))
        
        # 4. MATERIALIZATION (Drawing the 7 Pillars)
        # Clear existing V31 strips first to avoid overlapping ghost data
        for s in list(scene.sequence_editor.sequences):
            if s.name.startswith("V31_"):
                scene.sequence_editor.sequences.remove(s)

        for i, c in enumerate(final_spine):
            l = c['lane']
            f_start = c['frame']
            
            # The API Call: Creating a Color Strip as a placeholder
            # We use Channel + 1 (A=7+1=8, etc.) to avoid the Soundtrack on Ch 1
            chan = self.lane_map.get(l, 2)
            
            strip = scene.sequence_editor.sequences.new_effect(
                name=f"V31_{l}_{i}", # CRITICAL: Exact prefix for exporter
                type='COLOR',
                channel=chan,
                frame_start=f_start,
                frame_end=f_start + 400
            )
            
            # Visual feedback: Lane A is Red, B is Green, C is Blue
            if l == "A": strip.color = (1, 0, 0)
            elif l == "B": strip.color = (0, 1, 0)
            else: strip.color = (0, 0, 1)

        # FORCE BLENDER TO ACKNOWLEDGE THE STRIPS
        bpy.context.view_layer.update()
        
        print(f"MAESTRO: Materialization complete. {len(final_spine)} hits placed.")
        return True

    def ingest_soundtrack(self):
        """Converts ANY .mp3 in the directory to the working wav."""
        import glob
        mp3_files = glob.glob(os.path.join(self.cwd, "*.mp3"))
        if not mp3_files:
            print("MAESTRO: No MP3 found.")
            return False
            
        source_mp3 = mp3_files[0]
        cmd = ['ffmpeg', '-y', '-i', source_mp3, '-ar', '48000', '-ac', '2', self.soundtrack_wav]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"MAESTRO: Ingested {os.path.basename(source_mp3)}")
            return True
        except Exception as e:
            print(f"MAESTRO: FFmpeg error: {e}")
            return False

    def export_to_edl(self):
        scene = bpy.context.scene
        if not scene.sequence_editor:
            print("MAESTRO: No Sequence Editor found to export.")
            return

        # DEFINING THE STRIPS: Filter the VSE for our V31 strips
        strips = [s for s in scene.sequence_editor.sequences_all if s.name.startswith("V31_")]
        if not strips:
            print("MAESTRO: No 'V31_' strips found in timeline. Export aborted.")
            return

        for lane in ["A", "B", "C"]:
            edl_path = os.path.join(self.root, f"maestro_{lane}.edl")
            
            # Filter strips belonging to this specific lane (V31_A, etc.)
            lane_strips = [s for s in strips if s.name.startswith(f"V31_{lane}")]
            lane_strips.sort(key=lambda x: x.frame_start)

            with open(edl_path, 'w') as f:
                f.write(f"TITLE: MAESTRO_V3_LANE_{lane}\n\n")
                for i, clip in enumerate(lane_strips):
                    # Standard EDL Format: Event Number | V (Video) | C (Cut) | Start | End
                    f.write(f"{str(i+1).zfill(3)}  V     C        {clip.frame_start} {clip.frame_final_end}\n")
            
        print(f"MAESTRO: EDLs materialized in {self.root}")