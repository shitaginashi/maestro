import librosa
import numpy as np
import yaml
import hashlib
from pathlib import Path

def get_bedrock_id(filename):
    """Generates a consistent 2-char Base-36 ID for the file."""
    hasher = hashlib.md5(filename.encode()).hexdigest()
    return hasher[:2].upper()

def analyze_audio(filepath):
    """Derives the 4D metrics: Pressure(X), Utility(Y), State(Z), and Time(T)."""
    y, sr = librosa.load(filepath)
    
    # --- T-AXIS (Temporal) ---
    duration = min(librosa.get_duration(y=y, sr=sr), 60.0)
    rms = librosa.feature.rms(y=y)[0]
    hit_anchor = round(librosa.frames_to_time(np.argmax(rms), sr=sr), 1)
    
    # --- X-AXIS (Pressure: Slope) ---
    x_slope = np.polyfit(np.arange(len(rms)), rms, 1)[0]
    vx = "+" if x_slope > 0.001 else ("-" if x_slope < -0.001 else "0")
    
    # --- Y-AXIS (Utility: Frequency Centroid) ---
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    vy = "+" if centroid > 2000 else ("-" if centroid < 500 else "0")
    
    # --- Z-AXIS (State: Texture/ZCR) ---
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    vz = "-" if zcr > 0.1 else ("+" if zcr < 0.03 else "0")
    
    # --- INTENSITY (f) ---
    vf = chr(97 + int(min(np.max(rms), 1.0) * 25)) # a-z
    
    bid = get_bedrock_id(Path(filepath).name)
    fingerprint = f"{bid}{vx}{vy}{vz}{vf}"
    
    return {
        "id": fingerprint,
        "t_d": round(duration, 1),
        "t_h": hit_anchor,
        "path": str(filepath)
    }

def run_census(source_dir, output_file="latent_inventory.yml"):
    print(f"--- STARTING CENSUS ON: {source_dir} ---")
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"ERROR: Path {source_dir} does not exist!")
        return

    files = list(source_path.glob("*.wav"))
    print(f"Found {len(files)} files.") # If this is 0, your glob is the problem.

    inventory = {}
    for audio_file in files:
        print(f"Processing: {audio_file.name}...")
        metrics = analyze_audio(audio_file)
        # ... rest of logic
    
    print(f"--- CENSUS COMPLETE: {len(inventory)} items indexed ---")

    if __name__ == "__main__":
    # Ensure the path matches your forge exactly
    run_census("/mnt/forge/audio/mega/")