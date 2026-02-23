import numpy as np
import sys

def hardwired_dna_sequence(kick_idx, bowl_idx):
    print("--- [TRACE] HARDWIRED DNA SEQUENCE ---")
    try:
        lib = np.load('latent_library.npy')
        
        # Extract DNA
        kick_dna = lib[kick_idx]
        bowl_dna = lib[bowl_idx]
        
        # Calculate the "Transient-to-Sustain" Delta
        delta = kick_dna - bowl_dna
        
        # The 'Kick-ness' (Transient) and 'Bowl-ness' (Sustain)
        transient_dims = np.argsort(delta)[-5:]
        sustain_dims = np.argsort(delta)[:5]
        
        print(f"[OK] KICK UNIQUE DIMS: {transient_dims}")
        print(f"[OK] BOWL UNIQUE DIMS: {sustain_dims}")
        
        return transient_dims, sustain_dims
    except Exception as e:
        print(f"[SF] ERROR: {e}")

# Example usage with known indices from your previous trace
# hardwired_dna_sequence(2013, 1341)