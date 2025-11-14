#!/bin/bash
# macOS 빌드 스크립트

echo "=== Building Nobody 3 for macOS ==="

# PyInstaller 설치 확인
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# 빌드 실행
pyinstaller --clean --noconfirm Nobody3.spec

# 패키지 생성
python3 create_release_package.py

echo "=== macOS build complete! ==="
echo "Result: releases/Nobody3-macOS.zip"

