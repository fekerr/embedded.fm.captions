#!/usr/bin/python

AUTHORDATE="fekerr 20180909-20180919"

# capscan.py - scan YouTube captions.sbv files
#
# Command line:
#   capscan.py < captions.sbv [wordfile [syncMode]]
#
# Scan YouTube Captions in .sbv format
# Output lightly parsed:
#
# Caption number: begin, end: text
#
# begin and end are caption times from start of recording,
# in floating point seconds
# text of caption
#
# after scanning through file, output a list of words to another
# file or stdout
#

# This is coded as a simple python script.
# It servers as a review and refresh of python,
# and may be used as an example of:  "This is one way to do it, then
# let's do it a better way!"

# Some early design notes and brainstorming:
#
# (debug) Print arguments in command line;
# Start parsing YouTube .sbv captions file;
# Parse time stamps;
# Start generating word lists, vocabularies, ....
# ....
# Other ideas: print out as "event" list,
# Left column starts with timeStamp, then as "caption start time"
# and "caption end time" are reached, indicate that.
#
# .srt format where each caption has a number is somewhat useful,
# but we don't need that extra information, really, since it seems easy to
# generate on the fly.
#
# "Start caption
# ....
# Would be nice to play back mp3 from python.
# ....
# Would be nice to play back with some of the previous ideas,
# with time delays, and some  interactive keyboard controls
# to allow adding notations, such as "Speaker Change", "Fix Caption", Todo, etc.
# Just keep it simple and allow entering some set of keyboard keys and put them
# in an output file in some easily scanned notation.
# ....
# Eventually could have some variables to configure at the beginning, such as list
# of speakers and tags for each one.
# ....

import sys
import time

# syncMode setting sleeps until the begin caption time is met
# TODO: better command line options
syncMode = True

print "capscan.py:, ", AUTHORDATE
print "Simple python script to scan YouTube .SBV captions files."
print "Usage: capscan <caption.sbv> [wordsList.txt [syncMode]]"
print

argvLen = len(sys.argv)
print "Arguments on command line:", argvLen, ":"

for i in sys.argv:
    print i

if argvLen < 2:
    print "Insufficient arguments."
    exit()

if argvLen > 3:
    syncMode = int(sys.argv[3])

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

# TODO: .srt file format seems to just have an integer number on a line
#   (starting at 1), before the timestamp begin, end, line.

# Treat three lines as one record, or
# treat as 3 fields, each on separate lines.

# Start to collect vocabulary, words.
# Should make objects to collect various useful information.
# caption object (collect the 3 lines, then have a list of them)
# words objects (a word, count of occurrance, location used, words before and after it?)
# Sequence of words is also important, or the probabilities of one word following another?
# Currently sorting the set at the end: copy set to list and sort list.
#   Yeah, who cares about efficiency?
# Obviously should be word/word sequence objects/data structures eventually, not just a simple set.

vocabWords = set()
fieldindex=0
captionNumber=0
currentCaption=[0,0,None]
captionList=[]

startTime=time.time()
print "Start Time = ", startTime

for line in f:
    if fieldindex == 0:
        beg,end=line.split(",")
        begins=convertTimeStamp(beg)
        ends=convertTimeStamp(end)

        currentCaption=[begins,ends,'']
        captionList.append(currentCaption)
        print '{0:05d}: {1:09.3f}, {2:0<09.3f}'.format(captionNumber, begins, ends),

        waitForTs=begins - (time.time() - startTime)
        if syncMode and (waitForTs > 0.0):
            time.sleep(waitForTs)

        fieldindex=fieldindex+1
    elif fieldindex == 1:
        captionList[captionNumber][2] = line.strip()
        print captionList[captionNumber][2]

# TODO: check if this misses any words

#        for i in line.split(" "):
        for i in captionList[captionNumber][2].split(" "):
            vocabWords.add(i.strip());

        fieldindex=fieldindex+1
    elif fieldindex == 2:
#        print "Blank=", line
        captionNumber = captionNumber + 1
        fieldindex=0

f.close()

# simple simple simple, copy set to list and sort it. Could be better!

vocabList = []
for i in vocabWords:
    vocabList.append(i)
vocabList.sort()

# If output filename provided, output vocabulary word list stuff to a file.
saveout = sys.stdout # derived from http://www.diveintopython.net/scripts_and_streams/stdin_stdout_stderr.html
if argvLen > 2:
    print "Attempting very simple open *FOR OUTPUT* of sys.argv[2]=", sys.argv[2]
    fOut = open(sys.argv[2], "w") # let's be mean and not check for file or append
    sys.stdout = fOut

print "vocabList="
print vocabList

sys.stdout = saveout # restore stdout in case we changed it.

