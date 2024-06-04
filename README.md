# UAL-CCI-CM-Machine-Vision-Arduino-Laser

**Operating Instructions**

**Ran using Pycharm Community Edition 2024.1.1**  
**Python 3.12**

**Required Packages for installation**
1. **cvzone 1.6.1** (is used for computer vision)
2. **mediapipe 0.10.14** (is used for computer vision)
3. **pyFirmata 1.1.0** (is used for python to Arduino communication)
4. **pygame 2.5.2** (is used for PC to play sound when face detected)

Open and run facetracking-depth-main.py

**PS:** If you have OBS Studios or similar software Installed, make sure that you open the application, and Start Virtual Camera is on while running this project. Or else it won’t be able to open your webcam.

## Features
1. Face tracking with lasers
2. Algorithms for more accurate face tracking
3. Depth perception so that if there are multiple faces, it will focus only the nearest one

## This project mixes both Haarcascade and OpenCV Machine Vision.  
Haarcascade is good at detecting objects in images irrespective of their scale in image and location.  
But a problem faced by using only Haarcascade is:  

A. It needs a wide skin patch for a successful detection. (Small patches won’t work well.)  
B. Haar cascades are usually trained only on frontal face images. (Covered faces won’t work.)

**SO mixing it with deep learning models will allow various face angles and better detection of side profiles.**

## Debugging:
You may get an error saying pyFirmata gives error: module 'inspect' has no attribute 'getargspec'  
This is because of: <https://stackoverflow.com/questions/74585622/pyfirmata-gives-error-module-inspect-has-no-attribute-getargspec>

**The Quick Fix Is:**  
Open up the debug console and click on the link which says something like `(C:\Python312\Lib\site-packages\pyfirmata\pyfirmata.py)`. The link will send you to the pyfirmata code. As of writing this, it should send you to line 185 of `pyfirmata.py`. 

The error message will look something like:

  File "C:\Python312\Lib\site-packages\pyfirmata\pyfirmata.py", line 185, in add_cmd_handler
    len_args = len(inspect.getargspec(func)[0])
                   ^^^^^^^^^^^^^^^^^^

**So go to line 185, and then replace**

len_args = len(inspect.getargspec(func)[0])

with

len_args = len(inspect.getfullargspec(func).args)

Rerun the code and it should work. 


## Acknowledgements:  
Thank you to the below people, for making this project possible.

**Computer Vision With Arduino | 2 Hour Course | OpenCV Python**  
*(Murtaza's Workshop - Robotics and AI)*  
<https://www.youtube.com/watch?v=mfiRJ1qgToc&list=PLE2NfML5IlFrC-0lxbQ5SrHt1DchouJVy&index=119>

**Face-Detection**  
*(rizkydermawan1992)*  
<https://github.com/rizkydermawan1992/Face-Detection>

**Face Distance Measurement with a Normal Webcam | Computer Vision**  
*(Murtaza's Workshop - Robotics and AI)*  
<https://www.youtube.com/watch?v=jsoe1M2AjFk>

## Authorship
A code project by Wong Jo-Hann

23/24 Creative Making Experience and Physical Computing

Creative Computing BSc class

UAL CCI University Of the Arts London
