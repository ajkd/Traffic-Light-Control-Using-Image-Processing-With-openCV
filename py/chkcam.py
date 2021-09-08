import cv2
import argparse
import json
print(cv2.__version__)

parser = argparse.ArgumentParser(description='To Check Web Cam')  
parser.add_argument('cam', help='Cam No', default='1' )
parser.add_argument('file', help='Data File Name', default='cam.txt' )
args = parser.parse_args()

vidCap = cv2.VideoCapture(int(args.cam))


if not vidCap.isOpened():
    print('Unable to open: ')
    exit(0)

ret, frame1 = vidCap.read()


with open( args.file, 'r' ) as f :
  fr=list(f)

while vidCap.isOpened():
  ret, frame2 = vidCap.read()
  frame = frame2.copy()

  if not ret : 
      break
   
  fgMask = cv2.absdiff(frame1,frame2)

  fgMask = cv2.cvtColor(fgMask,cv2.COLOR_BGR2GRAY)
  _,thresh = cv2.threshold(fgMask,50,255,cv2.THRESH_BINARY)

  i=0
  while (i < len(fr) ) :
    fjd= json.loads(fr[i])
    sx=fjd["detectarea"][0]
    sy=fjd["detectarea"][1]
    sw=fjd["detectarea"][2]
    sh=fjd["detectarea"][3]
    mincarea=fjd["mincarea"]
    maxcarea=fjd["maxcarea"]
 
    cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(0,255,255),2)

    conts,_=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for c in conts :
      ca = cv2.contourArea(c)
      if ( mincarea > 0 and ca < mincarea ) or ( maxcarea > 0 and ca > maxcarea ) :
        continue

      x,y,w,h = cv2.boundingRect(c)
      OK=False
      if x > sx and x + w < sx + sw :
        OK=True

      if OK :
        OK=False
        if y > sy and y < sy + sh :
          OK=True
        else :
          if y < sy and y + h > sy :
            OK=True


      if OK :
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)   
        print('Object Found Area -- ', fjd["area"], ' -- Countour Area -- ', ca)
      else :
        print('Object Not Found Area --', fjd["area"], ' -- Countour Area -- ', ca)

    i+=1

  cv2.imshow('Original Video', frame)

  if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
vidCap.release()