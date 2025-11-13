@echo off
echo === Windows??Nobody 3 ë¹Œë“œ ===
echo.

REM Python ë²„ì „ ?•ì¸
python --version
if %errorlevel% neq 0 (
    echo Python???¤ì¹˜?˜ì? ?Šì•˜ê±°ë‚˜ PATH???†ìŠµ?ˆë‹¤.
    pause
    exit /b 1
)

REM ë¹Œë“œ ?¤í¬ë¦½íŠ¸ ?¤í–‰
python build_windows.py

echo.
echo ë¹Œë“œê°€ ?„ë£Œ?˜ì—ˆ?µë‹ˆ??
pause
