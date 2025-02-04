import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import platform

# Determine serial port dynamically
if platform.system() == "Windows":
    port = "COM9"  # Adjust as necessary

else:
    port = "/dev/ttyACM0"

# Initialize serial communication   
try:
    SerialObj = serial.Serial(port, baudrate=9600, timeout=1)
except Exception as e:
    print(f"Error initializing serial port: {e}")
    SerialObj = None

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Configure camera
wCam, hCam = 1024, 768
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

def calculate_angle(point1, point2, point3):
    a, b, c = np.array(point1), np.array(point2), np.array(point3)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

# Main video loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w, _ = frame.shape

        # Right arm landmarks
        right_shoulder = [int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h)]
        right_elbow = [int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w),
                       int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h)]
        right_wrist = [int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w),
                       int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h)]
        right_palm = [int(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x * w),
                      int(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y * h)]

        # Calculate angles
        elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Shoulder angle with a vertical reference
        vertical_reference = [right_shoulder[0], right_shoulder[1] + 100]
        shoulder_angle = calculate_angle(vertical_reference, right_shoulder, right_elbow)

        # Wrist angle with a horizontal reference
        horizontal_reference = [right_wrist[0] + 100, right_wrist[1]]
        wrist_angle = calculate_angle(horizontal_reference, right_wrist, right_palm)

        # Send angles to serial port
        if SerialObj:
            try:
                SerialObj.write(f"{int(elbow_angle)},{int(shoulder_angle)},{int(wrist_angle)}\n".encode())
            except Exception as e:
                print(f"Serial transmission error: {e}")

        # Visualization
        cv2.circle(frame, tuple(right_shoulder), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_elbow), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(right_wrist), 5, (255, 0, 0), -1)
        cv2.circle(frame, tuple(right_palm), 5, (255, 255, 0), -1)
        cv2.line(frame, tuple(right_shoulder), tuple(right_elbow), (0, 255, 255), 2)
        cv2.line(frame, tuple(right_elbow), tuple(right_wrist), (0, 255, 255), 2)
        cv2.line(frame, tuple(right_wrist), tuple(right_palm), (0, 255, 255), 2)

        # Display angles
        cv2.putText(frame, f"Elbow: {int(elbow_angle)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Shoulder: {int(shoulder_angle)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Wrist: {int(wrist_angle)}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("3axis pose estimation", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
if SerialObj:
    SerialObj.close()
cv2.destroyAllWindows()
