import cv2 
import serial
import mediapipe as mp
import numpy as np
import time
import warnings

warnings.filterwarnings("ignore")

# Initialize serial communication with Arduino
# Replace '/dev/ttyACM0' with the correct port for your Arduino
#arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Camera settings
wCam, hCam = 1024, 768
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)  # First point (shoulder)
    b = np.array(b)  # Mid point (elbow)
    c = np.array(c)  # End point (wrist)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = result.pose_landmarks.landmark
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            # Display the angle on the frame
            cv2.putText(frame, str(int(angle)),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Check if the elbow is at approximately 180 degrees
            if angle >= 178 and angle <= 182:  # Allow some tolerance
                #arduino.write(b'1')  # Send '1' to turn on LED
                print("Elbow at ~180 degrees: LED ON")
            else:
                #arduino.write(b'0')  # Send '0' to turn off LED
                print("Elbow not at ~180 degrees: LED OFF")

        except Exception as e:
            print(f"Error: {e}")

        # Draw pose landmarks on the frame
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4, circle_radius=4),
                                   mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=4, circle_radius=3))

        cv2.imshow('Elbow Detection', frame) 
        if cv2.waitKey(10) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
