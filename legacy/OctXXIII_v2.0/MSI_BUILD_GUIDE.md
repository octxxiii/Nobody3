# OctXXIII MSI 빌드 가이드

## 개요
이 가이드는 OctXXIII 애플리케이션을 Windows MSI 설치 파일로 빌드하는 방법을 설명합니다.

## 필요 조건

### 필수 요구사항
- Windows 10/11
- Python 3.8 이상
- Git (선택사항)

### 권장 도구 (선택사항)
1. **Advanced Installer** (가장 전문적인 MSI)
   - 다운로드: https://www.advancedinstaller.com/
   - 30일 무료 체험판 사용 가능

2. **Inno Setup** (EXE 설치 파일)
   - 다운로드: https://jrsoftware.org/isinfo.php
   - 완전 무료

## 빌드 방법

### 방법 1: 자동 빌드 스크립트 사용 (권장)

1. **배치 파일 실행**
   ```cmd
   build_msi.bat
   ```

2. **또는 Python 스크립트 직접 실행**
   ```cmd
   python build_msi.py
   ```

### 방법 2: 기존 빌드 시스템 사용

1. **전체 빌드**
   ```cmd
   python build_all.py
   ```

2. **Windows 전용 빌드**
   ```cmd
   python build_windows.py
   ```

3. **cx_Freeze 사용**
   ```cmd
   python setup.py bdist_msi
   ```

## 빌드 옵션

### 1. Advanced Installer (권장)
- 가장 전문적인 MSI 파일 생성
- 사용자 정의 설치 옵션
- 디지털 서명 지원
- 자동 업데이트 지원

### 2. cx_Freeze
- 간단한 MSI 생성
- 무료
- 기본적인 설치 기능

### 3. Inno Setup
- EXE 설치 파일 생성
- 무료이며 매우 안정적
- 다국어 지원
- 사용자 정의 설치 화면

## 생성되는 파일

빌드 완료 후 다음 파일들이 생성됩니다:

```
dist/
├── OctXXIII/                 # PyInstaller 실행 파일 폴더
│   ├── OctXXIII.exe         # 메인 실행 파일
│   ├── ffmpeg.exe           # FFmpeg 바이너리
│   └── ... (기타 라이브러리)
├── OctXXIII.msi            # MSI 설치 파일 (Advanced Installer/cx_Freeze)
└── OctXXIII-setup.exe      # EXE 설치 파일 (Inno Setup)
```

## 문제 해결

### 일반적인 문제

1. **Python 모듈 누락**
   ```cmd
   pip install -r requirements.txt
   ```

2. **PyQt5 설치 오류**
   ```cmd
   pip install --upgrade pip
   pip install PyQt5==5.15.10
   ```

3. **FFmpeg 누락**
   - `ffmpeg.exe`를 프로젝트 루트에 복사
   - 또는 `build_windows.py`가 자동으로 다운로드

4. **권한 오류**
   - 관리자 권한으로 명령 프롬프트 실행

### 빌드 실패 시

1. **의존성 재설치**
   ```cmd
   pip uninstall -y PyQt5 pyinstaller cx-Freeze
   pip install -r requirements.txt
   ```

2. **빌드 폴더 정리**
   ```cmd
   rmdir /s build
   rmdir /s dist
   del *.spec
   ```

3. **가상환경 사용**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python build_msi.py
   ```

## 고급 설정

### 아이콘 변경
- `icon.ico` 파일을 프로젝트 루트에 배치
- 32x32, 48x48, 256x256 크기 포함 권장

### 버전 정보 수정
`build_msi.py` 파일에서 다음 값들을 수정:
```python
self.version = "1.0.0"        # 버전 번호
self.author = "nobody"        # 제작자
self.description = "..."      # 설명
```

### 추가 파일 포함
PyInstaller spec 파일의 `datas` 섹션에 추가:
```python
datas=[
    ('resources_rc.py', '.'),
    ('config.json', '.'),      # 추가 파일
    ('docs/', 'docs/'),        # 폴더 전체
],
```

## 배포

생성된 MSI 또는 EXE 파일을 사용자에게 배포할 수 있습니다:

1. **MSI 파일**: Windows Installer를 통한 표준 설치
2. **EXE 파일**: 사용자 정의 설치 마법사

## 라이선스

이 빌드 스크립트는 OctXXIII 프로젝트와 동일한 라이선스를 따릅니다.