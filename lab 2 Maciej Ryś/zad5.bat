@echo off
set /p SCIEZKA=podaj sciezke do folderu w ktorym znajduje sie plik
set /p NAME=podaj nazwe pliku mp4
ffmpeg -i "%SCIEZKA%%NAME%.mp4" -vf "select=gte(n\,300)" -vframes 1 "%SCIEZKA%%NAME%.png"
pause