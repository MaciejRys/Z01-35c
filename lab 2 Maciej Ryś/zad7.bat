@echo off
setlocal enabledelayedexpansion
set /p n=podaj liczbe ktorej trzeba obliczyc silnie

set a=1

for /l %%g in (1,1,%n%) do (
	set /a a=a*%%g
)
echo !a!

pause