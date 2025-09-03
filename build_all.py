#!/usr/bin/env python3
"""
전체 빌드 프로세스 관리 스크립트
"""

import sys
import os
import platform
import subprocess

def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        return False
    return True

def install_build_dependencies():
    """빌드에 필요한 기본 패키지 설치"""
    print("기본 빌드 의존성 설치 중...")
    
    packages = ["cx_Freeze", "Pillow"]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✓ {package} 설치됨")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 설치 실패: {e}")
            return False
    
    return True

def create_icons():
    """아이콘 생성"""
    print("아이콘 생성 중...")
    try:
        subprocess.run([sys.executable, "create_icon.py"], check=True)
        print("✓ 아이콘 생성 완료")
        return True
    except subprocess.CalledProcessError:
        print("✗ 아이콘 생성 실패 (선택사항이므로 계속 진행)")
        return True

def build_for_platform():
    """플랫폼별 빌드 실행"""
    system = platform.system()
    
    if system == "Windows":
        print("Windows용 빌드 시작...")
        try:
            subprocess.run([sys.executable, "build_windows.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Windows 빌드 실패: {e}")
            return False
            
    elif system == "Darwin":
        print("macOS용 빌드 시작...")
        try:
            subprocess.run([sys.executable, "build_macos.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"macOS 빌드 실패: {e}")
            return False
            
    else:
        print(f"지원하지 않는 플랫폼: {system}")
        print("Windows 또는 macOS에서 실행해주세요.")
        return False

def main():
    """메인 빌드 프로세스"""
    print("=" * 50)
    print("OctXXIII 통합 빌드 시스템")
    print("=" * 50)
    print()
    
    # 시스템 정보 출력
    print(f"플랫폼: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print()
    
    # 단계별 빌드 실행
    steps = [
        ("Python 버전 확인", check_python_version),
        ("빌드 의존성 설치", install_build_dependencies),
        ("아이콘 생성", create_icons),
        ("플랫폼별 빌드", build_for_platform),
    ]
    
    for step_name, step_func in steps:
        print(f"[{step_name}]")
        if not step_func():
            print(f"✗ {step_name} 실패")
            return 1
        print()
    
    print("=" * 50)
    print("✓ 모든 빌드 과정이 완료되었습니다!")
    print("=" * 50)
    
    # 결과 파일 안내
    system = platform.system()
    if system == "Windows":
        print("생성된 파일:")
        print("- build/exe.win-amd64-3.x/ (실행 파일)")
        print("- OctXXIII.msi (설치 파일)")
    elif system == "Darwin":
        print("생성된 파일:")
        print("- OctXXIII.app (앱 번들)")
        print("- OctXXIII.dmg (설치 파일)")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n빌드가 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n예상치 못한 오류: {e}")
        sys.exit(1)