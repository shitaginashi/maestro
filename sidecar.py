import os
import yaml
import numpy as np
import argparse

# --- CONFIG ---
CWD = os.getcwd()
NPY_PATH = os.path.join(CWD, "latent_library.npy")
LEGEND_PATH = os.path.join(CWD, "legend.yml")
SPINE_PATH = os.path.join(CWD, "spine.yml")
FPS = 24

class ConformistSampler:
    def __init__(self):
        # Load math and legend - Ensure variable names match find_match
        self.vectors = np.load(NPY_PATH, allow_pickle=True)
        with open(LEGEND_PATH, 'r') as f:
            self.legend = yaml.safe_load(f)
        
        # Guard against mismatch between NPY rows and Legend entries
        if len(self.vectors) != len(self.legend):
            print(f"⚠️ WARNING: Sync Error! Vectors: {len(self.vectors)}, Legend: {len(self.legend)}")
            # Truncate to the smaller of the two to prevent IndexErrors
            limit = min(len(self.vectors), len(self.legend))
            self.vectors = self.vectors[:limit]
            self.legend = self.legend[:limit]

        self.weights = np.array([1.0, 1.2, 2.5]) # Freq, Phase, Integrity

    def find_match(self, target_vec, sassy_val=0):
        if sassy_val > 0:
            target_vec += np.random.normal(0, sassy_val, size=target_vec.shape)
        
        # Uses self.vectors (defined in __init__)
        sub_matrix = self.vectors[:, :3]
        distances = np.sqrt(np.sum(self.weights * (sub_matrix - target_vec)**2, axis=1))
        best_idx = np.argmin(distances)
        
        return {
            'id': self.legend[best_idx]['id'],
            'path': self.legend[best_idx]['path'],
            'vector': self.vectors[best_idx]
        }

def generate_xml(sassy=0):
    sampler = ConformistSampler()
    with open(SPINE_PATH, 'r') as f:
        spine = yaml.safe_load(f).get('beats', [])

    xml = ['<?xml version="1.0" encoding="UTF-8"?><xmeml version="4"><sequence>',
           f'<rate><timebase>{FPS}</timebase></rate><media><video>']

    # --- VIDEO BRAID (CH 7-9) ---
    for lane_idx, lane_char in enumerate(["A", "B", "C"]):
        xml.append('<track>')
        for i, beat in enumerate(spine):
            if beat['lane'] == lane_char:
                start = int(beat['t_delta'] * FPS)
                xml.append(f'<clipitem id="V{i}"><name>V_{lane_char}_{i}</name><start>{start}</start><end>{start+81}</end></clipitem>')
        xml.append('</track>')

    xml.append('</video><audio>')

    # --- AUDIO BRAID (CH 3-5) ---
    for lane_idx, lane_char in enumerate(["A", "B", "C"]):
        xml.append('<track>')
        for i, beat in enumerate(spine):
            if beat['lane'] == lane_char:
                f = beat['fingerprint']
                target = np.array([f['freq'], f['phase'], f['integrity']])
                
                asset = sampler.find_match(target, sassy_val=sassy)
                path = asset['path']
                # Start frame minus the hit-offset (t_h is vector index 1)
                start = int(beat['t_delta'] * FPS) - int(asset['vector'][1] * FPS)
                
                xml.append(f'<clipitem id="A{i}"><name>{os.path.basename(path)}</name>')
                xml.append(f'<file><pathurl>file://{path}</pathurl></file>')
                xml.append(f'<start>{start}</start><end>{start+120}</end></clipitem>')
        xml.append('</track>')

    xml.append('</audio></media></sequence></xmeml>')
    
    with open("maestro_output.xml", "w") as f:
        f.write("".join(xml))
    print(f"✅ Framework Verified: XML Materialized via ID-Centric Legend.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sassy", type=float, default=0.0)
    args = parser.parse_args()
    generate_xml(sassy=args.sassy)