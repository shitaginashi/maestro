import bpy
from .materialize_agent import MaterializeAgent

class MAESTRO_OT_Materialize(bpy.types.Operator):
    bl_idname = "maestro.materialize"
    bl_label = "Materialize Sequence"
    
    def execute(self, context):
        agent = MaterializeAgent()
        return agent.execute(context)

class MAESTRO_OT_ExportXML(bpy.types.Operator):
    bl_idname = "maestro.export_xml"
    bl_label = "Export Final XML"
    def execute(self, context):
        return {'FINISHED'}

class MAESTRO_OT_Swap(bpy.types.Operator):
    bl_idname = "maestro.swap_asset"
    bl_label = "Swap Rank"
    def execute(self, context):
        return {'FINISHED'}

class MAESTRO_PT_Panel(bpy.types.Panel):
    bl_label = "Maestro Control"
    bl_idname = "MAESTRO_PT_Panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Maestro'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator("maestro.materialize", icon='NODE_INSERT')
        layout.operator("maestro.swap_asset", icon='UV_SYNC_SELECTION')
        layout.prop(scene, "maestro_pass_sassy", text="Sassy Mode")
        layout.operator("maestro.export_xml", icon='EXPORT')

def register():
    bpy.utils.register_class(MAESTRO_OT_Materialize)
    bpy.utils.register_class(MAESTRO_OT_ExportXML)
    bpy.utils.register_class(MAESTRO_OT_Swap)
    bpy.utils.register_class(MAESTRO_PT_Panel)

def unregister():
    bpy.utils.unregister_class(MAESTRO_OT_Materialize)
    bpy.utils.unregister_class(MAESTRO_OT_ExportXML)
    bpy.utils.unregister_class(MAESTRO_OT_Swap)
    bpy.utils.unregister_class(MAESTRO_PT_Panel)