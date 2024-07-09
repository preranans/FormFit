from flask import Flask, Response
import cv2
import mediapipe as mp
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app, resources={r"/dumbbell_lateral_raise": {"origins": "http://localhost:3000"}})

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

@app.route('/dumbbell_lateral_raise', methods=['GET','POST'])
def dumbbell_lateral_raise():
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    up = False
    counter = 0
    if not cap.isOpened():
        return "Error: Cannot open webcam."

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)
            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[13], 15, (255, 0, 0), cv2.FILLED)
            if not up and points[14][1] + 10 < points[12][1]:
                print("UP")
                up = True
                counter += 1
            elif points[14][1] > points[12][1]:
                print("Down")
                up = False
        cv2.putText(
            img, str(counter), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )

        # Display the frame in a window
        cv2.imshow('Webcam Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"


@app.route('/sit-up_with_arms_on_chest',methods=['GET','POST'])
def sit_up_with_arms_on_chest():
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    up = False
    counter = 0
    if not cap.isOpened():
        return "Error: Cannot open webcam."

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)
            if not up and points[12][1] > points[24][1]:
                print("UP")
                up = True
            elif up and points[12][1] < points[24][1]:
                print("Down")
                up = False
                counter += 1
        cv2.putText(
            img, str(counter), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )

        # Display the frame in a window
        cv2.imshow('Webcam Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"

@app.route('/air_bike',methods=['GET','POST'])
def air_bike_counter():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Initialize MediaPipe Pose with higher confidence thresholds
    pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.7)

    # Initialize webcam capture
    cap = cv2.VideoCapture("Air-bike.mp4")
    rep_counter = 0
    prev_rep_detected = False

    if not cap.isOpened():
        return "Error: Cannot open webcam."

    # Function to calculate angle between three points
    def calculate_angle(a, b, c):
        radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
        angle = abs(radians * 180.0 / math.pi)
        return angle

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extracting landmark points
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            # Calculate angle between thigh and torso for each leg
            right_knee_angle = calculate_angle(points[24], points[26], points[28])
            left_knee_angle = calculate_angle(points[23], points[25], points[27])

            # Check for air bike movement
            if right_knee_angle > 160 and left_knee_angle > 160:
                if not prev_rep_detected:
                    rep_counter += 1
                    prev_rep_detected = True
                    print("Rep Detected")

            else:
                prev_rep_detected = False

            # Display rep counter on the frame
            cv2.putText(img, f"Reps: {rep_counter}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Webcam Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"

@app.route('/alternate_heel_touchers', methods=['GET','POST'])
def alternate_heeltouch_counter():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Initialize MediaPipe Pose with higher confidence thresholds
    pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    # Initialize video capture
    cap = cv2.VideoCapture("Alternate-heel-touch.mp4")
    rep_counter = 0
    prev_rep_detected = False

    if not cap.isOpened():
        return "Error: Cannot open video."

    while True:
        success, img = cap.read()
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Get landmark positions
            landmarks = results.pose_landmarks.landmark
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate distances between wrist and shoulder landmarks
            right_distance = abs(right_wrist.y - right_shoulder.y)
            left_distance = abs(left_wrist.y - left_shoulder.y)

            # Detect alternate heel touches
            if right_distance < 0.1 and left_distance < 0.1:
                if not prev_rep_detected:
                    rep_counter += 1
                    prev_rep_detected = True
                    print("Rep Detected")

            else:
                prev_rep_detected = False

            # Display rep counter on the frame
            cv2.putText(img, f"Reps: {rep_counter}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Video Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Video feed closed"

@app.route('/shoulder_tap',methods=['GET','POST'])
def shoulder_tap_counter():
    # Initialize MediaPipe Pose with higher confidence thresholds
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    
    mp_drawing = mp.solutions.drawing_utils  # Initialize drawing utils inside the function

    # Initialize webcam capture (change to 0 for default webcam)
    cap = cv2.VideoCapture("Shoulder-Tap.mp4")
    if not cap.isOpened():
        return "Error: Cannot open webcam."

    tap_count = 0
    tap_detected = False
    last_tapped_shoulder = None

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract key landmark points
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

            # Calculate angles
            def calculate_angle(a, b, c):
                radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
                angle = abs(radians * 180.0 / math.pi)
                return angle

            left_angle = calculate_angle([left_shoulder.x, left_shoulder.y], [left_elbow.x, left_elbow.y],
                                         [right_elbow.x, right_elbow.y])
            right_angle = calculate_angle([right_shoulder.x, right_shoulder.y], [right_elbow.x, right_elbow.y],
                                          [left_elbow.x, left_elbow.y])

            # Check for shoulder tap movement
            if left_angle < 100 and right_angle < 100:  # Adjust angle thresholds here
                if not tap_detected:
                    if last_tapped_shoulder == 'right':
                        last_tapped_shoulder = 'left'
                    elif last_tapped_shoulder == 'left':
                        last_tapped_shoulder = 'right'
                    else:
                        last_tapped_shoulder = 'right'  # Start with right if no taps detected yet
                    tap_detected = True
                    print("Shoulder Tap Counted")
                    tap_count += 1
            else:
                tap_detected = False

            # Display shoulder tap counter on the frame
            cv2.putText(img, f"Shoulder Taps: {tap_count}", (50, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Shoulder Tap Counter', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"

@app.route('/dumbbell_alternate_side_press',methods=['GET','POST'])
def dumbbell_alternate_side_press_counter():
    # Initialize MediaPipe Pose with higher confidence thresholds
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.7)

    # Initialize MediaPipe drawing utilities
    mp_drawing = mp.solutions.drawing_utils

    # Initialize webcam capture
    cap = cv2.VideoCapture(0)  # Change to 0 for default webcam
    press_counter = 0
    prev_raised_arm = None

    if not cap.isOpened():
        return "Error: Cannot open webcam."

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extracting landmark points
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            # Check for Dumbbell Alternate Side Press pose with higher confidence thresholds
            left_elbow_confidence = results.pose_landmarks.landmark[15].visibility
            right_elbow_confidence = results.pose_landmarks.landmark[16].visibility
            left_shoulder_confidence = results.pose_landmarks.landmark[11].visibility
            right_shoulder_confidence = results.pose_landmarks.landmark[12].visibility

            if (left_elbow_confidence > 0.7 and right_elbow_confidence > 0.7 and
                left_shoulder_confidence > 0.7 and right_shoulder_confidence > 0.7):
                left_elbow_y = points[15][1]
                right_elbow_y = points[16][1]
                left_shoulder_y = points[11][1]
                right_shoulder_y = points[12][1]

                # Check if elbows are lower than shoulders and at least one arm is raised above the other
                if (left_elbow_y < left_shoulder_y and right_elbow_y > right_shoulder_y) or \
                   (left_elbow_y > left_shoulder_y and right_elbow_y < right_shoulder_y):
                    # Identify which arm is raised higher
                    raised_arm = "left" if left_elbow_y < right_elbow_y else "right"

                    # Check if the raised arm is different from the previously raised arm
                    if prev_raised_arm != raised_arm:
                        # Check if elbows are extended and straight
                        def calculate_angle(a, b, c):
                            radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
                            angle = abs(radians * 180.0 / math.pi)
                            return angle

                        left_elbow_angle = calculate_angle(points[11], points[13], points[15])
                        right_elbow_angle = calculate_angle(points[12], points[14], points[16])

                        if (raised_arm == "left" and left_elbow_angle > 160) or \
                           (raised_arm == "right" and right_elbow_angle > 160):
                            press_counter += 1
                            prev_raised_arm = raised_arm
                            print("Dumbbell Alternate Side Press")

            else:
                prev_raised_arm = None

            # Display pose counter on the frame
            cv2.putText(img, f"Dumbbell Alternate Side Press: {press_counter}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Webcam Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"


@app.route('/push-up',methods=['GET','POST'])
def pushup_counter():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        angle = abs(radians * 180.0 / math.pi)
        return angle

    # Initialize MediaPipe Pose with higher confidence thresholds
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize video capture
    cap = cv2.VideoCapture("Push-up.mp4")
    if not cap.isOpened():
        return "Error: Cannot open video file."

    pushup_count = 0
    pushup_detected = False

    while True:
        success, img = cap.read()
        if not success:
            print("Error reading frame.")
            break

        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract key landmark points
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Calculate angles
            left_angle = calculate_angle([left_elbow.x, left_elbow.y], [left_shoulder.x, left_shoulder.y],
                                         [left_wrist.x, left_wrist.y])
            right_angle = calculate_angle([right_elbow.x, right_elbow.y], [right_shoulder.x, right_shoulder.y],
                                          [right_wrist.x, right_wrist.y])

            # Check for push-up movement
            if left_angle > 160 and right_angle > 160:
                if not pushup_detected:
                    pushup_count += 1
                    pushup_detected = True
                    print("Push-up Counted")
            else:
                pushup_detected = False

            # Display push-up counter on the frame
            cv2.putText(img, f"Push-ups: {pushup_count}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Push-up Counter', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Video playback completed"

@app.route('/jump_squat',methods=['GET','POST'])
def jump_squat_counter():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Initialize MediaPipe Pose with higher confidence thresholds
    pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.7)

    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    squat_counter = 0
    squat_down = False

    if not cap.isOpened():
        return "Error: Cannot open webcam."

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extracting landmark points
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            # Check for jump squat pose
            left_knee_confidence = results.pose_landmarks.landmark[26].visibility
            right_knee_confidence = results.pose_landmarks.landmark[25].visibility
            left_hip_confidence = results.pose_landmarks.landmark[23].visibility
            right_hip_confidence = results.pose_landmarks.landmark[24].visibility

            if (left_knee_confidence > 0.7 and right_knee_confidence > 0.7 and
                    left_hip_confidence > 0.7 and right_hip_confidence > 0.7):
                left_knee_y = points[26][1]
                right_knee_y = points[25][1]
                left_hip_y = points[23][1]
                right_hip_y = points[24][1]

                # Check if knees are lower than hips and person is squatting down
                if (left_knee_y > left_hip_y and right_knee_y > right_hip_y) and not squat_down:
                    print("Squat Down")
                    squat_down = True
                elif (left_knee_y < left_hip_y and right_knee_y < right_hip_y) and squat_down:
                    print("Stand Up")
                    squat_down = False
                    squat_counter += 1
                    print("Squat Count:", squat_counter)

            # Display squat counter on the frame
            cv2.putText(img, f"Jump Squats: {squat_counter}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the frame in a window
        cv2.imshow('Webcam Feed', img)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Webcam feed closed"


if __name__ == '__main__':
    app.run(debug=True)
