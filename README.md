# VIPER: Video and Image-based Pose Estimation (Pre-Cursor)
A Blender addon that uses Google's Mediapipe Face Landmarker to map facial expressions onto a 3D character in real time. This Facial Motion Capture Addon is a pre-cursor to my 3D human pose estimation model, VIPER (Video and Image-based Pose Estimation), which I hope to release within the next year or so.

# Demo:
https://www.loom.com/share/9b76c306718d48fcbcf54203242fef00

The addon uses Mediapipe Facial Landmarker, a subset of Google's Mediapipe project. The landmarker generates a bar graph with values representing the shape of the face, called "blendshapes." This addon takes advantage of such a feature to detect an actor's facial movements and apply them to Blender's Rigify bone rig in real time. However, along with simply retargeting facial motion onto a 3D character, the addon has other features to make this more personalized for the animator.

In order to map the facial expressions onto the rig, you must select the desired rig, from the scene objects, under "Select and Armature." Then, set "Key Step" to your desired integer. Key step refers to the amount of frames skipped before inserting another keyframe (subtract one). Increasing the key step increases the smoothness of the animation, but decreases the precision that the landmarker provides. The camera index refers to the pythonic index of the camera (webcam being 0, any external camera being 1+). Using Iriun Webcam on a smart phone (on a head rig) in conjunction with Rokoko (Monocular Mocap or Mocap suit), in which you would set the camera index to 1, can achieve real-time full-body motion capture.

The "Expressiveness" sliders allow control over the influence of the mouth, mouth corners, jaw, eyes, iris, and eyebrows, so that the animator can customize the motion capture to fit their liking.

Finally, the "Install Dependencies" button allows installation of Mediapipe and OpenCV (which must be installed using administrator privilages). You only need to install dependencies once after the addon has been added to Blender; you never have to install them on that device again (except if the libraries are updated). More information for troubleshooting is in the following video, and any other issues can be placed in this repository, and I will try to fix them as soon as possible.

# Installation
https://www.loom.com/share/949fc1b42b6743f6bddaaebf350a73e9

Any issues with installation should be put in this repository. I will try to address them as soon as possible.

# Future Work
