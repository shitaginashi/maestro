import os
import yaml
import numpy as np

class MaestroCore:
    def __init__(self):
        # Authority Pathing
        self.forge_path = "/mnt/forge/audio/mega"
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.spine_path = os.path.join(self.cwd, "spine.yml")
        self.library_path = os.path.join(self.cwd, "latent_library.npy")

    def load_spine(self):
        if not os.path.exists(self.spine_path):
            return {"tracks": []}
        with open(self.spine_path, 'r') as f:
            return yaml.safe_load(f)

    def get_asset_path(self, filename):
        # Direct pathing to the Forge to avoid symlink shadowing
        return os.path.join(self.forge_path, filename)