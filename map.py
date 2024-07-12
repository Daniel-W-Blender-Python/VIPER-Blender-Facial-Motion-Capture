from . import get_global
import math

ref_dict = {
    "_neutral" : ["None"],
    "browDownLeft" : [["brow.B.L.002"], ["-y"], 5],
    "browDownRight" : [["brow.B.R.002"], ["-y"], 5],
    "browInnerUp" : [["brow.B.R.004", "brow.B.L.004"], ["y"], 5],
    "browOuterUpLeft" : [["brow.B.L"], ["y"], 5],
    "browOuterUpRight" : [["brow.B.R"], ["y"], 5],
    "cheekPuff" : ["None"],
    "cheekSquintLeft" : [["cheek.T.L.001"], ["y"], 6],
    "cheekSquintRight" : [["cheek.T.R.001"], ["y"], 6],
    "eyeBlinkLeft" : [["lid.T.L.002"], ["-y"], 6],
    "eyeBlinkRight" : [["lid.T.R.002"], ["-y"], 6],
    "eyeLookDownLeft" : [["eye.L"], ["-y"], 4],
    "eyeLookDownRight" : [["eye.R"], ["-y"], 4],
    "eyeLookInLeft" : [["eye.L"], ["-x"], 4],
    "eyeLookInRight" : [["eye.R"], ["x"], 4],
    "eyeLookOutLeft" : [["eye.L"], ["x"], 4],
    "eyeLookOutRight" : [["eye.R"], ["-x"], 4],
    "eyeLookUpLeft" : [["eye.L"], ["y"], 4],
    "eyeLookUpRight" : [["eye.R"], ["y"], 4],
    "eyeSquintLeft" : [["lid.B.L.002"], ["y / 4"], 3],
    "eyeSquintRight" : [["lid.B.R.002"], ["y / 4"], 3],
    "eyeWideLeft" : [["lid.T.L.002"], ["y"], 3],
    "eyeWideRight" : [["lid.T.R.002"], ["y"], 3],
    "jawForward" : [["jaw_master"], ["y", "-z / 6.64"], 2],
    "jawLeft" : [["jaw_master"], ["x"], 2],
    "jawOpen" : [["jaw_master"], ["y", "z"], 2],
    "jawRight" : [["jaw_master"], ["-x"], 2],
    "mouthClose" : [["lip.B"], ["y"], 0],
    "mouthDimpleLeft" : ["None"],
    "mouthDimpleRight" : ["None"],
    "mouthFrownLeft" : [["lip_end.L.001"], ["-y"], 1],
    "mouthFrownRight" : [["lip_end.R.001"], ["-y"], 1],
    "mouthFunnel" : [["lip_end.R.001", "lip_end.L.001"], ["None"], 0],
    "mouthLeft" : ["None"],
    "mouthLowerDownLeft" : [["lip_end.L.001"], ["-y"], 1],
    "mouthLowerDownRight" : [["lip_end.R.001"], ["-y"], 1],
    "mouthPressLeft" : ["None"],
    "mouthPressRight" : ["None"],
    "mouthPucker" : [["jaw_master_mouth"], ["y / 3"], 0],
    "mouthRight" : ["None"],
    "mouthRollLower" : [["lip.B", "lip.B.R.001", "lip.B.L.001"], ["rotation"], ["-x"], 6],
    "mouthRollUpper" : [["lip.T", "lip.T.R.001", "lip.T.L.001"], ["rotation"], ["x"], 6],
    "mouthShrugLower" : ["None"],
    "mouthShrugUpper" : ["None"],
    "mouthSmileLeft" : [["lip_end.L.001"], ["y"], 1],
    "mouthSmileRight" : [["lip_end.R.001"], ["y"], 1],
    "mouthStretchLeft" : ["None"],
    "mouthStretchRight" : ["None"],
    "mouthUpperUpLeft" : [["lip_end.L.001"], ["y"], 1],
    "mouthUpperUpRight" : [["lip_end.R.001"], ["y"], 1],
    "noseSneerLeft" : [["nose.L.001"], ["y"], 6],
    "noseSneerRight" : [["nose.R.001"], ["y"], 6]
    
    }
    
    
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

