import numpy as np
import yaml
import os

def probe_local_library():
    print("--- [PROBE] ANALYZING LOCAL ARTIFACTS ---")
    try:
        # 1. Check Matrix
        if os.path.exists('latent_library.npy'):
            lib = np.load('latent_library.npy')
            print(f"[MATRIX] Found: {lib.shape}")
            print(f"[MATRIX] Stats: Mean={np.mean(lib):.4f}, Max={np.max(lib):.4f}, Min={np.min(lib):.4f}")
            # Check for zero-vectors (failed encodings)
            zeros = np.sum(~lib.any(axis=1))
            print(f"[MATRIX] Dead vectors: {zeros}")
        else:
            print("[FAIL] latent_library.npy NOT FOUND in CWD.")

        # 2. Check Legend
        if os.path.exists('legend.yml'):
            with open('legend.yml', 'r') as f:
                legend = yaml.safe_load(f)
            print(f"[LEGEND] Found {len(legend)} entries.")
            if len(legend) > 0:
                sample = legend[0]
                print(f"[LEGEND] Keys present: {list(sample.keys())}")
                fp = sample.get('fingerprint', 'NONE')
                print(f"[LEGEND] Fingerprint Sample: {fp} (Length: {len(str(fp))})")
                
                # Path Check
                p = sample.get('path', '')
                print(f"[LEGEND] Path Root: {p.split('/')[1] if '/' in p else 'N/A'}")
        else:
            print("[FAIL] legend.yml NOT FOUND in CWD.")

    except Exception as e:
        print(f"[SF] PROBE FAILED: {e}")

probe_local_library()