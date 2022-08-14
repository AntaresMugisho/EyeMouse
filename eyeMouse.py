# This python file uses following encoding: utf-8

import cv2
import mediapipe as mp
import pyautogui

CLICK_COUNTER = 1

# Read camera
cam = cv2.VideoCapture(0)

# Set the setting of webcam
#cam.set(3, 50)
#cam.set(4, 50)

# Detect face
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get screen size
screen_w, screen_h = pyautogui.size()

while True:
    success, frame = cam.read()

    if not success:
        print('Ignoring empty camera frame.')
        continue  # use break if reading from a video file

    # Flip the video vertically and change the BGR to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        for i, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            # Move cursor
            if i == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y, duration=0.1)

        # Manage left click
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

        closed = left[0].y - left[1].y
        if closed <= 0.005:
            print(f"Click N°{CLICK_COUNTER}")
            pyautogui.click()
            CLICK_COUNTER += 1
            #pyautogui.sleep(1)

        # Manage double click
        # ...

        # Manage right click
        # right = (landmarks[257], landmarks[386])
        # ...

        # Manage scroll
        # ...

        # Manage drag and drop
        # ...

    cv2.imshow("EyeMouse - Antares", frame)
    #cv2.waitKey(1)

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release back camera resource
cam.release()