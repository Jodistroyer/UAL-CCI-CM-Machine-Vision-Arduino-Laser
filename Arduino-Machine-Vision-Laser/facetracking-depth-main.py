import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata
import numpy as np
import time
import pygame

# Initialize pygame mixer for sound playback
pygame.mixer.init()
# Replace with your sound file path. MUST be a .wav file.
sound = pygame.mixer.Sound("scream.wav")

# Initialize camera (you have to play around to see which one works for you)
# cv2.VideoCapture(1) is for default webcam
# cv2.VideoCapture(1) is for laptop webcam
# cv2.VideoCapture(2) is for external webcam
cap = cv2.VideoCapture(1)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't Access!!!")
    exit()

# Initialize Arduino. Adjust port as needed
# https://www.mathworks.com/help/matlab/supportpkg/find-arduino-port-on-windows-mac-and-linux.html
port = "COM7"
board = pyfirmata.Arduino(port)

# Define pins
servo_pinX = board.get_pin('d:5:s')
servo_pinY = board.get_pin('d:6:s')

# If you want lasers to stay off unless they see a face, then change :s to :o
laser_pin1 = board.get_pin('d:9:s')
laser_pin2 = board.get_pin('d:10:s')
laser_pin3 = board.get_pin('d:11:s')

# Initialize face detector
# minDetectionCon = minimum detection confidence threshold
# modelSelection= 0 (short range of 1 meter)
# modelSelection= 1 (long range of 5 meters)
detector = FaceDetector(modelSelection=0)
servoPos = [90, 30]  # initial servo position
servo_pinX.write(servoPos[0])
servo_pinY.write(servoPos[1])

# Scanning parameters
scanDirection = 1  # 1 for right, -1 for left
scanLimit = [30, 180]  # Scanning range in degrees

playing_sound = False  # Variable to track sound playback state

scaling_factor = 0.5  # Adjust this factor as needed

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # Initialize variables to store information about the closest face
        min_distance = float('inf')
        closest_face = None

        for bbox in bboxs:
            # Get the center coordinates of the detected face
            fx, fy = bbox["center"][0], bbox["center"][1]

            # Calculate width of the face (assuming distance between eye corners)
            w = bbox["bbox"][2]  # Width in pixels
            W = 6.3  # Width of the face in centimeters. This is the average length between eyes for all humans.

            # Calculate distance from the camera using the known width and focal length
            f = 840  # Focal length of the camera
            d = (W * f) / w  # Formula for distance

            # Update closest face if it is closer than the previous closest face
            if d < min_distance:
                min_distance = d
                closest_face = bbox

        # Get the coordinates of the closest face
        fx, fy = closest_face["center"][0], closest_face["center"][1]
        pos = [fx, fy]

        # Calculate distance of the face from the center of the frame
        distance_from_center = abs(fx - ws / 2)

        # Adjust servo movement based on distance from center
        # This increases laser pointer accuracy on x-axis
        servoX_range = 180 * scaling_factor
        servoX = np.interp(fx, [0, ws], [90 - servoX_range / 2, 90 + servoX_range / 2])

        # Clip servo position to ensure it stays within valid range
        servoX = np.clip(servoX, 0, 180)

        # Convert coordinates to servo degree
        servoY = np.interp(fy, [0, hs], [0, 60])
        servoY = np.clip(servoY, 0, 180)

        servoPos[0] = servoX
        servoPos[1] = servoY

        cv2.circle(img, (int(fx), int(fy)), 80, (0, 0, 255), 2)
        cv2.putText(img, str(pos), (int(fx) + 15, int(fy) - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.line(img, (0, int(fy)), (ws, int(fy)), (0, 0, 0), 2)  # x line
        cv2.line(img, (int(fx), hs), (int(fx), 0), (0, 0, 0), 2)  # y line
        cv2.circle(img, (int(fx), int(fy)), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "TARGET LOCKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Turn on the laser
        laser_pin1.write(1)
        laser_pin2.write(1)
        laser_pin3.write(1)

        # Play sound in a loop if not already playing
        if not playing_sound:
            sound.play(loops=-1)  # Loop indefinitely
            playing_sound = True

    else:
        cv2.putText(img, "NO TARGET", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)  # x line
        cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)  # y line

        # Turn off the laser
        laser_pin1.write(0)
        laser_pin2.write(0)
        laser_pin3.write(0)

        # Stop the sound if playing
        if playing_sound:
            sound.stop()
            playing_sound = False

        # Scanning motion
        servoPos[0] += scanDirection * 2  # Change the step size as needed
        if servoPos[0] > scanLimit[1] or servoPos[0] < scanLimit[0]:
            scanDirection *= -1  # Change direction

    cv2.putText(img, f'Servo X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    servo_pinX.write(servoPos[0])
    servo_pinY.write(servoPos[1])

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
