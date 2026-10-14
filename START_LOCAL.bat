@echo off
cd /d "%~dp0"
where py >nul 2>nul && (start "LIMINAL" http://127.0.0.1:8765/ & py -3 -m http.server 8765 --bind 127.0.0.1 & exit /b)
where python >nul 2>nul && (start "LIMINAL" http://127.0.0.1:8765/ & python -m http.server 8765 --bind 127.0.0.1 & exit /b)
echo Cai dat Python 3 tu python.org roi thu lai.
pause
