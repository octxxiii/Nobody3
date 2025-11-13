@echo off
echo ===================================
echo Nobody 3 MSI ë¹Œë“œ ?¤í¬ë¦½íŠ¸
echo ===================================
echo.

REM Python ?¤ì¹˜ ?•ì¸
python --version >nul 2>&1
if errorlevel 1 (
    echo Python???¤ì¹˜?˜ì? ?Šì•˜ê±°ë‚˜ PATH???†ìŠµ?ˆë‹¤.
    echo Python 3.8 ?´ìƒ???¤ì¹˜?´ì£¼?¸ìš”.
    pause
    exit /b 1
)

REM ê°€?í™˜ê²??œì„±??(?ˆëŠ” ê²½ìš°)
if exist ".venv\Scripts\activate.bat" (
    echo ê°€?í™˜ê²??œì„±??ì¤?..
    call .venv\Scripts\activate.bat
)

REM ë¹Œë“œ ?¤í¬ë¦½íŠ¸ ?¤í–‰
echo MSI ë¹Œë“œ ?œì‘...
python build_msi.py

echo.
echo ë¹Œë“œ ?„ë£Œ! ?ì„±???Œì¼???•ì¸?˜ì„¸??
pause
