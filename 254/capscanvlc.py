#!/usr/bin/python3
# Scan YouTube Captions in .sbv format:
import sys
argvLen = len(sys.argv)
print("Arguments on command line:", argvLen, ":")
if argvLen < 3:
#print("Attempting very simple open of sys.argv[1]=", sys.argv[1])
p = vlc.MediaPlayer(sys.argv[2])
def convertTimeStamp(timeStampString):
fieldindex=0
        currentCaption=[begins,ends,'']
        fieldindex=fieldindex+1
    elif fieldindex == 1:
f.close()