import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
start_time = time.time()
last_click_time = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    print('outside', abs(index_y - thumb_y))
                    current_time = time.time()
                    if abs(index_y - thumb_y) < 50 and current_time - last_click_time > 1:
                        pyautogui.click()
                        last_click_time = current_time
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 250:
                        pyautogui.moveTo(index_x, index_y,)  # Tambahkan parameter duration untuk membuat gerakan lebih smooth
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
    start_time = end_time