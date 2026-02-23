import os
import cv2
import numpy as np
import imagehash
from PIL import Image
import subprocess
import json
import shutil
import sys
import argparse

def log(msg):
    print(f"[*] {msg}")
    sys.stdout.flush()

def get_stats(path):
    try:
        cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,bit_rate,nb_frames -of json "{path}"'
        result = subprocess.check_output(cmd, shell=True)
        data = json.loads(result)
        s = data['streams'][0]
        w, h = int(s.get('width', 0)), int(s.get('height', 0))
        br = int(s.get('bit_rate', 0)) or (os.path.getsize(path) // 8)
        frames = int(s.get('nb_frames', 0))
        return w, h, br, frames
    except: return 0, 0, 0, 0

def get_fingerprints(path, total_frames):
    pid = os.getpid()
    temp_start = f"start_{pid}.jpg"
    temp_mid = f"mid_{pid}.jpg"
    
    try:
        # Start Frame
        subprocess.run(f'ffmpeg -y -i "{path}" -frames:v 1 "{temp_start}" -loglevel quiet', shell=True)
        # 1-Second Mark (Divergence Check)
        subprocess.run(f'ffmpeg -y -i "{path}" -ss 00:00:01 -frames:v 1 "{temp_mid}" -loglevel quiet', shell=True)
        
        s_hash = int(str(imagehash.phash(Image.open(temp_start))), 16)
        m_hash = int(str(imagehash.phash(Image.open(temp_mid))), 16) if os.path.exists(temp_mid) else s_hash
        
        img = cv2.imread(temp_start)
        lap = cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        
        for t in [temp_start, temp_mid]:
            if os.path.exists(t): os.remove(t)
        return s_hash, m_hash, lap
    except:
        return 0, 0, 0

def main():
    parser = argparse.ArgumentParser(description="vcull-gator: Fidelity-First Video Culler")
    parser.add_argument("path", nargs="?", default=".", help="Path to video directory")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.path)
    cull_dir = os.path.join(target_dir, "cull")
    matrix_path = os.path.join(cull_dir, "fingerprints.npy")
    manifest_path = os.path.join(cull_dir, "cull_manifest.json")

    if not os.path.exists(cull_dir): os.makedirs(cull_dir)
    log(f"Targeting: {target_dir}")

    db = np.load(matrix_path, allow_pickle=True).item() if os.path.exists(matrix_path) else {}
    manifest = []
    
    videos = [f for f in os.listdir(target_dir) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]
    
    for f in videos:
        orig_path = os.path.join(target_dir, f)
        w, h, br, frames = get_stats(orig_path)
        if w == 0: continue
        
        s_hash, m_hash, lap = get_fingerprints(orig_path, frames)
        uid = hex(s_hash)[2:10].zfill(8)
        iters = round(frames / 81)
        cs = (w * h * br) * lap

        collision_uid = None
        if uid in db:
            m_dist = bin(db[uid]['m_hash'] ^ m_hash).count('1')
            if m_dist <= 3: collision_uid = uid
            else: uid = f"{uid}_alt"

        if not collision_uid or uid not in db:
            p_name = f"{uid}P-{iters}.mp4"
            if f != p_name: os.rename(orig_path, os.path.join(target_dir, p_name))
            db[uid] = {"filename": p_name, "iters": iters, "cs": cs, "res_w": w, "m_hash": m_hash, "variants": 0}
            manifest.append({"action": "INITIAL", "file": p_name})
        else:
            existing = db[uid]
            upgrade = False
            if w > existing['res_w']: upgrade = True
            elif w == existing['res_w'] and iters > existing['iters']: upgrade = True
            
            existing['variants'] += 1
            if upgrade:
                old_p = existing['filename']
                new_v = f"{uid}v{existing['variants']}-{existing['iters']}.mp4"
                shutil.move(os.path.join(target_dir, old_p), os.path.join(cull_dir, new_v))
                
                new_p = f"{uid}P-{iters}.mp4"
                os.rename(orig_path, os.path.join(target_dir, new_p))
                db[uid].update({"filename": new_p, "iters": iters, "cs": cs, "res_w": w})
                manifest.append({"action": "UPGRADE", "new": new_p, "cull": old_p})
            else:
                v_name = f"{uid}v{existing['variants']}-{iters}.mp4"
                shutil.move(orig_path, os.path.join(cull_dir, v_name))
                manifest.append({"action": "CULL", "file": f, "moved_as": v_name})

    np.save(matrix_path, db)
    with open(manifest_path, 'w') as m: json.dump(manifest, m, indent=2)
    log(f"Done. Processed {len(videos)} files. Manifest: {manifest_path}")

if __name__ == "__main__":
    main()