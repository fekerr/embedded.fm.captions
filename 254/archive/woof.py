def convertTimeStamp(timeStampString):
    ts = timeStampString.split(':');
    sec = ts[2].split('.');
    return int(ts[0]) * 3600.0 + int(ts[1]) * 60.0 + int(sec[0]) + int(sec[1]) / 1000.0

beginStr="0:00:03.640"
endStr="0:00:11.660"

print '"', beginStr, '"', '"', endStr, '"'
print convertTimeStamp(beginStr), convertTimeStamp(endStr)
