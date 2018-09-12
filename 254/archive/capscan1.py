#!/usr/bin/python
#TODO shbang?

# fekerr 20180909
# Simple python script to print arguments in command line;
# start parsing YouTube .sbv captions file;
# parse time stamps;
# ....
# 
# would be nice to play back mp3 from python

import sys
import time

print "This is a refresh and extend review of python."
print "Keeping everything extremely simple."

print "Arguments on command line:", len(sys.argv), ":"
for i in sys.argv:
    print i

print "Attempting very simple open of sys.argv[1]=", sys.argv[1]
f = open(sys.argv[1], "r")

def convertTimeStamp(timeStampString):
    ts = timeStampString.split(':');
    sec = ts[2].split('.');
    return int(ts[0]) * 3600.0 + int(ts[1]) * 60.0 + int(sec[0]) + int(sec[1]) / 1000.0

# test code and almost documentation for convertTimeStamp():
#beginStr="0:00:03.640"
#endStr="0:00:11.660"
#
#print '"', beginStr, '"', '"', endStr, '"'
#print convertTimeStamp(beginStr), convertTimeStamp(endStr)

# parsing for now will be extremely simple
# expect only original file format of
#    timestamp line
#    text line
#    blank line

# Treat three lines as one record, or
# treat as 3 fields, each on separate lines.

fieldindex=0
for line in f:
    if fieldindex == 0:
        print "TS=", line
        beg,end=line.split(",")
#       print beg, end
        begins=beg.convertTimeStamp()
        ends=end.convertTimeStamp()
        print "Begins:", begins, ", Ends:", ends
        fieldindex=fieldindex+1
    elif fieldindex == 1:
        print "Text=", line
        fieldindex=fieldindex+1
    elif fieldindex == 2:
#        print "Blank=", line
        fieldindex=0


