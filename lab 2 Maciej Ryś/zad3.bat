@echo off
net session >nul 2>nul
if %errorLevel% == 0 (
   echo Success: Administrative permissions confirmed.
) else (
   echo Failure: Current permissions inadequate.
)
pause >nul