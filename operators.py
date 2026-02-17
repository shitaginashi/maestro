import bpy
import os
from .maestro_core import MaestroEngineV3

class MAESTRO_OT_RunVSEBridge(bpy.types.Operator):
    bl_idname = "maestro.run_vse_bridge" 
    bl_label = "Run Maestro VSE Bridge"
    
    def execute(self, context):
        from . import maestro_core
        # The Modern V3 Engine (Statistical Rarity)
        engine = maestro_core.MaestroEngineV3() 
        
        # Step 1: Materialize (The 7-hit structural pillars)
        success = engine.materialize_with_statistical_rarity()
        
        if success:
            # Step 2: Export (Fixed the 'core' name error)
            engine.export_to_edl() 
            self.report({'INFO'}, "MAESTRO V3: Pillars & EDLs Generated")
        else:
            self.report({'ERROR'}, "MAESTRO: Bridge Materialization Failed")
            
        return {'FINISHED'}

class MAESTRO_OT_AnalyzeSoundtrack(bpy.types.Operator):
    bl_idname = "maestro.analyze_soundtrack"
    bl_label = "Analyze Soundtrack"
    
def execute(self, context):
        from . import maestro_core
        # Initialize the V3 Engine
        engine = maestro_core.MaestroEngineV3() 
        
        # 1. Materialize the VSE
        success = engine.materialize_with_statistical_rarity()
        
        if success:
            # 2. Export EDLs using the SAME instance
            # Ensure this method exists in your MaestroEngineV3 class!
            engine.export_to_edl() 
            self.report({'INFO'}, "MAESTRO: V3.2 Timeline & EDLs Materialized")
        else:
            self.report({'ERROR'}, "MAESTRO: Materialization failed.")
            
        return {'FINISHED'}

class MAESTRO_PT_MainPanel(bpy.types.Panel):
    bl_label = "Maestro V3"
    bl_idname = "MAESTRO_PT_main_panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Maestro"

    def draw(self, context):
        layout = self.layout
        
        # Section 1: Analysis
        col = layout.column(align=True)
        col.label(text="Step 1: Acoustic Analysis")
        # Ensure this operator is registered
        col.operator("maestro.analyze_soundtrack", icon='SOUND')
        
        layout.separator()
        
        # Section 2: Materialization
        col = layout.column(align=True)
        col.label(text="Step 2: Generate Braid")
        col.operator("maestro.run_vse_bridge", icon='PLAY', text="Materialize Timeline")

        layout.separator()

        # Section 3: External Handoff
        layout.label(text="Step 3: External Handoff")
        # We point this to the new EDL logic
        layout.operator("maestro.run_vse_bridge", icon='EXPORT', text="Export EDLs")
        
        # Section 4: Diagnostic Info
        box = layout.box()
        box.label(text="RC2 Status: Operational", icon='SEQUENCE')

class MAESTRO_OT_ExportXML(bpy.types.Operator):
    """Export Spine to XML/EDL using V3 Engine"""
    bl_idname = "maestro.export_xml"
    bl_label = "Export XML"

    def execute(self, context):
        from . import maestro_core
        # Switch to the new engine class
        engine = maestro_core.MaestroEngineV3()
        
        # We must run the rarity logic first to determine WHICH hits exist
        # before we can export them.
        success = engine.materialize_with_statistical_rarity()
        
        if success:
            engine.export_to_edl()
            self.report({'INFO'}, "MAESTRO V3: EDLs Exported to Forge")
        else:
            self.report({'ERROR'}, "MAESTRO: Export Failed")
            
        return {'FINISHED'}

# THE RESTORED REGISTRATION TUPLE
# Using consistent CamelCase for class names to avoid NameErrors
classes = (
    MAESTRO_OT_AnalyzeSoundtrack,
    MAESTRO_OT_RunVSEBridge,
    MAESTRO_OT_ExportXML,
    MAESTRO_PT_MainPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)