# no shbang, bash bash bash
# this is the "local" version using a local, perhaps updated copy of the original captions file
# from YouTube.

# ./capscan.py ../originalCaptions/254_captions.sbv werdz254.txt > capscan254.txt

#echo '$0='$0
#echo '$1='$1
#echo '$2='$2
#echo '$3='$3

# $1 is 1 or 0 for syncMode: 0 to scan all without pausing, 1 to "sync" with beginning timestamp
./capscan.py 254_captions.sbv wordList254.txt $1
