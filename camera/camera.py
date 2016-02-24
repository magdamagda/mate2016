import numpy as np
import cv2

#cap = cv2.VideoCapture("udpsrc port=1234 ! videoconvert ! appsink")
print "start camera"
cap = cv2.VideoCapture('udpsrc port=1234 ! capsfilter caps=video/x-raw,format=GRAY8 ! videoconvert ! appsink')
#cap = cv2.VideoCapture('udpsrc port=1234 ! "application/x-rtp, payload=127" ! video/x-raw-rgb ! appsink')
#cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    print "streaming"
    ret, frame = cap.read()
    print "captured"
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print "to grey"
    cv2.imshow('frame',frame)
    print "show"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print "end"