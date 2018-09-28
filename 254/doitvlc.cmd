REM .cmd file for Windows .CMD box...
setlocal
set captionline=%1
if "%1" == "" set captionline=0
python ./capscanvlc.py 254_captions.sbv embedded-ep254.mp3 %captionline%

