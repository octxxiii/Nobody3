@echo off
echo ===================================
echo OctXXIII MSI 빌드 스크립트
echo ===================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되지 않았거나 PATH에 없습니다.
    echo Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 가상환경 활성화 (있는 경우)
if exist ".venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call .venv\Scripts\activate.bat
)

REM 빌드 스크립트 실행
echo MSI 빌드 시작...
python build_msi.py

echo.
echo 빌드 완료! 생성된 파일을 확인하세요.
pause