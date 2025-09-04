#!/bin/bash

echo "=== macOS용 OctXXIII 빌드 ==="
echo

# Python 버전 확인
python3 --version
if [ $? -ne 0 ]; then
    echo "Python3가 설치되지 않았습니다."
    exit 1
fi

# 빌드 스크립트 실행
python3 build_macos.py

echo
echo "빌드가 완료되었습니다!"