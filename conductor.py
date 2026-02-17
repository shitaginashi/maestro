import librosa
import numpy as np
import yaml
import sys
import argparse
import os

class Conductor:
    def __init__(self, spine_path="spine.yml"):
        self.spine_path = spine_path

    def analyze_lane(self, y, sr, t):
        start = int(t * sr)
        end = start + int(0.05 * sr)
        if end > len(y): return "B"
        
        spec = np.abs(librosa.stft(y[start:end]))
        centroid = librosa.feature.spectral_centroid(S=spec, sr=sr).mean()
        
        # --- RE-BALANCED GATES ---
        if centroid > 4000: return "A"  # Only the sharpest banjo/piano highs
        if centroid > 1500: return "B"  # Mids/Guitar/Vocals
        return "C"                      # Bass/Sub (Everything below 1.5kHz)

    def get_integrity(self, y, sr, t):
        # Peak volume at the hit point
        start = max(0, int((t - 0.05) * sr))
        end = min(len(y), int((t + 0.05) * sr))
        window = y[start:end]
        return float(np.max(np.abs(window))) if len(window) > 0 else 0.5

    def generate_spine(self, soundtrack_path):
        print(f"MAESTRO: Loading {soundtrack_path}...")
        y, sr = librosa.load(soundtrack_path, sr=48000)
        
        # Detect onsets
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        hits = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')
        
        print(f"MAESTRO: Found {len(hits)} raw candidates.")
        
        beats = []
        for t in hits:
            lane = self.analyze_lane(y, sr, t)
            integrity = self.get_integrity(y, sr, t)
            
            # Debugging to terminal so we can see the banjo hits
            print(f"  [HIT] {t:.2f}s | Lane: {lane} | Vol: {integrity:.2f}")
            
            beats.append({
                't_delta': float(t),
                'lane': lane,
                'integrity': integrity, # Flattened for RC2
                'freq': 0.5 # Placeholder
            })
            
        with open(self.spine_path, 'w') as f:
            yaml.dump({'beats': beats}, f)
        
        print(f"MAESTRO: Success. {len(beats)} beats written to {self.spine_path}")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    
    c = Conductor()
    c.generate_spine(args.input)