#!/usr/bin/python3

# Environmental / dev issues: "Windows" vs "UNIX"
# end of lines (windows editor notepad++ config)

# This file currently only works in a Windows .CMD environment...
# VLC must be installed
# get vlc.py for VLC API bindings
# msvcrt used for reading keys (unblocking)
#
# file doitvlc.cmd:
# python ./capscanvlc.py 254_captions.sbv embedded-ep254.mp3

AUTHORDATE="fekerr 20180909-20180928"

#
#   capscanvlc.py <captions.sbv> <episode.mp3> <captionStartLine#>
#

# Scan YouTube Captions in .sbv format:
#  Caption number: begin, end: text
#
# begin, end: caption times from start of recording,
#     in floating point seconds (end is currently not used here)
# text: text of caption

import sys
import time
import vlc

# Interactive keyboard input gets annoying fast.
import msvcrt

print("capscanvlc.py:, ", AUTHORDATE)
print("Simple python script to scan YouTube .SBV captions files and play the MP3.")
print("Usage: capscanvlc <caption.sbv> <episode.mp3> <caption # start>\n")

argvLen = len(sys.argv)

print("Arguments on command line:", argvLen, ":")
for i in sys.argv:
    print(i)

if argvLen < 3:
    print("Insufficient arguments.")
    exit()

#print("Attempting very simple open of sys.argv[1]=", sys.argv[1])
f = open(sys.argv[1], "r")
#print(f)

p = vlc.MediaPlayer(sys.argv[2])
print(f, p)

captionPlaybackStart = 0
if argvLen >= 3:
   captionPlaybackStart = int(sys.argv[3])
#  print("Starting on caption line {}.".format(captionPlaybackStart))

# convertTimeStamp(string):
# string is of format "hh:mm:ss.fff"
# Returns float, seconds since beginning.

def convertTimeStamp(timeStampString):
    ts = timeStampString.split(':');
    sec = ts[2].split('.');
    return int(ts[0]) * 3600.0 + int(ts[1]) * 60.0 + int(sec[0]) + int(sec[1]) / 1000.0

fieldindex=0
captionNumber=0
currentCaption=[0,0,None]
captionList=[]

for line in f:
    if fieldindex == 0:
        beg,end=line.split(",")
        begins=convertTimeStamp(beg)
        ends=convertTimeStamp(end)

        currentCaption=[begins,ends,'']
        captionList.append(currentCaption)
#        print('{0:05d}: {1:09.3f}'.format(captionNumber, begins), end=' ')

        fieldindex=fieldindex+1

    elif fieldindex == 1:
        captionList[captionNumber][2] = line.strip()
        fieldindex=fieldindex+1
    elif fieldindex == 2: # blank line
        captionNumber = captionNumber + 1
        fieldindex=0

f.close()

currentCaption=[ends+1,ends+1,'[END]'] # dummy
captionList.append(currentCaption)

#print("Playing back")
p.play()
p.set_pause(True)

caption=captionPlaybackStart
modFlag=True

# TODO: do this better with events in a queue

while(caption in range(len(captionList)-1)): # added dummy at end of list
   cap=captionList[caption]   
#   print("caption={}".format(caption))
   if(modFlag):
      print("set_time()")
      p.set_time(int(1000.0 * cap[0]))
      p.set_pause(False)

   # Use the next start time instead of the current end time.
   # There is some overlap.

   print('{: 5d}:{: 7.3f},{: 7.3f}: {:}'.format(caption, cap[0], captionList[caption+1][0], cap[2]))
   sleepTime = captionList[caption+1][0] - cap[0]
   if(sleepTime > 0.0):
#     print("Sleeping while playing back. {} until {}".format(sleepTime, cap[1]))
      time.sleep(sleepTime)
   
   caption = caption + 1
   modFlag = False

   # process user interactions (keys).
   kbhit=msvcrt.kbhit() # windows-specific method....
   if(not kbhit):
      continue

   #print("Key hit.")

   modFlag = True
   p.set_pause(True)

   # Quick and dirty - 'p' to pause, 'q' to quit.
   
   getchs=[]
   while(kbhit):
     getchs.append(ord(msvcrt.getch()))
     kbhit=msvcrt.kbhit()
   else:
      if(getchs):
         print(getchs)
         # this is simple and dumb... Only processing the first key.
		 # different systems give 113,0 or just 113 depending on some environmental settings?
         
         if(getchs[0]==113): # and getchs[1]==0): # 'q' = quit - blam!
            exit()

         if(getchs[0]==112): # and getchs[1]==0): # 'p' = pause
         
            print("Paused. Waiting for the any key.")
            # now wait for a new key
            kbhit=msvcrt.kbhit()            
            while(not kbhit):
               time.sleep(1)
               kbhit=msvcrt.kbhit()
               
            getchs=[]
            while(kbhit):
              getchs.append(ord(msvcrt.getch()))
              kbhit=msvcrt.kbhit()
            print(getchs) # show the any keys
            
         else: # not 'p' or 'q'
            print("\nKey(s) hit: ", getchs)
