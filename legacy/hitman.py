import os
import librosa

root = "/mnt/forge/audio/"
threshold = 2048
purge_list = []

print(f"[*] Hunting for stowaways with length < {threshold} samples...")

for r, d, files in os.walk(root):
    for f in files:
        if f.endswith(".wav"):
            path = os.path.join(r, f)
            try:
                # Load with duration=0.5 just to check the header length
                y, sr = librosa.load(path, sr=None, duration=0.2)
                if len(y) < threshold:
                    print(f"[FOUND] {path} | Length: {len(y)}")
                    purge_list.append(path)
            except:
                print(f"[CORRUPT] {path}")
                purge_list.append(path)

print(f"\n[*] Total stowaways found: {len(purge_list)}")
# To actually delete them, uncomment the line below:
# for p in purge_list: os.remove(p)