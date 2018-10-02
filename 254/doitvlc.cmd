REM .cmd file for Windows .CMD box...

rem Requirements:
rem Install desktop version of VLC
rem pip install python-vlc
rem copy vlc.py and .mp3 to local directory (see command line below)

setlocal

rem set pypath=E:\Users\fred\AppData\Local\Programs\Python\Python37
set pypath="C:\Users\feker\AppData\Local\Programs\Python\Python37"

set captionline=%1
if "%1" == "" set captionline=0
%pypath%\python capscanvlc.py 254_captions.sbv embedded-ep254.mp3 %captionline%

