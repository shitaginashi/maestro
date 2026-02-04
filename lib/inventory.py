import os
import librosa
import numpy as np
import yaml
import hashlib
from pathlib import Path

# FORCING NUMBA CACHE: Prevents the silent hang on Nemo/Shared Environments
os.environ['NUMBA_CACHE_DIR'] = '/tmp'

def get_bedrock_id(filename):
    hasher = hashlib.md5(filename.encode()).hexdigest()
    return hasher[:2].upper()

def analyze_audio(filepath):
    # Use sr=None to avoid resampling overhead during inventory
    y, sr = librosa.load(filepath, sr=None)
    
    # Temporal Axis (T) - Cast to native Python floats for clean YAML
    duration = float(min(librosa.get_duration(y=y, sr=sr), 60.0))
    rms = librosa.feature.rms(y=y)[0]
    hit_anchor = float(round(librosa.frames_to_time(np.argmax(rms), sr=sr), 1))
    
    # Directional Vectors (X, Y, Z)
    x_slope = float(np.polyfit(np.arange(len(rms)), rms, 1)[0])
    vx = "+" if x_slope > 0.001 else ("-" if x_slope < -0.001 else "0")
    
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    vy = "+" if centroid > 2000 else ("-" if centroid < 500 else "0")
    
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    vz = "-" if zcr > 0.1 else ("+" if zcr < 0.03 else "0")
    
    # Intensity (f)
    vf = chr(97 + int(min(np.max(rms), 1.0) * 25))
    
    bid = get_bedrock_id(Path(filepath).name)
    return {
        "id": f"{bid}{vx}{vy}{vz}{vf}",
        "t_d": round(duration, 1),
        "t_h": hit_anchor,
        "path": str(filepath.absolute())
    }

def run_census(source_dir, output_file="latent_inventory.yml"):
    source_path = Path(source_dir).expanduser().resolve()
    print(f"--- INITIATING DEEP SCAN: {source_path} ---")
    
    if not source_path.exists():
        print(f"CRITICAL ERROR: {source_path} not found.")
        return

    # RECURSIVE SEARCH: Looking for .wav and .WAV
    files = [f for f in source_path.rglob("*") if f.suffix.lower() == ".wav"]
    print(f"FOUND {len(files)} ASSETS ACROSS ALL SUBDIRECTORIES.")

    inventory = {}
    for i, audio_file in enumerate(files):
        print(f"[{i+1}/{len(files)}] MAPPING: {audio_file.name}...", end=" ", flush=True)
        try:
            metrics = analyze_audio(audio_file)
            inventory[audio_file.name] = metrics
            print(f"DONE [{metrics['id']}]")
        except Exception as e:
            print(f"SKIP: {e}")

    # FORCE FLAT YAML: Use safe_dump to ensure no Numpy objects survive
    with open(output_file, 'w') as f:
        yaml.safe_dump(inventory, f, sort_keys=True, default_flow_style=False)
    
    print(f"\n--- SUCCESS: {len(inventory)} ASSETS COMMITTED TO {output_file} ---")

if __name__ == "__main__":
    # Ensure this path is 100% accurate for your environment
    run_census("/mnt/forge/audio/mega/")