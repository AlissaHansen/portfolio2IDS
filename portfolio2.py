import cv2
import pyautogui
import mediapipe as mp
import time
import datetime

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
pyautogui.PAUSE = 0
TimesDrawn = 0
startTimer = True

My_file = open('test.txt', 'a')

# Webcam input:
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():

    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if startTimer:
        timeStart = time.time()
        startTimer = False
    
     #Print handedness and draw hand landmarks on the image.
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      intIndexFingerTipX = int((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width))
      intIndexFingerTipY = int((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height))
      intIndexFingerTipZRounded = round((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z), 2)

      pyautogui.moveTo(intIndexFingerTipX, intIndexFingerTipY)

      if intIndexFingerTipZRounded > -0.13:
        pyautogui.dragTo(intIndexFingerTipX, intIndexFingerTipY, button='left')
        TimesDrawn += 1

      #print (intIndexFingerTip)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

timeElapsedSeconds = round(time.time() - timeStart)

totalTimeElapsed = str(datetime.timedelta(seconds=timeElapsedSeconds))

My_file.write (f'Du har tegnet {TimesDrawn} gange. Total tid programmet var åbent: {totalTimeElapsed} \n')
My_file.close()
cap.release()
cv2.destroyAllWindows()