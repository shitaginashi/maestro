import os
import numpy as np
import librosa
import yaml
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class ConductorRC3Mirror:
    def __init__(self, root="/mnt/forge/audio/"):
        self.root = root
        # THE BOUNDARY: Only these sub-paths are allowed
        self.safe_zones = ["/mega/", "/fx/"] 
        self.library = []
        self.vectors = []
        self.stats = {"A (Risers)": 0, "B (Hits)": 0, "C (Suckbacks)": 0, "Flippable": 0}

    def is_path_safe(self, path):
        # Convert path to lower to avoid case-sensitivity issues on Nemo
        return any(zone in path.lower() for zone in self.safe_zones)

    def get_metrics(self, path):
        try:
            y, sr = librosa.load(path, sr=16000, mono=True)
            if len(y) < 2048: return None, False

            # --- DUAL-CHECK MOMENTUM (X) ---
            rms_head = np.sqrt(np.mean(y[:int(sr*0.4)]**2)) + 1e-6
            rms_tail = np.sqrt(np.mean(y[-int(sr*0.4):]**2)) + 1e-6
            amp_growth = np.clip((rms_tail / rms_head) / 8.0, 0, 1)
            
            cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            cent_growth = np.clip((cent[-1] / (cent[0] + 1e-6)) / 2.0, 0, 1)
            x = float(max(amp_growth, cent_growth))

            # --- IMPACT (Y) & GRAVITY (Z) ---
            peak = np.max(np.abs(y[:int(sr*0.2)]))
            y_axis = float(np.clip((peak/(np.sqrt(np.mean(y**2))+1e-6)) / 12.0, 0, 1))
            z = float(np.clip(np.mean(cent) / 6000, 0, 1))

            # --- INVERSION SUITABILITY ---
            initial_spike = np.max(np.abs(y[:int(sr*0.1)]))
            avg_abs = np.mean(np.abs(y)) + 1e-6
            is_flippable = bool(initial_spike < (avg_abs * 4))

            return [x, y_axis, z], is_flippable
        except Exception:
            return None, False

    def run(self):
        print(f"[*] Commencing Secure RC3 Mirror Regen...")
        print(f"[*] Target Zones: {self.safe_zones}")
        
        for r, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".wav"):
                    path = os.path.join(r, f)
                    
                    # Security Check
                    if not self.is_path_safe(path):
                        continue

                    m, flip = self.get_metrics(path)
                    if m is None: continue

                    if m[0] > 0.5: self.stats["A (Risers)"] += 1
                    if m[1] > 0.4: self.stats["B (Hits)"] += 1
                    if m[2] < 0.3: 
                        self.stats["C (Suckbacks)"] += 1
                        if flip: self.stats["Flippable"] += 1

                    self.library.append({
                        "fp": "".join([f"{int(v*255):02X}" for v in m]),
                        "path": path,
                        "class": "asset" if "/mega/" in path else "foley",
                        "flippable": flip
                    })
                    self.vectors.append(m)

        # File Export
        np.save("latent_library.npy", np.array(self.vectors))
        with open("legend.yml", "w") as f:
            yaml.dump(self.library, f)
        
        print("\n--- SECURE RC3 LANDSCAPE ---")
        total = len(self.library)
        print(f"Total Validated Assets: {total}")
        print(f"Native Risers (A): {self.stats['A (Risers)']}")
        print(f"Potential Risers (A + Flip C): {self.stats['A (Risers)'] + self.stats['Flippable']}")
        print(f"Safe for VSE Inversion: {self.stats['Flippable']}")
        print(f"Hits (B): {self.stats['B (Hits)']}")
        print("\n--- [SUCCESS] Clean RC3 Manifest Exported ---")

if __name__ == "__main__":
    ConductorRC3Mirror().run()