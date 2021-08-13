## Smart Trafic Light Control System

### Objective
To control traffic lights efficiently based on traffic congestion. 

### How this Model works 
   Time sharing based but efficiency is achieved by adopting following 
   techniques
   - green light will be "on" only when vehicles presence on the lane.
   - add more time to lanes when high conjession occurs
   - periodical processing of traffic lanes ( less congested lanes )
             

[Detail Disscussion of this project](readme.pdf) 

<a href="https://www.youtube.com/watch?v=SNN4s4HEaW4&t=219s&ab_channel=ShraddhaTV" target="_blank"><img src="image.png" alt="IMAGE ALT TEXT HERE" width="340" height="180" border="10" /></a>

### Working Model
 - Application written in Python and runs in windows environment
 - Vehicle present in lanes is detected by sensors and web cams
 - Sensors are connected to Arduino board and Arduino board
   connected to application windows machine via serial port. Application
   will communicate with application running in Arduino to read sensor
   data. Application will determine presence of traffic by received values
   of Sensor data.
 - Web cams are directly connected to windows machine and images of
   vehicle movements on lanes are detected and processed by
   Python/OpenCV
 - LEDs are used as traffic lights which are connected to Arduino board
   and application communicates with Arduino to on/off LEDs 

### Requirements
   Model based on this System has been tested under following software/hardware environments  
   - Windows 10 home
   - Python 3.9.6
   - OpenCV 4.5
   - PySerial 3.5
   - Arduino components  
        - Arduino GUI 1.8.15  
        - Arduino UNO board  
        - TCRT 5000 reflective optical IR sensors  
        - LEDs - red, yellow and green for each lane  
        - Resistors 10k - 1, 220 - 1 for each sensor, 220 - 1 for each LED  
        - Breadboard, Jumper wires  
- Web Cams  

### To Run Application
- py videom.py sit1.txt
  System Initialization Table is passed as first parameter (sit1.txt)
- before starting the application
   - tfrcntl.ino Arduino file under “tfrcntl” folder must be uploaded to
     Arduino board using Arduino GUI
   - All sensors, web cams and LEDs must be checked

### System Tables
Configuration information is given to application using tables
which are JSON based data structures
#### System Initialization Table
This is the main table (sit1.tx) which specifies information of other tables  

    {  
    "videom":"videosm1.txt",  
    "videop":"videosp1.txt",  
    "tlc":"videotlc1.txt",  
    "comps":{"c1":["COM3",9600,5,2]}  
    }  
    videom - Lane Definition Table which defines sensor and web cam information  
    videop - Priority Assign Table which is used assign more time to when high congested occurs to lanes  
    tlc - Traffic Light Control table where traffic lights data are specified  
    comps - Arduino board info  
           c1 - board id, there can be more than one board connecting sensors and LEDs  
           COM3 - is the port this board connects to application running machine  
           9600 - baud rate, data transfer rate of application running machine serial port and Arduino board  
           5 - time out will occur if unable to connect with Arduino within this time period ( milliseconds )  
           2 - wait time to connect with Arduino ( milliseconds )  

#### Lane Definition Table
"videom" : "videosm1.txt"  
Four lanes are considered in this demonstrated model and two lanes are managed by sensors and two lanes are  
managed by web cams  

      { "lane":1, "type":"s", "prtyid":["lane1-1"], "maxt":5, "skipc":0, "debug":"Y",  
        "parms": { "sensor":"A0 "comport":"c1", "sensorid":"s1", "rdelay":1, "rtime":200, "srtm":150 } },  
      { "lane":2, "type":"c", "maxt":5, "skipc":0, "debug":"Y",  
        "parms": { "cam":0, "camid":"cam1", "camtype":" ", "detectarea":[360,230,200,250],  
        "mincarea":1500, "rdelay":0.1, "rtime":1, "viewcam":1 } }  
             
      lane - lane id  
      type - 's' for sensor manage lane 'c' for web cam manage lane  
      prtyid - for this lane is a priority lane i.e. more time will be allocated if concession occurs and  
      this info is defined in table specified in 'videop' parm of system initialization table.  
      maxt - maximum time allocated to lane in seconds  
      kipc - processing frequency, for example less congested lane can processed once in two cycle  
      debug - 'y' or 'n' if 'y' - application will print debug info on console  
      parms -  
         For Sensors
              sensor - Analog pin of the Arduino, sensor is connected to ex. A0  
              sensorid - not relevant  
              comport - Arduino board id this sensor is connected to which is defined in system  
                        initialization table  
              srtm - Min value read from sensor to determine traffic is present in the lane  
              rtime - Time in milliseconds sensor should be read continuesly to determine if traffic is  
                      presented in the lane  
              rdelay - Time in milliseconds to wait before beginning reading cycle from sensor again  
  
              Desirable values for srtm, rtime and rdelay can be found out by running chksensor.py  
              
         For Cams  
              cam - Number ex. 0,1,2.. Windows will assign a number to a cam  
              camid, camtype - Not relevant  
              detectarea - To determine traffic is presence, vehicle must be presence in this area of  
                           the lane. This is the coordinates ( x, y,width,height ) of cam view area  
                           application should detect vehicles  
              mincarea - To identify detected object as a vehicle and to drop other objects which may  
                         presence in the video image frame, area detected of an object must be higher  
                         than this value  
              rtime, rdelay - Same as specified in sensor but specified in seconds  
              viewcam - 1 to show video cam frames on the console  
              
              Desirable values for cam no, detectarea, mincarea, rtime and rdelay can be found out by  
              running chkcam.py.           
           
