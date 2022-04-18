import cv2 as cv2
import numpy as np
import time
import json
import serial
import time

t_width = 30;
t_height = 30;
t_space = 50;
t_x = 0;
t_y = 15;
t_r = 10;
max_items = 5;
df = (0, 0, 0)
wbg = (220,220,220)
tbg = (128,128,128)
off = (169, 169, 169)
lc = { 'R':(0,0,255), 'Y':(0,255,255), 'G':(0,128,0) } 


class video :

 def __init__( self, cr ) : 

     self.myd = {}
     self.wcam = {}
     self.wcamarea = {}

     self.tmap = {}
     self.image = 0

     try :
       x=cr["comps"]
       for k,v in x.items() :
         port= v[0]
         speed = int(v[1])
         to = int(v[2])
         sl = int(v[3])  
         self.myd[k]=serial.Serial(port,speed,timeout=to)
         time.sleep(sl)
     except KeyError :
         pass

 def onofftl(self, p):
   i=0
   while i < len(p) :
     ard = self.myd[p[i][0]]
     j=1 
     t=''
     while j < len(p[i]) :
        k = 0
        while ( k < len(p[i][j]) ) :
          t = t + str(p[i][j][k]) + ','
          k+=1
        t = t + '#'
        j+=1 
     t='#0#' + t + '\n'
     ard.write(t.encode('utf-8'))
     ard.flush()
     msgx=ard.read_until()
     if not msgx[0] == '#' :
       print( 'ERROR - Invalid Message Read Traffic Light ON/OFF ', msgx.decode('utf-8') )
     i +=1
     
 def prcs( self, lane, type, maxt, debug, parms ):
    if type[0]=='c':
      return self.prcsvideo( lane, maxt, debug, parms )
    else :
      return self.prcssensor( lane, maxt, debug, parms )
  
 def prcsvideo( self, lane, maxt, debug, parms ):

    cam = parms["cam"]    
    camid = parms["camid"]
    camtype = parms["camtype"]
    viewcam = parms["viewcam"]
    rdelay = int(parms["rdelay"])
    rtime = int(parms["rtime"])
    oarea=parms["detectarea"]
    mincarea = int(parms["mincarea"]) 
    maxcarea = int(parms["maxcarea"]) 
    rot = int(parms["rotate"]) 

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
      if ( rot != 0 ) :
        (rows, cols) = frame1.shape[:2]
        M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
        frame1 = cv2.warpAffine(frame1, M, (cols, rows))
      try :
        darea = self.wcamarea[ 'l' + camid + str(lane) ]
      except KeyError :
        self.wcamarea[ 'l' + camid + str(lane) ] = oarea
    except KeyError :
      cap = cv2.VideoCapture(cam)
      ret, frame1 = cap.read()
      if not ret : 
        cap.release()
        cv2.destroyAllWindows()
        print ( 'ERROR - Reading Camera - ', camid )
        return r
      if ( rot != 0 ) :
        (rows, cols) = frame1.shape[:2]
        M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
        frame1 = cv2.warpAffine(frame1, M, (cols, rows))
      self.wcam['cap' + camid] = cap
      self.wcam[ 'frame' + camid ] = frame1
      self.wcamarea['l' + camid + str(lane) ] = oarea
   
    while cap.isOpened()  :
      start_time1 = time.time()
      noc += 1
      nof = 0
      OK=False 
      while (  time.time() - start_time1 < rtime ):
        ret, frame2 = cap.read()
        if not ret : 
          print ( '************* Error Reading Camera - ', cam )
          break

        if ( rot != 0 ) :
          (rows, cols) = frame2.shape[:2]
          M = cv2.getRotationMatrix2D(((cols-1)//2.0, (rows-1)//2.0), int(rot), 1.0)
          frame2 = cv2.warpAffine(frame2, M, (cols, rows))

        nof += 1
        frame = frame2.copy()

        search_key = 'l' + camid
        res = [val for key, val in self.wcamarea.items() if search_key in key]
        for darea in res :
          sx1=int(darea[0])
          sy1=int(darea[1])
          sw1=int(darea[2])
          sh1=int(darea[3])
          if oarea == darea : 
            cv2.rectangle(frame,(sx1,sy1),(sx1+sw1,sy1+sh1),(0,0,255),2)
          else :
            cv2.rectangle(frame,(sx1,sy1),(sx1+sw1,sy1+sh1),(0,255,255),2)

        fgMask = cv2.absdiff(frame1,frame2)
        fgMask = cv2.cvtColor(fgMask,cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(fgMask,50,255,cv2.THRESH_BINARY)
        
        conts,_=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for c in conts :
          ca = cv2.contourArea(c)
          if ( mincarea > 0 and ca < mincarea ) or ( maxcarea > 0 and ca > maxcarea ) :
            continue
          x,y,w,h = cv2.boundingRect(c)
          OOK = False
          if x > sx and x + w < sx + sw :
            if y > sy and y < sy + sh :
              OOK=True
            else :
              if y < sy and y + h > sy :
                OOK=True
          if OOK :
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            OK=True 

        if viewcam > 0 :        
          cv2.imshow('cam - ' + camid, frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

        if OK :
          if debug[0] == 'Y' :
             print('Cycle No - ', noc, '  Frame No - ', nof, ' Object/s Detected' )
          break
        else :  
          if debug[0] == 'Y' :
             print('Cycle No - ', noc, '  Frame No - ', nof, ' Object/s Not Detected' )
           
        time.sleep(rdelay)

      if OK : 
         if time.time() - start_time > maxt :
            r=1
            break
      else :
        break

    if viewcam > 0 :        
      ret, frame = cap.read()
      if ret : 
        search_key = 'l' + camid
        res = [val for key, val in self.wcamarea.items() if search_key in key]
        for darea in res :
          sx1=int(darea[0])
          sy1=int(darea[1])
          sw1=int(darea[2])
          sh1=int(darea[3])
          cv2.rectangle(frame,(sx1,sy1),(sx1+sw1,sy1+sh1),(0,255,255),2)
        cv2.imshow('cam - ' + camid, frame)
      else :
         print ( '************* Error Reading Camera - ', cam )


    if debug[0] == 'Y' :
      print ( 'Return From Camera "', cam, '" - "', r )

    return r

 def prcssensor( self, lane, maxt, debug, parms ):
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
         print ( 'ERROR - Invalid Message Read From Sensor - '  + sensor )       
     else :
       print ( 'ERROR - No Data Read From Sensor - '  + sensorid )

     if ( time.time() - start_time > maxt ):
       r=1
       break
   if debug[0] == 'Y' :
     print ( 'Return From Sensor "', sensor, '" - "', r )
   return r
 
 def createtl(self, tlr):
   o = ''
   l = len(tlr) * t_width * 3 + t_space * (len(tlr) + 1)
   self.image = np.zeros(( t_height * 2, l,3), np.uint8 )
   self.image[:,:] = wbg
   x = t_x
   for js in tlr :
     i = 0
     x += t_space
     cv2.putText(
          self.image,
          'Lane - ' + str(js[0]),
          (x, t_y - 5),
          cv2.FONT_HERSHEY_COMPLEX_SMALL,
          .6,
          (0, 0, 0), 1,
          cv2.LINE_AA, False)
     while (i < len(js[1])) :
       cv2.rectangle(self.image, (x, t_y), (x + t_width, t_y + t_height), tbg, -1)
       cv2.circle(self.image, (int(x + t_width / 2), int(t_y + t_height / 2)), t_r, off, -1, 2)
       lidr = js[1][i]
       ix = lidr.find('-')
       tlc = lidr[0:ix]
       ix+=1
       tlid = lidr[ix:len(lidr)]
       self.tmap['x#' + tlid] = int(x + t_width / 2)
       self.tmap['y#' + tlid] = int(t_y + t_height / 2)
       self.tmap['c#' + tlid] = tlc
       x += t_width
       i+=1
   cv2.imshow('Traffic Light Display Window', self.image)
   if cv2.waitKey(1) & 0xFF == ord('q'):
     return o
   return o

 def onoff(self, p) :
   o = ''  
   i=0
   while i < len(p) :
     j=1 
     while j < len(p[i]) :
        o = o + self.onoffl(p[i][j])
        j+=1 
     i +=1
   return o
 
 def onoffl(self, tlr) :
       o = ''
       j = 0
       s = ['']* max_items
       for el1 in tlr :
         if j == 1 :
           s[j] = tlr[j]
         else :
           s[j] = int(tlr[j])
         j+=1
       sx = 'x#' + str(s[0])
       sy = 'y#' + str(s[0])
       if (s[1][0] == 'O') :
           sc = self.tmap['c#' + str(s[0])]
           cv2.circle(self.image, ( self.tmap[sx], self.tmap[sy] ), t_r, lc[sc], -1, 2)
           cv2.imshow('Traffic Light Display Window', self.image)
           if cv2.waitKey(1) & 0xFF == ord('q'):
              return o 
           time.sleep(int(s[2])/1000)
       else : 
           if (s[1][0] == 'F') :
             cv2.circle(self.image, ( self.tmap[sx], self.tmap[sy] ), t_r, off, -1, 2)
             cv2.imshow('Traffic Light Display Window', self.image)
             if cv2.waitKey(1) & 0xFF == ord('q'):
               return o 
             time.sleep(int(s[2])/1000)
           else :
             if (s[1][0] == 'B') :
               st1 = time.time()
               sc = self.tmap["c#" + str(s[0])]
               while (True) :
                 cv2.circle(self.image, ( self.tmap[sx], self.tmap[sy] ), t_r, lc[sc], -1, 2)
                 cv2. imshow("Traffic Light Display Window", self.image)
                 if cv2.waitKey(1) & 0xFF == ord('q'):
                   return o 
                 time.sleep(int(s[3])/1000)
                 cv2.circle(self.image, ( self.tmap[sx], self.tmap[sy] ), t_r, off, -1, 2)
                 cv2.imshow('Traffic Light Display Window', self.image)
                 if cv2.waitKey(1) & 0xFF == ord('q'):
                   return o 
                 time.sleep(int(s[3])/1000)
                 st3 = time.time()
                 if ( (st3 - st1) * 1000 > s[4] ) :
                   return o
                 time.sleep(int(s[2]))
             else :
               o = '#Invalid Function Code'
       return o