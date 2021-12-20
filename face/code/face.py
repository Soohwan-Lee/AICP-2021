"""
   *Face Tracking System Using Arduino - Python Code*
    Close the Arduino IDE before running this code to avoid Serial conflicts.
    Replace 'COM5' with the name of port where you arduino is connected.
    To find the port check Arduino IDE >> Tools >> port.
    Upload the Arduino code before executing this code.

    # Code by Harsh Dethe, 09 Sep 2018 #
"""
import numpy as np
import serial
import time
import sys
import cv2
import imutils

arduino = serial.Serial('COM6', 9600, timeout=.1)
time.sleep(2)
print("Connection to arduino...")


face_cascade = cv2.CascadeClassifier('./face/code/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(2)
# cap.set(3, 500)
# cap.set(4, 500)
# cap = cv2.resize(cap,(500,500), 0.5, 0.5, interpolation)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(height)

while 1:
    ret, img = cap.read()
    # img = imutils.resize(img, width=600, height =450)
    img = cv2.flip(img, 1)

    # cv2.resizeWindow(img, 500,500)
    cv2.line(img,(640,240),(0,240),(0,255,0),1)
    cv2.line(img,(320,0),(320,480),(0,255,0),1)
    cv2.circle(img, (320, 240), 5, (255, 255, 255), -1)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
        roi_gray  = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        arr = {y:y+h, x:x+w}
        print (arr)
        
        print ('X :' +str(x))
        print ('Y :'+str(y))
        print ('x+w :' +str(x+w))
        print ('y+h :' +str(y+h))

        xx = int(x+(x+h))/2
        yy = int(y+(y+w))/2

        print (xx)
        print (yy)

        center = (xx,yy)

        print("Center of Rectangle is :", center)
        data = "X{0:d}Y{1:d}Z".format(int(xx), int(yy))
        print ("output = '" +data+ "'")
        arduino.write(data.encode())
    

    cv2.imshow('img',img)
   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break