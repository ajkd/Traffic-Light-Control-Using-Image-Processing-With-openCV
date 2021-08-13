import numpy as np
import cv2 as cv2
import time
import json
import serial
import time

class video :

 def __init__( self, cr ) : 
     self.myd = {}
     self.wcam = {}

     x=cr["comps"]
     for k,v in x.items() :
       port= v[0]
       speed = int(v[1])
       to = int(v[2])
       sl = int(v[3])  
       self.myd[k]=serial.Serial(port,speed,timeout=to)
       time.sleep(sl)

 def onofftl(self,p):
   i=0
   while i < len(p) :
     ard = self.myd[p[i][0]]
     j=1 
     t=''
     while j < len(p[i]) :
       t = t + str(p[i][j][0]) + ',' + str(p[i][j][1]) + ',' + str(p[i][j][2]) + ',#' 
       j+=1
     t='#0#' + t + '\n'
     ard.write(t.encode('utf-8'))
     ard.flush()
     msgx=ard.read_until()
     if not msgx[0] == '#' :
       print( msgx.decode('utf-8') )
     i +=1
     
 def prcs( self, type, maxt, debug, parms ):
    if type[0]=='c':
      return self.prcsvideo( maxt, debug, parms )
    else :
      return self.prcssensor( maxt, debug, parms )
  
 def prcsvideo( self, maxt, debug, parms ):

    cam = parms["cam"]    
    camid = parms["camid"]
    camtype = parms["camtype"]
    viewcam = parms["viewcam"]
    rdelay = int(parms["rdelay"])
    rtime = int(parms["rtime"])
    oarea=parms["detectarea"]
    mincarea = int(parms["mincarea"]) 

    sx=int(oarea[0])
    sy=int(oarea[1])
    sw=int(oarea[2])
    sh=int(oarea[3]) 

    start_time = time.time()
    noc = 0 
    r=0

    cap = 0 
    frame1 = 0  
    try : 
      cap = self.wcam['cap' + camid]
      frame1 = self.wcam['frame' + camid]
    except KeyError :
      cap = cv2.VideoCapture(cam)
      ret, frame1 = cap.read()
      if not ret : 
        cap.release()
        cv2.destroyAllWindows()
        print ( '************* Error Reading Camera - ', cam )
        return r
      self.wcam['cap' + camid] = cap
      self.wcam[ 'frame' + camid ] = frame1
    
    while cap.isOpened()  :
      start_time1 = time.time()
      noc += 1
      nof = 0 
      OOK = False
      while (  time.time() - start_time1 < rtime ):
        ret, frame2 = cap.read()
        if not ret : 
          print ( '************* Error Reading Camera - ', cam )
          break

        nof += 1
        frame = frame2.copy()
        cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)
        fgMask = cv2.absdiff(frame1,frame2)
        fgMask = cv2.cvtColor(fgMask,cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(fgMask,50,255,cv2.THRESH_BINARY)
        
        conts,_=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for c in conts :
         if cv2.contourArea(c) < mincarea :
            continue
         x,y,w,h = cv2.boundingRect(c)
         if x > sx and x + w < sx+sw and y  > sy and y + h < sy+sh:
           cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
           OOK = True

        if viewcam > 0 :        
          cv2.imshow('cam - ' + str(cam), frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

        if OOK :
          if debug[0] == 'Y' :
             print('Cycle No - ', noc, '  Frame No - ', nof, ' Object Detected' )
          break
        else :  
          if debug[0] == 'Y' :
             print('Cycle No - ', noc, '  Frame No - ', nof, ' Object Not Detected' )
           
        time.sleep(rdelay)

      if OOK : 
         if time.time() - start_time > maxt :
            r=1
            break
      else :
        break

    if debug[0] == 'Y' :
      print ( 'Return From Camera "', cam, '" - "', r )
    return r

 def prcssensor( self, maxt, debug, parms ):
   sensor = parms["sensor"]
   sensorid = parms["sensorid"]
   rdelay = parms["rdelay"]
   rtime = parms["rtime"]
   srtm = parms["srtm"]
   comport = parms["comport"]
   ard=self.myd[comport]
   cc=0
   r=0
   start_time=time.time()
   while True :
     cc+=1
     sr = '#1#' + sensor + ',' + str(rdelay) + ',' + str(rtime) + ',' + str(srtm) + ',#\n'
     if debug[0] == 'Y' :
       print ( 'Get From Sensor - "', sensor, '" - Cycle ', cc, ' - ', sr )
     ard.write(sr.encode('utf-8'))
     ard.flush()
     msg=ard.read_until()
     if len(msg) > 0 :
       s=msg.decode('utf-8')
       if debug[0] == 'Y' :
         print ( 'Read From Sensor - "', sensor, '" - Cycle ', cc, ' - ', s )
       if s[0] == '#' :
         l = s[1:2]
         if l[0] == '0' :
           break
       else :
         if debug[0] == 'Y' :
           print ( 'Invalid Message Read From Sensor - '  + sensor )       
     else :
       if debug[0] == 'Y' :
         print ( 'No Data Read From Sensor - '  + sensor )

     if ( time.time() - start_time > maxt ):
       r=1
       break
   if debug[0] == 'Y' :
     print ( 'Return From Sensor "', sensor, '" - "', r )
   return r
 


