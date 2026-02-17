import bpy
import os
import yaml
import subprocess

# --- CONFIGURATION ---
CWD = "/mnt/forge/forge/maestro/"
SPINE_PATH = os.path.join(CWD, "spine.yml")
SOUNDTRACK_WAV = os.path.join(CWD, "soundtrack.wav")

def prepare_rc2_scene():
    """Step 1: Ingest audio and lock scene bounds."""
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    # Audio Conversion Fallback
    if not os.path.exists(SOUNDTRACK_WAV):
        mp3s = [f for f in os.listdir(CWD) if f.endswith('.mp3')]
        if mp3s:
            print(f"MAESTRO: Converting {mp3s[0]}...")
            subprocess.run(['ffmpeg', '-i', os.path.join(CWD, mp3s[0]), '-ar', '48000', SOUNDTRACK_WAV, '-y'])
    
    # Place Master Soundtrack and Set Endframe
    if os.path.exists(SOUNDTRACK_WAV):
        # Clear existing to prevent doubling
        for s in scene.sequence_editor.sequences:
            if s.name == "MASTER_ST": scene.sequence_editor.sequences.remove(s)
            
        st = scene.sequence_editor.sequences.new_sound("MASTER_ST", SOUNDTRACK_WAV, channel=1, frame_start=1)
        scene.frame_end = int(st.frame_duration)
        print(f"MAESTRO: Scene locked to {scene.frame_end} frames.")
        return True
    return False

def filter_ranked_braid(target_count=30):
    """
    Sorts beats by integrity and fills the 400f slots 
    to ensure we get the 'best' matches without crowding.
    """
    with open(SPINE_PATH, 'r') as f:
        data = yaml.safe_load(f)
    
    # Sort all 679 beats by integrity (highest first)
    all_beats = sorted(data.get('beats', []), key=lambda x: x.get('integrity', 0), reverse=True)
    
    final_spine = []
    # Track occupied frames to respect the 400f Video Guard
    occupied = {"A": [], "B": [], "C": []}

    for beat in all_beats:
        lane = beat.get('lane', 'A')
        t_frame = int(beat['t_delta'] * 24)
        
        # Check if this frame is at least 400f away from any already placed clip in this lane
        if all(abs(t_frame - p) >= 400 for p in occupied[lane]):
            final_spine.append(beat)
            occupied[lane].append(t_frame)
            
        # Stop if we've reached a healthy density for this lane
        if len(occupied[lane]) >= target_count:
            continue

    print(f"MAESTRO: Ranked 679 hits down to {len(final_spine)} high-integrity, non-overlapping beats.")
    return sorted(final_spine, key=lambda x: x['t_delta']) # Return in chronological order

# --- EXECUTION ---
if prepare_rc2_scene():
    rational_spine = filter_complementary_spine(min_integrity=0.75)
    # Store this for the Sampler in the next iteration