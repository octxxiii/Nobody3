@echo off
echo ========================================
echo    OctXXIII 제거 프로그램 v2.0
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

REM 설치 디렉토리 확인
set "INSTALL_DIR=%ProgramFiles%\OctXXIII"
if exist "%INSTALL_DIR%" (
    echo 설치 디렉토리 발견: %INSTALL_DIR%
    echo.
    set /p confirm="정말로 OctXXIII를 제거하시겠습니까? (Y/N): "
    if /i "%confirm%"=="Y" (
        echo 파일 제거 중...
        rmdir /s /q "%INSTALL_DIR%"
        echo 설치 디렉토리가 제거되었습니다.
    ) else (
        echo 제거가 취소되었습니다.
        goto :end
    )
) else (
    echo 설치 디렉토리를 찾을 수 없습니다: %INSTALL_DIR%
)

REM 바탕화면 바로가기 제거
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%\OctXXIII.url" (
    echo 바탕화면 바로가기 제거 중...
    del "%DESKTOP%\OctXXIII.url"
)

REM 시작 메뉴 바로가기 제거
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\OctXXIII"
if exist "%START_MENU%" (
    echo 시작 메뉴 바로가기 제거 중...
    rmdir /s /q "%START_MENU%"
)

REM 캐시 디렉토리 제거
set "CACHE_DIR=%LOCALAPPDATA%\OctXXIII"
if exist "%CACHE_DIR%" (
    echo 캐시 디렉토리 제거 중...
    rmdir /s /q "%CACHE_DIR%"
)

echo.
echo ========================================
echo    제거가 완료되었습니다!
echo ========================================
echo.

:end
pause
