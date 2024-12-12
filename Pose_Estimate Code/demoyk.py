import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import platform

# Determine serial port dynamically
if platform.system() == "Windows":
    port = "COM5"  # Adjust as necessary
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
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Configure camera
wCam, hCam = 1024, 768
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Desired FPS
desired_fps = 30
frame_delay = 1 / desired_fps  # Time per frame in seconds

def calculate_angle(point1, point2, point3):
    a, b, c = np.array(point1), np.array(point2), np.array(point3)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

# Main video loop
while cap.isOpened():
    start_time = time.time()  # Record start time of frame processing

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

        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Send angle to serial port
        if SerialObj:
            try:
                SerialObj.write(f"{int(right_angle)}\n".encode())
            except Exception as e:
                print(f"Serial transmission error: {e}")

        # Visualization
        cv2.circle(frame, tuple(right_shoulder), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_elbow), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(right_wrist), 5, (255, 0, 0), -1)
        cv2.line(frame, tuple(right_shoulder), tuple(right_elbow), (0, 255, 255), 2)
        cv2.line(frame, tuple(right_elbow), tuple(right_wrist), (0, 255, 255), 2)
        cv2.putText(frame, f"Angle: {int(right_angle)} deg", tuple(right_elbow),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Elbow Angles", frame)

    # Measure elapsed time for frame processing
    elapsed_time = time.time() - start_time
    delay = max(0, frame_delay - elapsed_time)  # Ensure no negative delay
    time.sleep(delay)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
if SerialObj:
    SerialObj.close()
cv2.destroyAllWindows()



#following is the code that implements angle smoothing to reduce jitters in movement, but may result in slower response. parameters might need refining before deployment.

#NOTE: does it need a low pass or a high pass filter? i think it may need a high pass considering the use case

'''
import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import platform

# Determine serial port dynamically
if platform.system() == "Windows":
    port = "COM3"  # Adjust as necessary
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
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Configure camera
wCam, hCam = 1024, 768
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Desired FPS
desired_fps = 30
frame_delay = 1 / desired_fps  # Time per frame in seconds

# Low-pass filter parameters
alpha = 0.2  # Smoothing factor (lower is smoother)
filtered_angle = None  # Initialize filtered angle

def calculate_angle(point1, point2, point3):
    a, b, c = np.array(point1), np.array(point2), np.array(point3)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

# Main video loop
while cap.isOpened():
    start_time = time.time()  # Record start time of frame processing

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

        # Calculate raw angle
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Apply low-pass filter
        if filtered_angle is None:
            filtered_angle = right_angle  # Initialize with the first value
        else:
            filtered_angle = alpha * right_angle + (1 - alpha) * filtered_angle

        # Send filtered angle to serial port
        if SerialObj:
            try:
                SerialObj.write(f"{int(filtered_angle)}\n".encode())
            except Exception as e:
                print(f"Serial transmission error: {e}")

        # Visualization
        cv2.circle(frame, tuple(right_shoulder), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_elbow), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(right_wrist), 5, (255, 0, 0), -1)
        cv2.line(frame, tuple(right_shoulder), tuple(right_elbow), (0, 255, 255), 2)
        cv2.line(frame, tuple(right_elbow), tuple(right_wrist), (0, 255, 255), 2)
        cv2.putText(frame, f"Filtered Angle: {int(filtered_angle)} deg", tuple(right_elbow),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Elbow Angles", frame)

    # Measure elapsed time for frame processing
    elapsed_time = time.time() - start_time
    delay = max(0, frame_delay - elapsed_time)  # Ensure no negative delay
    time.sleep(delay)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
if SerialObj:
    SerialObj.close()
cv2.destroyAllWindows()
'''
