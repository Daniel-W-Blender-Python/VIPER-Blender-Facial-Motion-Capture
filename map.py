from .get_global import get_global
import math
    
def map_face(shapes, ref_dict, influence):
    
    context = bpy.context
    scene = context.scene
    mytool = scene.settings
    
    armature = scene.objects.get(mytool.eyedropper)
    
    if bpy.data.scenes[0].frame_current % 2 == 0:
     
        for i in range(len(shapes[0])):
            
            if ref_dict[shapes[0][i].category_name][0] != "None":

                if shapes[0][i].category_name == "mouthFunnel":
                        
                    r_bone = armature.pose.bones.get(ref_dict[shapes[0][i].category_name][0][0])
                    l_bone = armature.pose.bones.get(ref_dict[shapes[0][i].category_name][0][1])
                    
                    r_reference_bone = armature.pose.bones.get("cheek.B.R.001")
                    l_reference_bone = armature.pose.bones.get("cheek.B.L.001")
                    
                    r_global = get_global(r_bone.name)
                    l_global = get_global(l_bone.name)
                    r_reference_global = get_global(r_reference_bone.name)
                    l_reference_global = get_global(l_reference_bone.name)
                    
                    l_distance = math.sqrt((r_global[0] - l_reference_global[0])**2 + (r_global[1] - l_reference_global[1])**2 + (r_global[2] - l_reference_global[2])**2)
                    r_distance = math.sqrt((l_global[0] - l_reference_global[0])**2 + (l_global[1] - l_reference_global[1])**2 + (l_global[2] - l_reference_global[2])**2)
                    
                    if l_distance > r_distance:
                    
                        l_bone.location.x = shapes[0][i].score * influence[0] * 2 * -1 / 10
                        r_bone.location.x = shapes[0][i].score * influence[0] * 2 / 10

                for k in range(len(ref_dict[shapes[0][i].category_name][0])):
                    
                    for j in range(len(ref_dict[shapes[0][i].category_name][1])):
                        bone = armature.pose.bones.get(ref_dict[shapes[0][i].category_name][0][k])
       
                        if ref_dict[shapes[0][i].category_name][1][j] == "x":
                            bone.location.x = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "-x":
                            bone.location.x = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * -1 / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "y":
                            bone.location.y = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "-y":
                            bone.location.y = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * -1 / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "z":
                            bone.location.z = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "-z":
                            bone.location.z = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * -1 / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "-z / 6.64":
                            bone.location.z = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * -1 / 6.64 / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "y / 3":
                            bone.location.y = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * 1 / 3 / 10
                        elif ref_dict[shapes[0][i].category_name][1][j] == "y / 4":
                            bone.location.y = shapes[0][i].score / len(ref_dict[shapes[0][i].category_name][1]) * influence[ref_dict[shapes[0][i].category_name][2]] * 1 / 4 / 10

                        bone.keyframe_insert(data_path="location", frame=bpy.data.scenes[0].frame_current) 

