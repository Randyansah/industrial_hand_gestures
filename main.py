import cv2 as cv
import mediapipe as pipe
import time
import Engine as Eg
 

time.sleep(2.0)

pipe_draw=pipe.solutions.drawing_utils
pipe_hand=pipe.solutions.hands


tipIds=[4,8,12,16,20]

video=cv.VideoCapture(0)

with pipe_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5,max_num_hands=1) as hands:
    while True:
        ret,image=video.read()
        image=cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv.cvtColor(image, cv.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                pipe_draw.draw_landmarks(image, hand_landmark, pipe_hand.HAND_CONNECTIONS,
                pipe_draw.DrawingSpec(color=(121,22,76),thickness=2,circle_radius=4),
                pipe_draw.DrawingSpec(color=(121,44,250),thickness=2,circle_radius=4),)
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            Eg.gesture_count(total)
            if total==0:
                cv.rectangle(image, (80, 10), (150, 100), (0, 0, 255), cv.FILLED)
                cv.putText(image, "", (45, 375), cv.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 3)
                cv.putText(image, "OFF STATE", (100, 80), cv.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 3)

            elif total==5:
                cv.rectangle(image, (80, 10), (150, 100), (0, 255, 0), cv.FILLED)
                cv.putText(image, "", (45, 375), cv.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 3)
                cv.putText(image, "ON STATE", (100, 80), cv.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 3)
        cv.imshow('Industrial Machines Hand Gesture control',image)
        k=cv.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv.destroyAllWindows()

