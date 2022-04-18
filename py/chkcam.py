import cv2
import sys
import argparse
import json
import imutils
print(cv2.__version__)

ptx1,pty1= -1,-1
ptx2,pty2= -1,-1
ptx3,pty3= -1,-1
ptx4,pty4= -1,-1
nc = 0
nc1 = 0

def prcsimg1( cid, rot, file ) :

 vidCap = cv2.VideoCapture(int(cid))

 if not vidCap.isOpened():
    print('Unable to open: ')
    exit(0)

 ret, frame1 = vidCap.read()
 if not ret : 
    exit(0)

 (rows, cols) = frame1.shape[:2]
 M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
 frame1 = cv2.warpAffine(frame1, M, (cols, rows))


 with open( file, 'r' ) as f :
   fr=list(f)
 while vidCap.isOpened():
   ret, frame2 = vidCap.read()
   if not ret : 
      break

   (rows, cols) = frame2.shape[:2]
   M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
   frame2 = cv2.warpAffine(frame2, M, (cols, rows))
   frame = frame2.copy()
   fgMask = cv2.absdiff(frame1,frame2)
   fgMask = cv2.cvtColor(fgMask,cv2.COLOR_BGR2GRAY)
  
   fgMask = 255-fgMask

   _,thresh = cv2.threshold(fgMask,225,255,cv2.THRESH_BINARY)
 
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
      if x > sx and x+w < sx+sw :
            if y > sy and y < sy+sh :
              OK=True
            else :
              if y < sy and y+h > sy :
                OK=True
      if not OK :    
            if y > sy and y+h < sy+sh :
               if x > sx and x < sx+sw :
                 OK=True
               else :
                 if x < sx and x+w > sx :
                   OK=True
      if OK :
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)   
        print('Object Found Area -- ', fjd["area"], ' -- Countour Area -- ', ca)
      else :
        print('Object Not Found Area --', fjd["area"], ' -- Countour Area -- ', ca)

    i+=1

   cv2.imshow("Rotated by " +  rot + " Degrees", frame)

   if cv2.waitKey(1) & 0xFF==ord('q'):
        break

 cv2.destroyAllWindows()
 vidCap.release()



def click(event, x, y, flags, param):
 global ptx1,pty1
 global ptx2,pty2
 global ptx3,pty3
 global ptx4,pty4
 global nc
 global nc1
 if event == cv2.EVENT_LBUTTONDBLCLK:
    ptx1,pty1 = x,y
 if event == cv2.EVENT_RBUTTONDBLCLK:
    ptx2,pty2 = x,y
 if event == cv2.EVENT_LBUTTONDOWN:
    ptx3,pty3 = x,y
    ptx4 = pty4 = -1
    nc = 1

 if event == cv2.EVENT_LBUTTONUP:
    ptx4,pty4 = x,y
    nc1 = 1
 if event == cv2.EVENT_MOUSEMOVE:
    if (bool)(nc) :
      ptx4,pty4 = x,y
  
def prcsimg2(cid, rot ) :
 global ptx1, pty1
 global ptx2, pty2
 global ptx3, pty3
 global ptx4, pty4
 global nc, nc1
 vidCap = cv2.VideoCapture(int(cid))
 if not vidCap.isOpened():
    print('Unable to open: ')
    exit(0)

 cv2.namedWindow('image')
 cv2.setMouseCallback("image", click)

 while vidCap.isOpened():
   ret, frame2 = vidCap.read()
   if not ret : 
      break
   
   (rows, cols) = frame2.shape[:2]
   M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
   rotated = cv2.warpAffine(frame2, M, (cols, rows))

   if ( ptx1 !=-1 and pty1 !=-1 ) :
          h, w, c = rotated.shape
          thickness = 2
          line_type = 8
          cv2.line(rotated,
             (ptx1,0),
             (ptx1,h),
             (0, 255, 0),
             thickness,
             line_type )
   if ( ptx2 !=-1 and pty2 !=-1 ) :
          h, w, c = rotated.shape
          thickness = 2
          line_type = 8
          cv2.line(rotated,(0,pty2),(w,pty2),(0, 255, 0),thickness,line_type)

   if ( ptx3 !=-1 and pty3 !=-1 ) :
          h, w, c = rotated.shape
          thickness = 1
          line_type = 8


   if ( ptx4 !=-1 and pty4 !=-1 ) :
          thickness = 1
          line_type = 8
          cv2.rectangle(rotated,(ptx3,pty3),(ptx4,pty4),(0, 255, 0),thickness,line_type )
          if ((bool)(nc1)) :
             print ( '******* Rectangle **********')
             print('Clicked coordinates: (', ptx3, ',',pty3, ')', '   (', ptx4,',', pty4, ')' )
             print('Rectangle Coordinates : x : ', ptx3, ' y : ', pty3, ' width : ', ptx4 - ptx3, ' Height : ', pty4 - pty3 )
             nc1 = 0 
             nc = 0
   
   cv2.imshow("image", rotated)

   if cv2.waitKey(1) & 0xFF==ord('q'):
        break

 cv2.destroyAllWindows()
 vidCap.release()

def main() :
  n = len(sys.argv)
  if ( n == 4 ) :  
   prcsimg1(sys.argv[1],sys.argv[2], sys.argv[3])
  else :
   if ( n == 3 ) :
     prcsimg2(sys.argv[1],sys.argv[2])
   else :
      print( 'arg 1 - camid, arg 2 - rotation, arg 3 - file' )  

if __name__ == "__main__":
    main()