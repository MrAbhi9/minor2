import cv2
import mediapipe as mp      # to detect the landmarks
import pyautogui            # to connect keyboard and the gestures
import time                 # was unable to detect , it counted 1,2,3 before even 5 finger o multiple outcome were there 

def count_fingers(lst):     # landmark k hisab se finger count kr lenge fir uske hisab se play/pause vgera jo bhi krna h vo kr denge 
    cnt = 0

    thresh = (lst.landmark[0].y*100  - lst.landmark[9].y*100)/2       #landmark 0-9 ki value ki half value store kr lia thresh me or 100 se multiply sab jgh kra denge taki bada digit dikhe or calculation me asani ho 

    #for any one finger 
    if(lst.landmark[5].y*100  - lst.landmark[8].y*100 ) > thresh:
        cnt+=1
    
    #for two finger
    if(lst.landmark[9].y*100  - lst.landmark[12].y*100 ) > thresh:
        cnt+=1

    if(lst.landmark[13].y*100  - lst.landmark[16].y*100 ) > thresh:
        cnt+=1

    if(lst.landmark[17].y*100  - lst.landmark[20].y*100 ) > thresh:
        cnt+=1

    #for thumb we have done it in x axis
    if(lst.landmark[5].x*100  - lst.landmark[4].x*100 ) > 5:
        cnt+=1
    return cnt

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

prev = -1   #to limit the cnt else whatever it finds true ,will occur infinite number of time 
start_init = False        #abhi start nhi hua finger aana

while True:
    end_time = time.time()      #end time 
    _, frm = cap.read()
    frm =cv2.flip(frm, 1)   #flip the camera outcome 

    res = hand_obj.process(cv2.cvtColor(frm,cv2.COLOR_BGR2RGB))    #Open cv2 reads in rgb format we have read in bgr format
   
    if res.multi_hand_landmarks:   #If number of hands> 0 
        
        hand_keyPoints = res.multi_hand_landmarks[0]
       
        cnt = count_fingers(hand_keyPoints)

        if not(prev == cnt):
            if not(start_init):
                start_time = time.time()        # start hone ka time note kiya, add krte gye 
                start_init = True
            elif (end_time-start_time) > 0.2:   #end k time or start time k bich ka antar , taaki multiple na count krle 
                if (cnt == 1):
                    pyautogui.press("up")
                elif (cnt == 2):
                    pyautogui.press("down")
                elif (cnt == 3):
                    pyautogui.press("left")
                elif (cnt == 4):
                    pyautogui.press("right")
                elif (cnt == 5):
                    pyautogui.press("space")

                prev=cnt
                start_init=False
        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)     # isse basically red point aaega or vo connected rahega 
    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
