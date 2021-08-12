## Smart Trafic Light Control System

### Objective :
   ffff
  To control traffic lights efficiently based on traffic congestion.
How it works
Time sharing based but efficiency is achieved by considering the following 
techniques
-green light will be "on" only when vehicles are in the lane.
-add more time to lanes when high conjession occurs
-periodical processing of traffic lanes 
Working Model
-Application written in Python and running in the Windows environment -Vehicle presence in lanes is detected by sensors and web cams
-Sensors are connected to the Arduino board and the Arduino board is connected to
application windows machine via serial port. Application will 
The Arduino communicates with an application running on the Arduino to read sensor data.
The application will determine the presence of traffic by receiving values of 
sensor data.
-Web cams are directly connected to windows machines and show images of 
Vehicle movements in lanes are detected and processed by Python/OpenCV
-LEDs are used as traffic lights which are connected to an arduio board and 
The application communicates with Arduino to on/off LEDs.
-
Requirements
A model based on this system has been tested under the following conditions.
Windows 10 home
-Python 3.9.6
-OpenCV 4.5.2
-PySerial 3.5
-Arduino components
Arduino GUI 1.8.15 Arduino UNO board
TCRT 5000 reflective opticle IR sensors 
LEDs-red, yellow and green for each lane.
Resistors 10k-1, 220-1 for each sensor 
220-1 for each LED
Breadboard, Jumper wires,
-Web Cams 
Run Application
-py videom.py sit1.txt
The System Initualization Table is passed as the first parameter (sit1.txt).
before starting the application.
-tfrcntl.ino arudino file under the tfrcntl folder must be uploaded to 
Arduino board using Arduino GUI 
-All sensors, web cams, and LEDs must be checked.
System Tables
Configuration information is given to the application using tables.
which are JSON based data structures.
  
System Initialization Table
This is the main table (sit1.tx) which specifies information about other 
tables
 
"videom": "videosm1.txt",
"videop": "videosp1.txt",
"tlc": "videotlc1.txt",
"comps": "c1": ["COM3", 9600,5,2]
 
videom-Lane definition table which defines sensor and web cam 
information
videop-Priority Assign Table, which is used to assign more time to lanes 
When high congestion occurs in lanes,
tlc-Traffic Light Control table where traffic light data is
specified
comps-Arduino board info
c1-board id. There can be more than one board connected
sensors and LEDs
COM3-is the port this board connects to the application 
running machine
9600-baud rate, data transfer rate of application 
running machine serial port and Arduino board
A 5-time out will occur if you are unable to connect with 
Arduino within this time period (miliseconds) 2-wait time to connect with arudino (miliseconds)
Lane Definition Table
"videom": "videosm1.txt" 
Four lanes are considered in this demonstrated model.
and two lanes are managed by sensors and two lanes are 
managed by web cams
"lane": 1, "type": "s", "prtyid": ["lane1-1"], "maxt": 5, 
"skipc": 0, "debug": "Y", "parms": "A0", 
"comport": "c1", "sensorid": "s1", "rdelay": 1, "rtime": 200, 
"srtm": 150,
"lane": 2, "type": "c", "maxt": 5, "skipc": 0, "debug": "Y", 
. "parms": "cam": 0, "camid": "cam1", "camtype": "", 
"detectarea": [360,230,200,250], "mincarea": 1500, 
"rdelay": 0.1, "rtime": 1, "viewcam": 1
lane-lane id 
's' for sensor managed lane, 'c' for web cam managed lane
This lane is a priority lane, i.e. more time will be 
Congestion occurs and this info is defined in 
table specified in the 'videop' parm of system initialization 
table
maxt-maximum time allocated to lane in seconds
skipc-processing frequency. For example, a less congested lane can 
processed once in two processing cycles.
debug-'y' or 'n' If 'y', the application will print debug info on the console.
For Sensors
sensor-Analog pin of the Arduino. The sensor is connected 
A0
sensorid-not relavant to comport-Arduino board id This sensor is connected to 
which is defined in the system initialization table.
srtm-Min value read from the sensor to determine traffic
is present in the lane.
The rtime-Time in miliseconds sensor should be read continuously.
to determine if traffic is in the lane.
rdelay-Time in miliseconds to wait before starting reading
from the sensor again. 
srtm, rtime, rdelay values are sent to Arduino.
which reads sensor data until elapsed.
with a delay of rdelay time. If the value read is higher,
Rather than srtm, it immediately ends the reading cycle.
inform the main application of the presence of traffic.
If the value read is less than srtm, it reads the sensor.
continuesly until a high srtm value is read or until a
time elapsed, meaning no traffic.
Desirable values for srtm, rtime and rdelay can be found here.
You can find out by running chksensor.py. 
For Cams
cam-Number ex. 0,1,2.. Windows will assign a number to a cam.
camid, camtype-Not relavant 
detectarea-To determine traffic presence,
A vehicle must be present in this area.
in the lane. These are the coordinates 
(x, y, width, height) of the cam view area,
The application application should detect vehicles.
mincarea-To identify a detected object as a vehicle and 
drop other objects which may be present in 
video image frame, area detected
The value of an object must be higher than this value.
rtime, rdelay-Same as specified in sensor but specified in
In seconds
viewcam-1 to show video cam frames on the console.
Desirable values for cam no, detectarea, mincarea, rtime 
and rdelay can be found out by running chkcam.py. 
Priority Assigning Table
"videop": "videosp1.txt"
"prtyid": "lane1-1", "type": "s", "pt": 20, "maxt": 2, 
"debug": "Y", "parms": "A3", "comport": "c1", 
"sensorid": "s3", "rdelay": 1, "rtime": 50, "srtm": 50
 
prtyid-Value specified in the "prtyid" parm of a lane 
entry in the lane definition table.
pt-If traffic is detected, this amount of 
time (in seconds) is added to the value in 
the "maxt" parm of the lane 
entry of the lane definition table.
Other parameters are the same as in the lane definition table. 
                 
                
Trafic Light Control Table
"tlc": "videotlc1.txt"
 
"lane": 1, 
"red": [["c1", [3," O", 0], [4," F", 1000], [2," O", 0], [3," F", 0]] ,
"green": [["c1", [3," O", 0], [2," F", 1000], [4," O", 0], [3," F", 0]]
 
lane-lane id 
When an application needs to light up, for example, red light
In lane 1, it will send the Arduino board Id "c1" following 
message
1) "On" LED connected to digital pin "3" 
and wait zero milliseconds.
For example, light up yellow
2) "Off" LED connected to digital pin "4" 
and wait 1000 miliseconds.
For example, off green
3) "On" LED connected to digital pin "2" 
and wait zero milliseconds.
For example, to light up red
4) "Off" LED connected to digital pin "3" 
and wait zero milliseconds.
For example, off yellow
green-to light up green, the same as red.
 
"lane": 99, 
"red": [["c1", "2," O", 0], [5," O", 0], [8," O", [11," O", 0]]
 
Lane '99' is a special lane which is used by the system to set 
All the red lights in the lanes are "On" when the system starts up.
Here, red LEDs on lanes are connected to digital pins 2, 5, 8 and 11.
Test System
After the system is setup, all the sensors, LEDs, and web cams must be checked.
py chksensor.py COM3 A0
To check a sensor connected to an analog pin (for example, A0) of the Arduino 
board connected to a serial port (for example, COM3) of a Windows machine
Here, desirable values for "srtm", "rtime" and "rdelay" can be found.
(by modifying the chksensor.py python program)
    
py chkled.py COM3 2
To check LED connected to digital pin (for ex. 2)
 
py chkcam.py 0
To check if the cam is connected to a windows machine (for example, cam 0). 
These are the numbers assigned to a cam by windows and the desirable values for 
"detectarea", "mincarea", "rtime" and "rdelay" parms of the lane 
entry of the lane definition table can be found.
(by modifying the chkcam.py python program)
Conclusion 
             
-This system is single-threaded and is useful for controlling traffic in 
moderately congested lanes.
-To achieve high efficiency and redundancy to handle high traffic 
We must have to deploy more than one sensor/cam to monitor the lanes.
lanes. The system will be multi-threaded and we may have to deploy 
machine learning techniques to determine the time for lanes depending on 
traffic lanes without allocating fixed time as in this model.
achieve high efficiency.
         
 
 
 
