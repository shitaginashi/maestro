import numpy as np
import yaml
import sys

def lock_hit_anchors_loud():
    try:
        print("[*] Loading Library...")
        lib = np.load('latent_library.npy')
        with open('legend.yml', 'r') as f:
            legend = yaml.safe_load(f)
        
        print(f"[*] Search space: {len(legend)} assets.")

        # Hardened search: checking if 'path' exists and contains 'Kick'
        kick_indices = []
        for i, entry in enumerate(legend):
            path = entry.get('path', '')
            if "One-Shots/Kick" in path:
                kick_indices.append(i)
        
        if not kick_indices:
            print("[!] FAIL: No Kicks found with string 'One-Shots/Kick'.")
            return

        print(f"[OK] Found {len(kick_indices)} kicks. Extracting DNA...")
        kick_matrix = lib[kick_indices]
        mean_kick_vec = np.mean(kick_matrix, axis=0)
        
        # Get top 5 dimensions
        impact_dims = np.argsort(mean_kick_vec)[-5:]
        print(f"[RESULT] Impact Anchors (Indices): {impact_dims}")
        print(f"[RESULT] Values: {mean_kick_vec[impact_dims]}")
        
        return impact_dims, mean_kick_vec

    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

lock_hit_anchors_loud()