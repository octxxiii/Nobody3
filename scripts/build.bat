@echo off
echo === Windows용 OctXXIII 빌드 ===
echo.

REM Python 버전 확인
python --version
if %errorlevel% neq 0 (
    echo Python이 설치되지 않았거나 PATH에 없습니다.
    pause
    exit /b 1
)

REM 빌드 스크립트 실행
python build_windows.py

echo.
echo 빌드가 완료되었습니다!
pause