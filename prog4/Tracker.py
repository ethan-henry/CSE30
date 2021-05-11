# -*- coding: utf-8 -*-
"""
Created on Thu May 25 02:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Fahim
"""

import cv2
import numpy as np
import math

cap = cv2.VideoCapture('Sample2.webm')
#cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

boxes = []

count = 1
path = []
time = 0
frame_height =int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
possible = False

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # cv2.imshow("dil", dilated)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cascade1 = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    cascade2 = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    cascade3 = cv2.CascadeClassifier('haarcascade_lowerbody.xml')
    rects = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        sub_img = frame1[y:y + h, x:x + w]
        boxes.append(sub_img)
        # cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.imshow("sub", sub_img)
        # cv2.waitKey(300)
        # cv2.destroyWindow("sub")
        gray1 = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray1)
        body1 = cascade1.detectMultiScale(gray1, 1.1, 1)
        x1 = x
        y1 = y
        w1 = w
        h1 = h
        path.append([(int(x1 + (w1 / 2)), int(y1 + (h1 / 2))), time])
        for (x, y, w, h) in body1:
            cv2.rectangle(frame1, (x1 + x, y1 + y), (x1 + w + x, y1 + h + y), (0, 255, 0), 2)
            count += 1


        x = x1
        y = y1
        w = w1
        h = h1
        # for (x, y, w, h) in body2:
        #     cv2.rectangle(frame1, (x1 + x, y1 + y), (x1 + w + x, y1 + h + y), (0, 255, 0), 2)
        #     count += 1
        # #     print("GOT ONE!")
        # #     count += 1
        # #
        # for (x, y, w, h) in body3:
        #     cv2.rectangle(frame1, (x1 + x, y1 + y), (x1 + w + x, y1 + h + y), (0, 255, 0), 2)
        #     count += 1
        #     print("GOT ONE!")
        #     count += 1
        # cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
        #             1, (0, 0, 255), 3)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        if (w >= 75 or h >= 150):
            possible = True
    if count > 1:
        cv2.putText(frame1, "Status: Not Following SD6", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif possible:
        cv2.putText(frame1, "Status: Probably Not Following SD6", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    else:
        cv2.putText(frame1, "Status: Following SD6", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    for i in path:
        cv2.circle(frame1, i[0], 3, (0, 255, 0), -1)
        if time - i[1] >= 25:
            path.remove(i)
    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("feed", image)
    frame1 = frame2
    time += 1
    ret, frame2 = cap.read()
    count = 0
    possible = False
    if cv2.waitKey(40) == 27 or not(ret):
        break

cap.release()
out.release()
cv2.destroyAllWindows()