# OctXXIII 빌드 가이드

FFmpeg를 포함한 설치 파일을 생성하는 방법입니다.

## 필요 조건

### Windows
- Python 3.8 이상
- pip
- WiX Toolset (MSI 생성용, 선택사항)
  - 다운로드: https://wixtoolset.org/releases/

### macOS
- Python 3.8 이상
- pip
- Xcode Command Line Tools
  ```bash
  xcode-select --install
  ```

## 빌드 방법

### Windows에서 빌드

1. **자동 빌드 (권장)**
   ```cmd
   build.bat
   ```

2. **수동 빌드**
   ```cmd
   python build_windows.py
   ```

### macOS에서 빌드

1. **자동 빌드 (권장)**
   ```bash
   ./build.sh
   ```

2. **수동 빌드**
   ```bash
   python3 build_macos.py
   ```

## 빌드 과정

### 자동으로 수행되는 작업:

1. **FFmpeg 다운로드**
   - Windows: 최신 Windows용 FFmpeg 바이너리
   - macOS: Apple Silicon/Intel 맞춤 FFmpeg 바이너리

2. **의존성 설치**
   - PyQt5
   - yt-dlp
   - requests
   - cx_Freeze (빌드 도구)

3. **실행 파일 생성**
   - 모든 의존성을 포함한 독립 실행 파일

4. **설치 파일 생성**
   - Windows: MSI 설치 파일
   - macOS: DMG 설치 파일

## 생성되는 파일

### Windows
- `build/exe.win-amd64-3.x/` - 실행 파일 폴더
- `OctXXIII.msi` - MSI 설치 파일

### macOS
- `OctXXIII.app` - 앱 번들
- `OctXXIII.dmg` - DMG 설치 파일

## 문제 해결

### Windows

**WiX Toolset 없음**
- MSI 파일이 생성되지 않지만 실행 파일은 정상 생성됩니다
- WiX Toolset 설치 후 다시 빌드하세요

**FFmpeg 다운로드 실패**
- 인터넷 연결을 확인하세요
- 방화벽이 다운로드를 차단하지 않는지 확인하세요

### macOS

**권한 오류**
```bash
chmod +x build.sh
sudo xattr -rd com.apple.quarantine OctXXIII.app
```

**DMG 생성 실패**
- dmgbuild 패키지가 설치되지 않은 경우:
```bash
pip3 install dmgbuild
```

**앱 서명 (선택사항)**
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" OctXXIII.app
```

## 배포

### Windows
- `OctXXIII.msi` 파일을 배포
- 사용자는 MSI 파일을 실행하여 설치

### macOS
- `OctXXIII.dmg` 파일을 배포
- 사용자는 DMG를 마운트하고 앱을 Applications 폴더로 드래그

## 주의사항

1. **FFmpeg 라이선스**: FFmpeg는 GPL 라이선스입니다
2. **코드 서명**: macOS에서 배포하려면 Apple Developer 계정이 필요할 수 있습니다
3. **바이러스 검사**: Windows Defender가 실행 파일을 차단할 수 있습니다

## 지원 플랫폼

- Windows 10/11 (64-bit)
- macOS 10.15+ (Intel/Apple Silicon)

## 빌드 시간

- Windows: 약 5-10분
- macOS: 약 5-10분

(인터넷 속도에 따라 FFmpeg 다운로드 시간이 달라집니다)