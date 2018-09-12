#!/usr/bin/python
#TODO review shbang?

# fekerr 20180909-20180911
# Simple python script used for review and refresh of
# python, and to do some work.
#
# Print arguments in command line;
# Start parsing YouTube .sbv captions file;
# Parse time stamps;
# Start generating word lists, vocabularies, ....
# Give up and actually design it.
# ....
# Would be nice to play back mp3 from python.

import sys
import time

print "capscan.py: fekerr 20180909-20180911"
print "Simple python script to scan YouTube .SBV captions files."
print "Usage: capscan <caption.sbv>"
print
print "Arguments on command line:", len(sys.argv), ":"

for i in sys.argv:
    print i

print "Attempting very simple open of sys.argv[1]=", sys.argv[1]
f = open(sys.argv[1], "r")
print f

# convertTimeStamp(string):
# string is of format "hh:mm:ss.fff"
# Quickly checked some libraries and decided to just do it.
# Returns float, seconds since beginning.

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

# TODO: .srt file format seems to just have an integer number on a line before the timestamp begin, end, line.
# TODO: support .srt file format eventually, or instead....

# Treat three lines as one record, or
# treat as 3 fields, each on separate lines.

# Start to collect vocabulary, words.
# Sequence of words is also important, or the probabilities of one word following another?
# Also should sort...
# Obviously should be word/word sequence objects eventually, not just a simple set.

vocabWords = set()
fieldindex=0

for line in f:
    if fieldindex == 0:
#        print "TS=", line
        beg,end=line.split(",")
        begins=convertTimeStamp(beg)
        ends=convertTimeStamp(end)
        print begins, ends,
        fieldindex=fieldindex+1
    elif fieldindex == 1:
        print line

# TODO: check if this misses any words

        for i in line.split(" "):
            vocabWords.add(i.strip());

        fieldindex=fieldindex+1
    elif fieldindex == 2:
#        print "Blank=", line
        fieldindex=0

f.close()

# TODO: output to a file, duh.

print "vocabWords="
print vocabWords

