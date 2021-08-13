from video2 import video
import threading  
import time
import json
import sys
import argparse


def prcstrafic() :
    i=0
    skipc={}
    while True:
      fjd= json.loads(fr[i])
      print( '\nProcessing - ', fjd )

      lid = "l" + str(fjd["lane"])
      try :
        dummy = int(skipc[lid])
      except KeyError :
        skipc[lid] = int(fjd["skipc"])
      if skipc[lid] > 0 :
        skipc[lid] = skipc[lid] - 1
        i+=1
        if i == len(fr) :
          i=0
        continue 
  
      skipc[lid] = int(fjd["skipc"])

      rv = v.prcs(fjd["type"], 0, fjd["debug"], fjd["parms"])
      if  rv > 0 : 
        v.onofftl(ld ['lg'+ str(fjd["lane"]) ])
        while True :
          t = fjd["maxt"]   
          try :
            t = t + prcspriority(fjd["prtyid"])
          except KeyError :
            pass
          rv = v.prcs(fjd["type"], t, fjd["debug"], fjd["parms"])
          if rv > 0 :
            j=i+1
            if j == len(fr) :
              j=0 
            f=False
            while True :
              fjdx = json.loads(fr[j])
              rv = v.prcs(fjdx["type"], 0, fjdx["debug"], fjdx["parms"])
              if rv > 0 :   
                v.onofftl(ld ['lr'+ str(fjd["lane"]) ])
                i=j
                f = True
                break
              else :
                j+=1
                if j == len(fr):
                  j=0
                if j == i:
                  break
            if f :
              break
          else : 
            v.onofftl(ld ['lr'+ str(fjd["lane"]) ])
            i+=1
            break
      else :
        i+=1
      if i == len(fr) :
        i=0

def prcspriority(prtyid) :
  r=0
  for j in range(len(prtyid)) :
      for i in range(len(fr1)) :
        fjd1= json.loads(fr1[i])
        if fjd1["prtyid"] == prtyid[j] :
          p = v.prcs(fjd1["type"],fjd1["maxt"],fjd1["debug"],fjd1["parms"])
          print('p********',p)
          if int(p) > 0 :
            r = fjd1["pt"]
            break
      if r > 0 :
        break
  return r

parser = argparse.ArgumentParser(description='To Control Trafic Light System')  
#parser.add_argument('--sit', default='sit.txt', help='System Initialization Table')
parser.add_argument('sit', help='System Initialization Table', default='sit.txt')
args = parser.parse_args()

with open( args.sit, 'r' ) as f :
  cr=json.load(f)


with open( cr["tlc"], 'r' ) as f :
  tlc=json.load(f)

v = video(cr)

ld = {}
for item in tlc:
  lane = item.get("lane")
  if lane == 99:
     v.onofftl(item.get("red"))
  else :
     ld [ 'lr' + str(lane) ] = item.get("red")
     ld [ 'lg' + str(lane) ] = item.get("green")

with open( cr["videom"], 'r' ) as f :
  fr=list(f)
with open( cr["videop"], 'r' ) as f :
  fr1=list(f)
prcstrafic()
