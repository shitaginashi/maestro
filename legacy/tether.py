import yaml
import random

# Load the newly minted legend
with open("legend.yml", "r") as f:
    legend = yaml.safe_load(f)

# Category sorting
native_risers = [a for a in legend if int(a['fp'][:2], 16) > 200]
flippable_suckbacks = [a for a in legend if a.get('flippable') and int(a['fp'][:2], 16) < 50]

print("--- RC3 SPOT-CHECK: NATIVE RISERS (Lane A) ---")
for a in random.sample(native_risers, 3):
    print(f"ID: {a['fp']} | Path: {a['path']}")

print("\n--- RC3 SPOT-CHECK: FLIPPABLE SUCKBACKS (Lane C -> A) ---")
for a in random.sample(flippable_suckbacks, 3):
    print(f"ID: {a['fp']} | Path: {a['path']}")