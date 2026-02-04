import bpy
import os
from .lib.sampler import Sampler

# Intent Map: Pairing Visual Tiers to Latent Vectors
# A = High Impact, B = Transition, C = Glitch/Texture
INTENT_MAP = {
    "A": {"vector": "+0+", "duration": 5.0},
    "B": {"vector": "+0-", "duration": 3.0},
    "C": {"vector": "00-", "duration": 1.5}
}

class MAESTRO_OT_PopulateBraid(bpy.types.Operator):
    bl_idname = "sequencer.maestro_populate_braid"
    bl_label = "Populate A/B/C Braid"

    def execute(self, context):
        # Assumes the YAML is in the same folder as the .blend
        inventory_path = bpy.path.abspath("//latent_inventory.yml")
        if not os.path.exists(inventory_path):
            self.report({'ERROR'}, "Inventory YAML not found in project root.")
            return {'CANCELLED'}

        trent = Sampler(inventory_path)
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        
        for marker in scene.timeline_markers:
            tier = marker.name.upper()
            if tier in INTENT_MAP:
                intent = INTENT_MAP[tier]
                results = trent.query(intent["vector"], intent["duration"])
                
                if results:
                    winner = results[0]
                    # Logic: Align 't_h' (Hit Anchor) to Marker Frame
                    start_frame = marker.frame - (winner['t_h'] * fps)
                    
                    strip = scene.sequence_editor.sequences.new_sound(
                        name=f"{tier}_{winner['id']}",
                        filepath=winner['path'],
                        channel=2 if tier == "A" else (3 if tier == "B" else 4),
                        frame_start=int(start_frame)
                    )
                    # Bind metadata for cycling
                    strip["maestro_tier"] = tier
                    strip["maestro_index"] = 0
                    strip["anchor_frame"] = marker.frame
                    
        return {'FINISHED'}

class MAESTRO_OT_CycleRunner(bpy.types.Operator):
    bl_idname = "sequencer.maestro_cycle_runner"
    bl_label = "Cycle Runner Up"

    def execute(self, context):
        strip = context.active_sequence
        if not strip or "maestro_tier" not in strip:
            self.report({'WARNING'}, "Select a Maestro strip.")
            return {'CANCELLED'}

        inventory_path = bpy.path.abspath("//latent_inventory.yml")
        trent = Sampler(inventory_path)
        
        tier = strip["maestro_tier"]
        intent = INTENT_MAP[tier]
        results = trent.query(intent["vector"], intent["duration"])
        
        # Cycle through the Top 6
        new_index = (strip["maestro_index"] + 1) % len(results)
        asset = results[new_index]
        
        # Swap and Re-align
        strip.sound.filepath = asset['path']
        strip["maestro_index"] = new_index
        fps = context.scene.render.fps / context.scene.render.fps_base
        strip.frame_start = int(strip["anchor_frame"] - (asset['t_h'] * fps))
        
        return {'FINISHED'}