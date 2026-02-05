import librosa
import librosa.display
import numpy as np
import yaml
import matplotlib.pyplot as plt
from pathlib import Path

def get_soundtrack_path(root):
    """Finds the first wav file in the root directory to use as the spine."""
    for f in os.listdir(root):
        if f.endswith(".wav") and not f.startswith("."):
            return os.path.join(root, f)
    return None

class Conductor:
    def __init__(self, root_dir):
        self.root = root_dir
        self.source = get_soundtrack_path(root_dir)
        # HARDCODE: Predictable naming for the Sampler
        self.output_yml = os.path.join(root_dir, "spine.yml")

    def analyze(self):
        if not self.source:
            print("Error: No WAV found in root to act as Spine.")
            return

        print(f"Conductor: Analyzing Spine -> {os.path.basename(self.source)}")
        y, sr = librosa.load(self.source, sr=44100)
        
        # ... (Analysis logic from before) ...
        
        inventory = {
            "metadata": {"source": self.source, "sr": sr},
            "beats": [] # Populated with T-deltas and Headroom
        }
        
        with open(self.output_yml, 'w') as f:
            yaml.dump(inventory, f)

def run(manifest):
    filename = manifest['interrogation']['input_file']
    input_path = Path.cwd() / filename
    
    if not input_path.exists():
        print(f"Critical Error: Signal '{filename}' not found.")
        return

    print(f"--- Trent (Mark 2) Interrogating + Visualizing: {filename} ---")
    
    # Load signal
    y, sr = librosa.load(str(input_path))
    
    # 1. FFT Analysis
    stft = np.abs(librosa.stft(y))
    db_spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    frequencies = librosa.fft_frequencies(sr=sr)
    
    # 2. Trajectory Detection
    targets = manifest['trent_settings']['target_pings']
    findings = []
    
    # QoL: Prepare the Plot
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(db_spectrogram, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    
    for freq in targets:
        idx = (np.abs(frequencies - freq)).argmin()
        magnitude = stft[idx]
        peaks = np.where(magnitude > manifest['trent_settings']['threshold'])[0]
        times = librosa.frames_to_time(peaks, sr=sr)
        
        # Draw target lines on the plot
        plt.axhline(freq, color='white', linestyle='--', alpha=0.5)
        
        findings.append({
            'frequency': int(freq),
            'detections': [round(float(t), 3) for t in times]
        })

    # 3. Save Visual Shard
    plt.title(f"Maestro Interrogation: {filename}")
    visual_path = Path.cwd() / "signal_visual.png"
    plt.savefig(visual_path)
    plt.close()

    # 4. Save YAML Artifact
    report = {
        'source': filename,
        'trajectory_pings': findings
    }
    
    output_path = Path.cwd() / manifest['interrogation']['output_file']
    with open(output_path, 'w') as f:
        yaml.dump(report, f)
        
    print(f"Visual shard saved: {visual_path.name}")
    print(f"Data artifact saved: {output_path.name}")
