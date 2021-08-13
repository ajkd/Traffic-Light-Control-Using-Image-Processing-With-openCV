import cv2
import argparse
print(cv2.__version__)

parser = argparse.ArgumentParser(description='To Check Web Cam')  
parser.add_argument('cam', help='Cam No', default='1' )
args = parser.parse_args()

vidCap = cv2.VideoCapture(int(args.cam))
vehicle=0

if not vidCap.isOpened():
    print('Unable to open: ')
    exit(0)

ret, frame1 = vidCap.read()

while vidCap.isOpened():
    ret, frame2 = vidCap.read()
    frame = frame2.copy()

    if not ret : 
      break
   
    fgMask = cv2.absdiff(frame1,frame2)

    fgMask = cv2.cvtColor(fgMask,cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(fgMask,50,255,cv2.THRESH_BINARY)


 #   sx=375
 #   sy=100
 #   sw=220
 #   sh=350

    sx=360
    sy=260
    sw=150
    sh=200 

    mincarea = 1400

    cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)


    conts,_=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for c in conts :
      if cv2.contourArea(c) < mincarea :
        continue

      x,y,w,h = cv2.boundingRect(c)
      if x > sx and x + w < sx+sw and y  > sy and y + h < sy+sh:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        print('found')
      else :
        print('***************** not found')

    cv2.imshow('Original Video', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
vidCap.release()