bl_info = {
    "name": "Blender Facial Mocap",
    "author": "Daniel W",
    "version": (0, 1),
    "blender": (3, 60, 0),
    "location": "3D View > Sidebar > Blender Facial Mocap",
    "description": "Facial Motion Capture",
    "category": "3D View"
}

import bpy
from . import panel

_classes = [
    BlenderMocapPanel,
    RunOperator_Face,
    RunFileSelector_Face,
    AddArmature,
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
    register()    
