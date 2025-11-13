@echo off
echo ========================================
echo    OctXXIII 설치 프로그램 v2.0
echo ========================================
echo.

REM 관리자 권한 확인
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 관리자 권한으로 실행 중...
) else (
    echo 경고: 관리자 권한이 필요할 수 있습니다.
    echo.
)

REM 설치 디렉토리 생성
set "INSTALL_DIR=%ProgramFiles%\OctXXIII"
echo 설치 디렉토리: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" (
    echo 디렉토리 생성 중...
    mkdir "%INSTALL_DIR%"
)

REM 실행 파일 복사
echo OctXXIII.exe 복사 중...
copy "dist\OctXXIII.exe" "%INSTALL_DIR%\" /Y

REM 바탕화면 바로가기 생성
echo 바탕화면 바로가기 생성 중...
set "DESKTOP=%USERPROFILE%\Desktop"
echo [InternetShortcut] > "%DESKTOP%\OctXXIII.url"
echo URL=file:///%INSTALL_DIR%\OctXXIII.exe >> "%DESKTOP%\OctXXIII.url"
echo IconFile=%INSTALL_DIR%\OctXXIII.exe >> "%DESKTOP%\OctXXIII.url"
echo IconIndex=0 >> "%DESKTOP%\OctXXIII.url"

REM 시작 메뉴 바로가기 생성
echo 시작 메뉴 바로가기 생성 중...
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%START_MENU%\OctXXIII" mkdir "%START_MENU%\OctXXIII"
echo [InternetShortcut] > "%START_MENU%\OctXXIII\OctXXIII.url"
echo URL=file:///%INSTALL_DIR%\OctXXIII.exe >> "%START_MENU%\OctXXIII\OctXXIII.url"
echo IconFile=%INSTALL_DIR%\OctXXIII.exe >> "%START_MENU%\OctXXIII\OctXXIII.url"
echo IconIndex=0 >> "%START_MENU%\OctXXIII\OctXXIII.url"

echo.
echo ========================================
echo    설치가 완료되었습니다!
echo ========================================
echo.
echo 설치 위치: %INSTALL_DIR%
echo 바탕화면 바로가기: %DESKTOP%\OctXXIII.url
echo 시작 메뉴: %START_MENU%\OctXXIII\OctXXIII.url
echo.
echo OctXXIII를 실행하려면 바탕화면의 바로가기를 더블클릭하세요.
echo.
pause
