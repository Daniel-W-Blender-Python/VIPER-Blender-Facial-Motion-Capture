import bpy
from . import map
import cv2
from . import mediapipe_setup

def run_face(file_path):
    
    # STEP 2: Create an FaceLandmarker object.
    base_options = python.BaseOptions(model_asset_path=bpy.path.abspath("4.0/python/lib/site-packages/facial_mocap/face_landmarker.task"))
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
