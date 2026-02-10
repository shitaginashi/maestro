import bpy
from . import operators

bl_info = {
    "name": "Maestro",
    "author": "Shiro",
    "version": (0, 9, 0),
    "blender": (4, 2, 0),
    "location": "Sequencer > Sidebar > Maestro",
    "description": "Trent RC0 - Sparse Blueprint Materializer",
    "category": "Sequencer",
}

def register():
    bpy.utils.register_class(operators.MAESTRO_OT_Materialize)
    bpy.utils.register_class(operators.MAESTRO_OT_ExportXML)
    bpy.utils.register_class(operators.MAESTRO_OT_Swap)
    bpy.utils.register_class(operators.MAESTRO_PT_Panel)
    
    bpy.types.Scene.maestro_show_audio = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.maestro_show_video = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.maestro_pass_sassy = bpy.props.BoolProperty(name="Sassy Mode", default=False)

def unregister():
    bpy.utils.unregister_class(operators.MAESTRO_OT_Materialize)
    bpy.utils.unregister_class(operators.MAESTRO_OT_ExportXML)
    bpy.utils.unregister_class(operators.MAESTRO_OT_Swap)
    bpy.utils.unregister_class(operators.MAESTRO_PT_Panel)