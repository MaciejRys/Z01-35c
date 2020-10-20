echo off
set /p SOURCE=podaj zrodlo
set /p DEST=podaj docelowy folder
XCopy %SOURCE% %DEST% /T /E
pause