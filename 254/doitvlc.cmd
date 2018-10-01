REM .cmd file for Windows .CMD box...
setlocal
set pypath=E:\Users\fred\AppData\Local\Programs\Python\Python37

set captionline=%1
if "%1" == "" set captionline=0
%pypath%\python .\capscanvlc.py 254_captions.sbv embedded-ep254.mp3 %captionline%

