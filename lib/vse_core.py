import bpy
import yaml
from pathlib import Path

def braid_test_markers(findings_path):
    """
    Reads the Trent report and places markers in the current Blender scene.
    """
    if not Path(findings_path).exists():
        print(f"Error: {findings_path} not found.")
        return

    with open(findings_path, 'r') as f:
        report = yaml.safe_load(f)

    print(f"--- Braiding Shards from {report['source']} ---")

    # Clear existing markers for a clean test
    bpy.context.scene.timeline_markers.clear()
    
    fps = bpy.context.scene.render.fps
    
    for ping in report['trajectory_pings']:
        freq = ping['frequency']
        for timestamp in ping['detections']:
            frame = int(timestamp * fps)
            
            # Place a marker as a 'Rational' placeholder
            marker_name = f"PING_{freq}Hz"
            bpy.context.scene.timeline_markers.new(name=marker_name, frame=frame)
            
    print(f"Braid Complete: {len(bpy.context.scene.timeline_markers)} markers placed.")