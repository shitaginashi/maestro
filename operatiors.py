import bpy
import os
import sys
import yaml

# --- 1. BOOTSTRAP ---
def get_maestro_root():
    return os.path.dirname(os.path.realpath(__file__))

MAESTRO_ROOT = get_maestro_root()
LIB_PATH = os.path.join(MAESTRO_ROOT, "lib")

if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

def get_recursive_vault_count(vault_path):
    count = 0
    if not os.path.exists(vault_path):
        return 0
    for root, _, files in os.walk(vault_path):
        count += sum(1 for f in files if f.lower().endswith('.wav'))
    return count

# --- 2. OPERATORS ---

class MAESTRO_OT_PopulateBraid(bpy.types.Operator):
    bl_idname = "maestro.populate_braid"
    bl_label = "Populate Braid"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        path_a = os.path.join(MAESTRO_ROOT, "a")
        try:
            import sampler
            import importlib
            importlib.reload(sampler)
            s = sampler.Sampler(path_a)
            s.execute_braid_abc(context)
            self.report({'INFO'}, "Braid Materialized")
            return {'FINISHED'}
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Sampler Fail: {e}")
            return {'CANCELLED'}

class MAESTRO_OT_CycleRunner(bpy.types.Operator):
    bl_idname = "maestro.cycle_runner"
    bl_label = "Cycle Asset"
    
def execute(self, context):
        path_a = os.path.join(MAESTRO_ROOT, "a")
        try:
            import sampler
            import importlib
            # Force a deep reload of the sampler module
            importlib.reload(sampler)
            
            # Re-instantiate with the fresh code
            s = sampler.Sampler(path_a)
            
            # Check if the method exists before calling (Defensive)
            if hasattr(s, 'execute_braid_abc'):
                s.execute_braid_abc(context)
                self.report({'INFO'}, "Braid Materialized")
            else:
                self.report({'ERROR'}, "Sampler loaded, but execute_braid_abc is missing. Check indentation/save.")
                
            return {'FINISHED'}
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Sampler Fail: {e}")
            return {'CANCELLED'}

# --- 3. UI PANEL ---

class MAESTRO_PT_Panel(bpy.types.Panel):
    bl_label = "Maestro v1.0.4-A"
    bl_idname = "MAESTRO_PT_Panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Maestro'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Flex Mode Toggle
        if hasattr(scene, "maestro_flex_mode"):
            layout.prop(scene, "maestro_flex_mode", toggle=True, icon='LIGHT')
        
        row = layout.row(align=True)
        row.operator("maestro.populate_braid", text="Populate", icon='PLAY')
        row.operator("maestro.cycle_runner", text="Cycle", icon='FILE_REFRESH')
        
        box = layout.box()
        vault_path = "/mnt/forge/audio/mega"
        v_count = get_recursive_vault_count(vault_path)
        box.label(text=f"Mega-Vault: {v_count} Assets", icon='SOUND')

# --- 4. REGISTRATION ---

classes = (
    MAESTRO_OT_PopulateBraid,
    MAESTRO_OT_CycleRunner,
    MAESTRO_PT_Panel,
)

def register():
    # Scene Property registration MUST happen before classes for drawing
    bpy.types.Scene.maestro_flex_mode = bpy.props.BoolProperty(
        name="Flex Mode",
        description="Toggle sassy/flexible latent matching",
        default=False
    )
    for cls in classes:
        # We use a try-except to handle the "Already Registered" ghosting
        try:
            bpy.utils.register_class(cls)
        except RuntimeError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass
    if hasattr(bpy.types.Scene, "maestro_flex_mode"):
        del bpy.types.Scene.maestro_flex_mode

if __name__ == "__main__":
    register()
