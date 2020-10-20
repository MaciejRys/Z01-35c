@echo off
setlocal enabledelayedexpansion
set /p n=podaj ilosc liczb fibonacciego

set a=1
set b=1

for /l %%g in (1,1,%n%) do (
	echo !a!
	set /a c=a+b
	set /a a=b
	set /a b=c

)


pause