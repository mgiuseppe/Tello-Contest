from djitellopy import Tello
import cv2
import numpy as np

def getBoundingRect(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            perimeter = cv2.arcLength(cnt, True)
            corners = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            x,y,w,h = cv2.boundingRect(corners)
    return x,y,w,h

tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
tello.send_rc_control(0,0,0,0)
original_w = 0
while True:
    img = frame_read.frame
    
    # create color mask
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, np.array([50,60,0]), np.array([80,150,255]))
    # find object and center
    x,y,w,h = getBoundingRect(mask)
    objectCenter = (x + int(w/2), y + int(h/2))
    imgCenter = (int(img.shape[1]/2), int(img.shape[0]/2))

    if (original_w == 0 or w == 0): # set the original_w if it has never been and reset if target has been lost  
        original_w = w


    # compute object distance from image center
    death_zone = 100
    x_diff = objectCenter[0] - imgCenter[0]
    y_diff = objectCenter[1] - imgCenter[1]
    # compute up_down and yaw
    up_down = 20 + int(20 / 360 * abs(y_diff)) if abs(y_diff) > death_zone else 0  # speed
    up_down = up_down if y_diff < 0 else -up_down # sign: go up if less than zero 
    yaw = 20 + int(20 / 540 * abs(x_diff)) if abs(x_diff) > death_zone else 0 # speed
    yaw = -yaw if x_diff < 0 else yaw # sign: go left if less than zero
    # compute forward_back
    w_death_zone = 10
    w_diff = original_w - w
    forward_back = 10 + int(10 / 720 * abs(w_diff)) if abs(w_diff) > w_death_zone else 0 # speed
    forward_back = -forward_back if w_diff < 0 else forward_back # sign: go back if less than zero

    # draw lines and move tello
    if (objectCenter != (0,0)):
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
        cv2.circle(img, objectCenter, 2, (0,0,255), cv2.FILLED)
        cv2.line(img, imgCenter, objectCenter, (0,0,255) if abs(x_diff) > 300 or abs(y_diff) > 200 else (0,255,0))
        tello.send_rc_control(0,forward_back,up_down,yaw)
    else:
        tello.send_rc_control(0,0,0,0)

    # add text and show img
    cv2.putText(img, f"obj: {objectCenter}", (0,100), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"img: {imgCenter}", (0,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"dy: {y_diff}", (0,200), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"dx: {x_diff}", (0,250), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"original_w: {original_w}", (0,300), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"w: {w}", (0,350), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    cv2.putText(img, f"Battery: {tello.get_battery()}", (0,600), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
    cv2.putText(img, f"Temp: {tello.get_temperature()}", (0,650), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
    cv2.imshow("drone", img)
    if(cv2.waitKey(33) & 0xFF ==27):
        break;

tello.send_rc_control(0,0,0,0)
tello.land()