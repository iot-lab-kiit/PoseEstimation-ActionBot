import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

wCam, hCam = 1024, 768
# Start video capture
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


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
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # Convert coordinates to pixel values
        h, w, _ = frame.shape
        left_shoulder = [int(coord * dim) for coord, dim in zip(left_shoulder, [w, h])]
        left_elbow = [int(coord * dim) for coord, dim in zip(left_elbow, [w, h])]
        left_wrist = [int(coord * dim) for coord, dim in zip(left_wrist, [w, h])]

        right_shoulder = [int(coord * dim) for coord, dim in zip(right_shoulder, [w, h])]
        right_elbow = [int(coord * dim) for coord, dim in zip(right_elbow, [w, h])]
        right_wrist = [int(coord * dim) for coord, dim in zip(right_wrist, [w, h])]

        # Calculate angle
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)   
        print(f"Left Elbow Angle: {left_angle}")
        print(f"Right Elbow Angle: {right_angle}")

        # Visualize landmarks and angles 
        cv2.circle(frame, tuple(left_shoulder), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(left_elbow), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(left_wrist), 5, (255, 0, 0), -1)

        cv2.line(frame, tuple(left_shoulder), tuple(left_elbow), (0, 255, 255), 2)
        cv2.line(frame, tuple(left_elbow), tuple(left_wrist), (0, 255, 255), 2)

        cv2.putText(frame, f"Left Angle: {int(left_angle)} deg", tuple(left_elbow),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.circle(frame, tuple(right_shoulder), 5,(0 ,0 ,255), -1)
        cv2.circle(frame ,tuple(right_elbow),5,(0 ,255 ,0),-1)
        cv2.circle(frame ,tuple(right_wrist),5,(255 ,0 ,0),-1)

        cv2.line(frame ,tuple(right_shoulder),tuple(right_elbow),(0 ,255 ,255),2)
        cv2.line(frame ,tuple(right_elbow),tuple(right_wrist),(0 ,255 ,255),2)

        cv2.putText(frame,f"Right Angle: {int(right_angle)} deg",tuple(right_elbow),
                    cv2.FONT_HERSHEY_SIMPLEX ,0.5,(255 ,255 ,255),2)

    # Display the frame
    cv2.imshow("Elbow Angles", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
