import yaml
from pathlib import Path
import importlib

class Maestro:
    def __init__(self, manifest_path="manifest.yml"):
        self.manifest_path = Path(manifest_path)
        self.data = self._load()
        self.mode = self.data['project']['mode']       # 'a' or 'v'
        self.mark = self.data['project']['iteration']  # 'mark2', etc.

    def _load(self):
        with open(self.manifest_path, 'r') as f:
            return yaml.safe_load(f)

    def execute(self):
        print(f"--- MAESTRO SIGNAL: {self.mode}/{self.mark} ---")
        
        # Dynamic import based on your tree: maestro.a.mark2
        try:
            module_path = f"{self.mode}.{self.mark}"
            mode_logic = importlib.import_module(module_path)
            
            # Execute the mode's primary interrogation
            mode_logic.run(self.data)
        except ImportError as e:
            print(f"Critical: Mode protocol '{self.mode}/{self.mark}' not found. {e}")

if __name__ == "__main__":
    maestro = Maestro()
    maestro.execute()