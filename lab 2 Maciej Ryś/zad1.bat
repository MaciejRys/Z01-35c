@echo off
set /p SCIEZKA=podaj sciezke
set /p EXT=podaj rozszerzenie

For %%A in (%SCIEZKA%*.%EXT%) do (echo %%A)
pause