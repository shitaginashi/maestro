bl_info = {
    "name": "Maestro",
    "blender": (4, 2, 0),
    "category": "Sequencer",
}

from . import operators

def register():
    operators.register()

def unregister():
    operators.unregister()