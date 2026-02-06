import numpy as np
import os
import yaml
import bpy

class Sampler:
    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        self.library_path = os.path.join(assets_dir, "latent_library.npy")
        self.yml_path = os.path.join(assets_dir, "spine.yml")
        # No more vault_path needed for mapping; the ID is absolute.
        self.library = np.load(self.library_path, allow_pickle=True)
        
def execute_braid_abc(self, context):
        scene = context.scene
        sed = scene.sequence_editor_create()
        fps = scene.render.fps

        # --- 1. THE SCORE (THE FOUNDATION) ---
        with open(self.yml_path, 'r') as f:
            spine_data = yaml.safe_load(f)
            # Use get() with fallbacks to avoid KeyErrors
            duration_sec = spine_data.get('duration', 0)
            score_path = spine_data.get('score_path', "")

        # Kill existing Score instances
        for s in [s for s in sed.sequences if s.name.startswith("Main_Score")]:
            sed.sequences.remove(s)
        
        if os.path.exists(score_path):
            # Place the Score on Channel 1
            score_strip = sed.sequences.new_sound("Main_Score", score_path, channel=1, frame_start=1)
            print(f"Maestro: Score materialized from {score_path}")
        else:
            print(f"Maestro WARNING: Score path not found at {score_path}")

        # --- 2. THE TIMELINE CEILING ---
        if duration_sec > 0:
            scene.frame_start = 1
            scene.frame_end = int(duration_sec * fps)
            print(f"Maestro: Timeline calibrated to {scene.frame_end} frames.")

        # --- 3. CHANNEL PURGE ---
        # Only proceed to populate if the environment is set
        for s in [s for s in sed.sequences if s.channel >= 3]:
            sed.sequences.remove(s)

        # --- 4. POPULATION ---
        occ = {3: 0, 4: 0, 5: 0}
        placed_count = 0
        
        for entry in self.library:
            full_path = entry['id']
            if not os.path.exists(full_path): continue
            
            # Use index 3 as the time delta
            t_sec = entry['vector'][3] 
            start_frame = max(1, int(t_sec * fps))
            
            # Find open channel
            target_ch = -1
            for ch in [3, 4, 5]:
                if start_frame >= occ[ch]:
                    target_ch = ch
                    break
            
            if target_ch != -1:
                filename = os.path.basename(full_path)
                strip = sed.sequences.new_sound(filename, full_path, target_ch, start_frame)
                strip["latent_vec"] = entry['vector']
                occ[target_ch] = start_frame + strip.frame_final_duration
                placed_count += 1

        print(f"Maestro: Environment ready. Placed {placed_count} braid assets.")

def cycle_strip(self, strip):
        """The Cycle Button Brain: Finds the N-best matches based on Flex Mode"""
        if "latent_vec" not in strip:
            return False

        # 1. Determine Search Vector
        base_vec = np.array(strip["latent_vec"])
        
        # 2. Flex Mode: Apply Sassy Jitter if enabled
        if bpy.context.scene.maestro_flex_mode:
            # Shift the search target by 10% of the variance
            base_vec += np.random.normal(0, 0.1, size=base_vec.shape)

        # 3. Calculate Distances
        all_vecs = np.array([e['vector'] for e in self.library])
        distances = np.linalg.norm(all_vecs - base_vec, axis=1)
        
        # 4. Get Next Best (using a rank counter on the strip)
        if "maestro_rank" not in strip:
            strip["maestro_rank"] = 0
        
        strip["maestro_rank"] = (strip["maestro_rank"] + 1) % 20 # Top 20 pool
        ranks = np.argsort(distances)
        new_idx = ranks[strip["maestro_rank"]]
        
        # 5. Execute Swap
        new_entry = self.library[new_idx]
        v_map = self.get_vault_map()
        new_path = v_map.get(new_entry['id'])
        
        if new_path and os.path.exists(new_path):
            strip.sound.filepath = new_path
            strip.name = new_entry['id']
            return True
        return False
