bl_info = {
    "name": "VIPER Blender Facial Mocap",
    "author": "Daniel W",
    "version": (0, 1),
    "blender": (3, 60, 0),
    "location": "3D View > Sidebar > VIPER Blender Facial Mocap",
    "description": "Facial Motion Capture",
    "category": "3D View"
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup, FloatProperty, PointerProperty, StringProperty
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper
import bpy_extras
import rigify
import subprocess
import sys
import os

def install_dependencies():
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    py_lib = os.path.join(sys.prefix, 'lib', 'site-packages','pip')
    subprocess.check_call([sys.executable, "-m", "ensurepip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mediapipe"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "jaxlib"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "jax"])

def draw_file_opener(self, context):
    layout = self.layout
    scn = context.scene
    col = layout.column()
    row = col.row(align=True)
    row.prop(scn.settings, 'file_path', text='directory:')
    row.operator("something.identifier_selector", icon="FILE_FOLDER", text="")
    
    
class Settings(PropertyGroup):
    smoothing: bpy.props.FloatProperty(name = "Animation Smoothing",
                            description = "Smoothing between 0 and 1",
                            min = 0.0,
                            max = 1.0,
                            default = 0.1)

    file_path = bpy.props.StringProperty()
    
    file_name : bpy.props.StringProperty(name = "File Path:")
    
    eyedropper : bpy.props.StringProperty(name = "Armature")

    key_step : bpy.props.IntProperty(name = "Key Step", default = 2, min = 1, max = 4)

    cam_index : bpy.props.IntProperty(name = "Camera Index", default = 0, min = 0, max = 5)
    
    mouth : bpy.props.FloatProperty(name = "Mouth", min = 0, max = 1, default = 0.5)

    mouth_corners : bpy.props.FloatProperty(name = "Mouth Corners", min = 0, max = 1, default = 0.5)
    
    jaw : bpy.props.FloatProperty(name = "Jaw", min = 0, max = 1, default = 0.5)
    
    eyes : bpy.props.FloatProperty(name = "Eyes", min = 0, max = 1, default = 0.5)
    
    iris : bpy.props.FloatProperty(name = "Iris", min = 0, max = 1, default = 0.5)
    
    brows : bpy.props.FloatProperty(name = "Eyebrows", min = 0, max = 1, default = 0.5)
    
    general : bpy.props.FloatProperty(name = "General", min = 0, max = 1, default = 0.5)
    
    target : bpy.props.StringProperty(name = "Target")
    
    source : bpy.props.StringProperty(name = "Source")
    
    
    
class RunOperator_Face(bpy.types.Operator):
    """Capture Face Motion"""
    bl_idname = "object.run_body_operator_face"
    bl_label = "Run Face Operator"

    def execute(self, context):
        from .run_face import run_face
        run_face("None")
        return {'FINISHED'}

    
class RunFileSelector_Face(bpy.types.Operator, ImportHelper):
    """Import Video (Face)"""
    bl_idname = "something.identifier_selector_face"
    bl_label = "some folder"
    filename_ext = ""

    def execute(self, context):
        from .run_face import run_face
        file_name = self.properties.filepath
        run_face(file_name)
        return{'FINISHED'} 
    
    
    
class AddArmature(bpy.types.Operator):
    """Add Rig"""
    bl_idname = "object.add_rig"
    bl_label = "Add Rig"
    
    
    def execute(self, context):
        bpy.ops.object.armature_human_metarig_add()
        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.selected_objects:
            rig_name = obj.name
        context = bpy.context
        scene = bpy.context.scene
        mrig = bpy.data.objects[rig_name]
        rigify.operators.upgrade_face.update_face_rig(mrig)
        rigify.generate.generate_rig(context, mrig)
        context = bpy.context
        scene = bpy.context.scene
        #context = scene.get_context()
        return {'FINISHED'}


class InstallDependencies(bpy.types.Operator):
    """Install Dependencies"""
    bl_idname = "object.install_dependencies"
    bl_label = "Install Dependencies"
    
    
    def execute(self, context):
        install_dependencies()
        return {'FINISHED'}    
         
    
class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""

    message = bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = 'Installing additional libraries, this may take a moment...'
    )

    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        self.layout.label(text=self.message)


class BlenderMocapPanel(bpy.types.Panel):
    bl_label = "VIPER Blender Facial Mocap"
    bl_category = "VIPER Blender Facial Mocap"
    bl_idname = "VIPER Blender Facial Mocap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "VIPER Blender Facial Mocap"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        settings = context.scene.settings
        scene = context.scene
        mytool = scene.settings
        
        row = layout.row()
        row.label(text="Select an Armature")
        
        layout.prop_search(mytool, "eyedropper", context.scene, "objects")

        layout.prop(mytool, "key_step")
        layout.prop(mytool, "cam_index")
        
        row = layout.row()
        row.label(text="Run Motion Capture")
        
        row = layout.row()
        row.operator(RunOperator_Face.bl_idname, text="Capture Face Motion", icon="CAMERA_DATA")
 
        row = layout.row()
        row.operator(RunFileSelector_Face.bl_idname, text="Import Video (Face)", icon="SEQUENCE")
        
        row = layout.row()
        row.label(text="(Press (esc) to stop)")
        
        row = layout.row()
        row.operator(AddArmature.bl_idname, text="Add Rig", icon="OUTLINER_OB_ARMATURE")
        
        row = layout.row()
        row.label(text="Expressiveness")
        
        layout.prop(mytool, "mouth", slider=True)
        
        layout.prop(mytool, "mouth_corners", slider=True)
        
        layout.prop(mytool, "jaw", slider=True)
        
        layout.prop(mytool, "eyes", slider=True)
        
        layout.prop(mytool, "iris", slider=True)
        
        layout.prop(mytool, "brows", slider=True)
        
        layout.prop(mytool, "general", slider=True)

        row = layout.row()
        row.label(text="Install Mediapipe and OpenCV")

        row = layout.row()
        row.operator(InstallDependencies.bl_idname, text="Install Dependencies", icon="IMPORT")
        
        context = bpy.context     
        scene = context.scene
        mytool = scene.settings


_classes = [
    BlenderMocapPanel,
    RunOperator_Face,
    RunFileSelector_Face,
    AddArmature,
    InstallDependencies,
    Settings,
    MessageBox
]

def register():
    for c in _classes: register_class(c)
    bpy.types.Scene.settings = bpy.props.PointerProperty(type=Settings)
    


def unregister():
    for c in _classes: unregister_class(c)
    del bpy.types.Scene.settings


if __name__ == "__main__":    
    install_dependencies()
    register()
