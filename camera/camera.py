import numpy as np
import cv2

#cap = cv2.VideoCapture("udpsrc port=1234 ! videoconvert ! appsink")
print "start camera"
cap = cv2.VideoCapture('udpsrc port=1234 ! "application/x-rtp, payload=127" ! rtph264depay ! ffdec_h264 ! ffmpegcolorspace ! video/x-raw ! appsink')
#cap = cv2.VideoCapture('udpsrc port=1234 ! "application/x-rtp, payload=127" ! appsink')
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