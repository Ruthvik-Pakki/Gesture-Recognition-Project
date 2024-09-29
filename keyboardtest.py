import cv2
import mediapipe as mp
import pyautogui
import math

mp_hand_tracking = mp.solutions.hands
hand_detector = mp_hand_tracking.Hands()
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
video_feed = cv2.VideoCapture(0)

last_x, last_y = None, None
gesture_memory = []


def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def detect_gestures(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hand_tracking.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hand_tracking.HandLandmark.THUMB_TIP]
    pinky_base = hand_landmarks.landmark[mp_hand_tracking.HandLandmark.PINKY_MCP]

    global last_x, last_y
    curr_x, curr_y = int(index_finger_tip.x * screen_w), int(index_finger_tip.y * screen_h)
    gesture_detected = None

    if last_x is not None and last_y is not None:
        delta_x = curr_x - last_x
        delta_y = curr_y - last_y

        if abs(delta_x) > abs(delta_y):
            if delta_x > 50:
                gesture_detected = 'Swipe Right'
            elif delta_x < -50:
                gesture_detected = 'Swipe Left'
        else:
            if delta_y > 50:
                gesture_detected = 'Swipe Down'
            elif delta_y < -50:
                gesture_detected = 'Swipe Up'

    last_x, last_y = curr_x, curr_y

    pinch_dist = calculate_distance(index_finger_tip, thumb_tip)
    if pinch_dist < 0.05:
        gesture_detected = 'Pinch Zoom'

    if len(gesture_memory) > 10:
        avg_x = sum([p[0] for p in gesture_memory]) / len(gesture_memory)
        avg_y = sum([p[1] for p in gesture_memory]) / len(gesture_memory)
        radius_variation = max([math.sqrt((p[0] - avg_x) ** 2 + (p[1] - avg_y) ** 2) for p in gesture_memory])
        if radius_variation > 20:
            gesture_detected = 'Circle Gesture'
        gesture_memory.clear()

    gesture_memory.append((curr_x, curr_y))
    if len(gesture_memory) > 10:
        gesture_memory.pop(0)

    return gesture_detected


def execute_gesture_action(gesture):
    if gesture == 'Swipe Right':
        pyautogui.press('right')
    elif gesture == 'Swipe Left':
        pyautogui.press('left')
    elif gesture == 'Swipe Down':
        pyautogui.press('down')
    elif gesture == 'Swipe Up':
        pyautogui.press('up')
    elif gesture == 'Pinch Zoom':
        pyautogui.hotkey('ctrl', '+')
    elif gesture == 'Circle Gesture':
        pyautogui.press('volumeup')


while video_feed.isOpened():
    success, img_frame = video_feed.read()
    img_frame = cv2.flip(img_frame, 1)
    rgb_img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGB)
    hand_data = hand_detector.process(rgb_img_frame)

    if hand_data.multi_hand_landmarks:
        for hand_landmarks in hand_data.multi_hand_landmarks:
            mp_draw.draw_landmarks(img_frame, hand_landmarks, mp_hand_tracking.HAND_CONNECTIONS)

            gesture = detect_gestures(hand_landmarks)
            if gesture:
                execute_gesture_action(gesture)

    cv2.imshow("Gesture Recognition", img_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video_feed.release()
cv2.destroyAllWindows()
