@echo off
set /p SCIEZKA=podaj sciezke rozpoczynajaca
cd %SCIEZKA%
set c=~
call :func c
pause
:func
FOR /D %%G in ("*") DO (
set c=%c%~
Echo %c% %%G
cd %%G
call :func c
cd ..
)
EXIT /B

