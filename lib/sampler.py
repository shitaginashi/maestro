import yaml
from pathlib import Path

class Sampler:
    def __init__(self, matrix_path="latent_inventory.yml"):
        with open(matrix_path, 'r') as f:
            self.matrix = yaml.safe_load(f)
            
    def query(self, target_vector, target_duration):
        """
        Finds the closest assets based on Vector ID and T-Delta.
        target_vector: The trinary suffix, e.g., '+0-'
        target_duration: The ideal length in seconds.
        """
        # 1. Filter by Fingerprint Suffix (X, Y, Z)
        # We ignore the 2-char Bedrock ID (prefix) and the intensity (suffix) 
        # unless you want to match intensity strictly.
        candidates = []
        for name, data in self.matrix.items():
            # Extracting trinary states from the 5-char ID (pos 2, 3, 4)
            asset_xyz = data['id'][2:5]
            if asset_xyz == target_vector:
                candidates.append(data)

        # 2. Rank by Temporal Proximity |Target_T - Asset_T|
        candidates.sort(key=lambda x: abs(x['t_d'] - target_duration))

        # 3. Return Top 6 (Winner + 5 Runners Up)
        return candidates[:6]

# --- QUICK TEST ---
if __name__ == "__main__":
    trent = Sampler()
    # Looking for a "Phrase" length Riser/Loop/Dry
    results = trent.query("+0-", 4.0)
    
    for i, res in enumerate(results):
        print(f"{'WINNER' if i==0 else 'RUNNER'}: {res['id']} | {res['t_d']}s | {Path(res['path']).name}")