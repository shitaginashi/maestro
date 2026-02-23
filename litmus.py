import numpy as np
import yaml

def loud_calibrated_strike():
    print("--- [TRACE] CALIBRATED STRIKE: NOISY VERSION ---")
    try:
        lib = np.load('latent_library.npy')
        with open('legend.yml', 'r') as f:
            legend = yaml.safe_load(f)

        # Our discovered "Impact Anchors"
        # We'll use the top 3: 19, 120, 56
        target_128 = np.zeros(128)
        target_128[19] = 0.7
        target_128[120] = 0.6
        target_128[56] = 0.6
        
        active_indices = [19, 120, 56]
        print(f"[*] Comparing against indices: {active_indices}")

        # Slice the library to only the active dimensions to avoid broadcast errors
        lib_slice = lib[:, active_indices]
        target_slice = target_128[active_indices]
        
        # Calculate Euclidean distance
        # Subtraction -> Square -> Sum -> Root
        diff = lib_slice - target_slice
        dist = np.sqrt(np.sum(diff**2, axis=1))
        
        suitability = 1 / (1 + dist)
        top_indices = np.argsort(suitability)[::-1][:5]

        print(f"\nRANK | SCORE  | ASSET")
        print("-" * 50)
        for i, idx in enumerate(top_indices):
            path = legend[idx].get('path', 'UNKNOWN')
            print(f"{i+1}    | {suitability[idx]:.4f} | {path.split('/')[-1]}")

    except Exception as e:
        print(f"[FATAL] Strike failed: {e}")
        import traceback
        traceback.print_exc()

loud_calibrated_strike()