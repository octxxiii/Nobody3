@echo off
echo ========================================
echo    Nobody 3 ?�거 ?�로그램 v2.0
echo ========================================
echo.

REM 관리자 권한 ?�인
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 관리자 권한?�로 ?�행 �?..
) else (
    echo 경고: 관리자 권한???�요?????�습?�다.
    echo.
)

REM ?�치 ?�렉?�리 ?�인
set "INSTALL_DIR=%ProgramFiles%\Nobody 3"
if exist "%INSTALL_DIR%" (
    echo ?�치 ?�렉?�리 발견: %INSTALL_DIR%
    echo.
    set /p confirm="?�말�?Nobody 3�??�거?�시겠습?�까? (Y/N): "
    if /i "%confirm%"=="Y" (
        echo ?�일 ?�거 �?..
        rmdir /s /q "%INSTALL_DIR%"
        echo ?�치 ?�렉?�리가 ?�거?�었?�니??
    ) else (
        echo ?�거가 취소?�었?�니??
        goto :end
    )
) else (
    echo ?�치 ?�렉?�리�?찾을 ???�습?�다: %INSTALL_DIR%
)

REM 바탕?�면 바로가�??�거
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%\Nobody 3.url" (
    echo 바탕?�면 바로가�??�거 �?..
    del "%DESKTOP%\Nobody 3.url"
)

REM ?�작 메뉴 바로가�??�거
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Nobody 3"
if exist "%START_MENU%" (
    echo ?�작 메뉴 바로가�??�거 �?..
    rmdir /s /q "%START_MENU%"
)

REM 캐시 ?�렉?�리 ?�거
set "CACHE_DIR=%LOCALAPPDATA%\Nobody 3"
if exist "%CACHE_DIR%" (
    echo 캐시 ?�렉?�리 ?�거 �?..
    rmdir /s /q "%CACHE_DIR%"
)

echo.
echo ========================================
echo    ?�거가 ?�료?�었?�니??
echo ========================================
echo.

:end
pause
