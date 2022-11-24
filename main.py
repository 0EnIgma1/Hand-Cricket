import cv2
import random 
import cvzone
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

StateResult = False
BatStart = False
BowlStart = False
count = 0
player_score = 0
ai_score = 0
score = 0
winner = 0
# winner = 1 if ai won
# winner = 2 if human won
cap = cv2.VideoCapture(0)
buttons = True
turn_count = 0

cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands = 1)

def count_fingers(x):
    count = 0
    if x == [1,0,0,0,0]:
        count = 6
    else:
        for i in range(0,len(x)):
            if x[i] == 1:
                count += 1
    return count

def AIrun():
    ailist = [1,2,3,4,5,6]
    AIchoice = random.choice(ailist)
    return AIchoice

def batting(player_score,airun):
    out_score = 0
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        count = count_fingers(fingers)
        #airun = AIrun()
        if count == airun:
            print("out")
            out_score = 1
            return player_score, out_score
        elif count==1:
            player_score +=1
            print("1 run")

            print("**********")
        elif count==2:
            player_score +=2
            print("2 run")

            print("**********")
        elif count==3:
            player_score +=3
            print("3 run")

            print("**********")
        elif count==4:
            player_score +=4
            print("4 run")

            print("**********")
        elif count==5:
            player_score +=5
            print("5 run")

            print("**********")
        elif count==6:
            player_score +=6
            print("6 run")
 
            print("**********")
        else:
            print("No player_score")
            print("**********")

        print(f"Total runs: {player_score}")
    return player_score, out_score

def bowling(airun,player_score):
    out_score = 0
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        count = count_fingers(fingers)
        #airun = AIrun()
        if count == airun:
            print("out")
            out_score = 1
            return player_score, out_score
        elif airun==1:
            player_score +=1
            print("1 run")

            print("**********")
        elif airun==2:
            player_score +=2
            print("2 run")

            print("**********")
        elif airun==3:
            player_score +=3
            print("3 run")

            print("**********")
        elif airun==4:
            player_score +=4
            print("4 run")

            print("**********")
        elif airun==5:
            player_score +=5
            print("5 run")

            print("**********")
        elif airun==6:
            player_score +=6
            print("6 run")
 
            print("**********")
        else:
            print("No player_score")
            print("**********")

        print(f"Total runs: {player_score}")
    return player_score, out_score


#print(rand)
imgAI = cv2.imread("giga_chad1.png",cv2.IMREAD_UNCHANGED)

out_score = 0
while True:
    #imgAI = cv2.imread(f"{rand}.png",cv2.IMREAD_UNCHANGED)
    imgBG = cv2.imread("hc_bg1.png")
    success, img = cap.read()
    #cv2.imshow("test",img)
    rand = random.randint(1,6)
    imgScale = cv2.resize(img,(0,0),None,0.814,0.814)
    imgScale = imgScale[:,89:429]
    hands, img = detector.findHands(imgScale)

    if BatStart:
        if StateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(617,405),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)     #dimension, font, size, color, thickness

            if timer>2:
                StateResult = True
                timer = 0
                airun = AIrun()
                player_score, out_score = batting(player_score,airun)
                imgAI = cv2.imread(f"{airun}.png",cv2.IMREAD_UNCHANGED)

                if out_score==1:
                    BatStart = False
                    buttons = True
                    turn_count += 1
                if turn_count == 2:
                    winner = 1
                initialTime = time.time()
                if ai_score != 0 and player_score > ai_score:
                    winner = 2
                    BatStart = False
     
    if BowlStart:
        if StateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(617,405),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)     #dimension, font, size, color, thickness

            if timer>2:
                StateResult = True
                timer = 0
                airun = AIrun()
                ai_score, out_score = bowling(airun, ai_score)
                imgAI = cv2.imread(f"{airun}.png",cv2.IMREAD_UNCHANGED)

                if out_score==1:
                    BowlStart = False
                    buttons = True
                    turn_count += 1
                if turn_count == 2:
                    winner = 2
                initialTime = time.time()
                if player_score != 0 and ai_score > player_score:
                    winner = 1
                    BowlStart = False
                    
    imgBG[225:616,797:1137] = imgScale
      
    imgBG = cvzone.overlayPNG(imgBG,imgAI,(155,260))

    if buttons==True and turn_count!=2:
        cv2.putText(imgBG, "Press S to BAT", (200,700),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        cv2.putText(imgBG, "Press B to BOWL", (700,700),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

    if out_score==1:
        cv2.putText(imgBG,f"! OUT !",(550,200),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5)
    
    cv2.putText(imgBG,f"{player_score}",(1045,200),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)
    cv2.putText(imgBG,f"{ai_score}",(390,200),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)

    cv2.putText(imgBG, "QUIT - Esc", (1100,700),cv2.FONT_HERSHEY_PLAIN,1.5,(255,255,255),2)

    if winner == 1:
        cv2.putText(imgBG,"AI won !",(550,700),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5)
    elif winner == 2:
        cv2.putText(imgBG,f"Human won !",(495,700),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5)

    cv2.imshow("bg",imgBG)
    StateResult = False

    key = cv2.waitKey(1)
    if key == ord("s"):
        out_score = 0
        BatStart = True
        initialTime = time.time()
        StateResult = False
        buttons = False

    if key == ord("b"):
        out_score = 0
        BowlStart = True
        initialTime = time.time()
        StateResult = False
        buttons = False
        
    if key & 0xFF == 27 :
        break
cv2.destroyAllWindows()