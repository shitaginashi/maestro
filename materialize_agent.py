import bpy
from .maestro_core import MaestroCore

class MaterializeAgent:
    def __init__(self):
        self.core = MaestroCore()

    def execute(self, context):
        spine = self.core.load_spine()
        scene = context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        
        sequencer = scene.sequence_editor
        
        for entry in spine.get('tracks', []):
            path = self.core.get_asset_path(entry['file'])
            # The 4.2 Fix: Explicit keywords for the C-API
            sequencer.sequences.new_sound(
                name=entry['file'],
                filepath=path,
                channel=entry.get('channel', 1),
                frame_start=entry.get('start', 1)
            )
            
        # Sassy Mode logic for console output
        if scene.maestro_pass_sassy:
            print("MAESTRO: Sequence materialized. Try not to break it.")
            
        return {'FINISHED'}