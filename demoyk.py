import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between three points.
    :param point1: First point (shoulder)
    :param point2: Second point (elbow)
    :param point3: Third point (wrist)
    :return: Angle in degrees
    """
    a = np.array(point1)  # Shoulder
    b = np.array(point2)  # Elbow
    c = np.array(point3)  # Wrist

    # Calculate vectors
    ba = a - b
    bc = c - b

    # Calculate cosine of the angle
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Extract landmarks
        landmarks = results.pose_landmarks.landmark

        # Get coordinates of shoulder, elbow, and wrist
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # Convert coordinates to pixel values
        h, w, _ = frame.shape
        shoulder = [int(coord * dim) for coord, dim in zip(shoulder, [w, h])]
        elbow = [int(coord * dim) for coord, dim in zip(elbow, [w, h])]
        wrist = [int(coord * dim) for coord, dim in zip(wrist, [w, h])]

        # Calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)
        print(angle)
        # Visualize landmarks and angle
        cv2.circle(frame, tuple(shoulder), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(elbow), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(wrist), 5, (255, 0, 0), -1)

        cv2.line(frame, tuple(shoulder), tuple(elbow), (0, 255, 255), 2)
        cv2.line(frame, tuple(elbow), tuple(wrist), (0, 255, 255), 2)

        cv2.putText(frame, f"Angle: {int(angle)} deg", tuple(elbow),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Elbow Angle", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
