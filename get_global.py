import bpy
import numpy as np

def get_global(bone_name):
    
    context = bpy.context
    scene = context.scene
    mytool = scene.settings
    
    R = bpy.data.objects[mytool.eyedropper].matrix_world.to_3x3()
    R = np.array(R)

    t = bpy.data.objects[mytool.eyedropper].matrix_world.translation
    t = np.array(t) 

    print(f"R = {R.shape}\n{R}")
    print(f"t = {t.shape}\n{t}")

    local_location = bpy.data.objects[mytool.eyedropper].data.bones[bone_name].head_local
    local_location = np.array(local_location)
    print(f"local position = {local_location.shape}\n{local_location}")

    loc = np.dot(R, local_location) + t 
    print(f"final loc = {loc.shape}\n{loc}")

    return [loc[0], loc[1], loc[2]]