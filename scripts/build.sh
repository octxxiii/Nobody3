#!/bin/bash

echo "=== macOS??Nobody 3 빌드 ==="
echo

# Python 버전 ?�인
python3 --version
if [ $? -ne 0 ]; then
    echo "Python3가 ?�치?��? ?�았?�니??"
    exit 1
fi

# 빌드 ?�크립트 ?�행
python3 build_macos.py

echo
echo "빌드가 ?�료?�었?�니??"
