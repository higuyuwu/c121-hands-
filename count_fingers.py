import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.soluions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detecion_confidence = 0.8, min_tracking_confidence = 0.5)
tipIds = [4,8,12,16,20]

def countFingers(img,hand_landmarks,handNo = 0):
    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmarks
        fingers = []

        for tp_index in tipIds:
            finger_tip_y = landmarks[tp_index].y
            finger_bottom_y = landmarks[tp_index -2].y
            if tp_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    print("finger with id ",tp_index," is open ")
                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    print("finger with id ",tp_index,"is closed")
        
        totalFingers = fingers.count(1)
        text = f"fingers : {totalFingers}"
        cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

def drawHandLandmarks(img,hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(img,landmarks,mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image,1)
    results = hands.process(image)
    hand_landmarks = results.multi_hand_landmarks
    drawHandLandmarks(image,hand_landmarks)
    countFingers(image,hand_landmarks)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

