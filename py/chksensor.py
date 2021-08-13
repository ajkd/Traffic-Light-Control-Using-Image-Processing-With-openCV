import serial
import argparse
import time
parser = argparse.ArgumentParser(description='To Check Sensor')  
parser.add_argument('port', type=str, help='com port')
parser.add_argument('pin', type=str, help='pin sensor connect to')
args = parser.parse_args()
ard=serial.Serial(args.port,9600,timeout=10)
time.sleep(2)
while ( True ):
     sr = '#1#' + args.pin + ',' + str(1) + ',' + str(50)+  ',#\n'
     ard.write(sr.encode('utf-8'))
     ard.flush()
     msg=ard.read_until()
     if len(msg) > 0 :
       s=msg.decode('utf-8')
       print ( 'Read From Sensor - ', s )
     else :
       print ( 'No Data Read From Sensor - '  + args.pin )
     