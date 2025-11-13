@echo off
echo ========================================
echo    Nobody 3 ?¤ì¹˜ ?„ë¡œê·¸ëž¨ v2.0
echo ========================================
echo.

REM ê´€ë¦¬ìž ê¶Œí•œ ?•ì¸
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ê´€ë¦¬ìž ê¶Œí•œ?¼ë¡œ ?¤í–‰ ì¤?..
) else (
    echo ê²½ê³ : ê´€ë¦¬ìž ê¶Œí•œ???„ìš”?????ˆìŠµ?ˆë‹¤.
    echo.
)

REM ?¤ì¹˜ ?”ë ‰? ë¦¬ ?ì„±
set "INSTALL_DIR=%ProgramFiles%\Nobody 3"
echo ?¤ì¹˜ ?”ë ‰? ë¦¬: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" (
    echo ?”ë ‰? ë¦¬ ?ì„± ì¤?..
    mkdir "%INSTALL_DIR%"
)

REM ?¤í–‰ ?Œì¼ ë³µì‚¬
echo Nobody 3.exe ë³µì‚¬ ì¤?..
copy "dist\Nobody 3.exe" "%INSTALL_DIR%\" /Y

REM ë°”íƒ•?”ë©´ ë°”ë¡œê°€ê¸??ì„±
echo ë°”íƒ•?”ë©´ ë°”ë¡œê°€ê¸??ì„± ì¤?..
set "DESKTOP=%USERPROFILE%\Desktop"
echo [InternetShortcut] > "%DESKTOP%\Nobody 3.url"
echo URL=file:///%INSTALL_DIR%\Nobody 3.exe >> "%DESKTOP%\Nobody 3.url"
echo IconFile=%INSTALL_DIR%\Nobody 3.exe >> "%DESKTOP%\Nobody 3.url"
echo IconIndex=0 >> "%DESKTOP%\Nobody 3.url"

REM ?œìž‘ ë©”ë‰´ ë°”ë¡œê°€ê¸??ì„±
echo ?œìž‘ ë©”ë‰´ ë°”ë¡œê°€ê¸??ì„± ì¤?..
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%START_MENU%\Nobody 3" mkdir "%START_MENU%\Nobody 3"
echo [InternetShortcut] > "%START_MENU%\Nobody 3\Nobody 3.url"
echo URL=file:///%INSTALL_DIR%\Nobody 3.exe >> "%START_MENU%\Nobody 3\Nobody 3.url"
echo IconFile=%INSTALL_DIR%\Nobody 3.exe >> "%START_MENU%\Nobody 3\Nobody 3.url"
echo IconIndex=0 >> "%START_MENU%\Nobody 3\Nobody 3.url"

echo.
echo ========================================
echo    ?¤ì¹˜ê°€ ?„ë£Œ?˜ì—ˆ?µë‹ˆ??
echo ========================================
echo.
echo ?¤ì¹˜ ?„ì¹˜: %INSTALL_DIR%
echo ë°”íƒ•?”ë©´ ë°”ë¡œê°€ê¸? %DESKTOP%\Nobody 3.url
echo ?œìž‘ ë©”ë‰´: %START_MENU%\Nobody 3\Nobody 3.url
echo.
echo Nobody 3ë¥??¤í–‰?˜ë ¤ë©?ë°”íƒ•?”ë©´??ë°”ë¡œê°€ê¸°ë? ?”ë¸”?´ë¦­?˜ì„¸??
echo.
pause
