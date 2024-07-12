import bpy
from .map import map_face
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os


def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image


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


def run_face(file_path):

    addon_dir = os.path.dirname(os.path.realpath(__file__))
    model_asset_path = os.path.join(addon_dir, "face_landmarker.task")

    base_options = python.BaseOptions(model_asset_path=bpy.path.abspath(model_asset_path))
    options = vision.FaceLandmarkerOptions(base_options=base_options,
                                           output_face_blendshapes=True,
                                           output_facial_transformation_matrixes=True,
                                           num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)


    if file_path == "None": cap = cv2.VideoCapture(0)
    else: cap = cv2.VideoCapture(file_path)


    while cap.isOpened():
        # STEP 3: Load the input image.
        for n in range(9000):
            success, image = cap.read()
            if success:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        #        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                detection_result = detector.detect(mp_image)
                
                if detection_result:
                    #image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                        
                    xl = bpy.data.scenes[0].frame_current
                    l_xl = xl - 1
                            
                            
                    context = bpy.context
                    scene = context.scene  
                    mytool = scene.settings
                    
                    mouth = mytool.mouth
                    mouth_corners = mytool.mouth_corners
                    jaw = mytool.jaw
                    eyes = mytool.eyes
                    iris = mytool.iris
                    brows = mytool.brows
                    general = mytool.general
                    
                    influence = [mouth, mouth_corners, jaw, eyes, iris, brows, general]
                

                    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
                    cv2.imshow("Detection", annotated_image)
                    
                    if len(detection_result.face_blendshapes) > 0:
                        map_face(detection_result.face_blendshapes, ref_dict, influence)

            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            bpy.context.scene.frame_set(n)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
