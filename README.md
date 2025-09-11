# OctXXIII - YouTube/Music Converter & Player

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-GPL-red)

YouTube와 SoundCloud에서 음악을 스트리밍하고 다운로드할 수 있는 PyQt5 기반 애플리케이션입니다.

## ✨ 주요 기능

### 🎵 스트리밍 & 플레이어
- YouTube, YouTube Music, SoundCloud 통합 브라우저
- 웹 기반 음악 재생 컨트롤
- **미니 플레이어 모드** - 최소화 시 작은 플레이어 창으로 전환
- 최상위 고정 토글 기능
- 실시간 제목 표시 및 스크롤

### 📥 다운로드 기능
- 단일 비디오 및 플레이리스트 다운로드
- 다양한 포맷 지원 (MP4, MP3 등)
- 썸네일 미리보기
- 제목 편집 가능
- 선택적 다운로드 (체크박스)
- 경로 지정 다운로드

### 🎨 사용자 인터페이스
- 다크 테마 기본 적용
- 분할 창 레이아웃 (브라우저 + 다운로드)
- 브라우저 숨기기/보이기 토글
- 반응형 UI 디자인

## 🚀 미니 플레이어

최소화 시 자동으로 작은 플레이어 창(300x120)으로 전환됩니다.

**미니 플레이어 기능:**
- ⏮️ 이전 트랙
- ⏯️ 재생/일시정지
- ⏭️ 다음 트랙  
- 📌/📍 최상위 고정 토글
- 🔼 원래 크기로 복원

## 📦 설치 및 빌드

### 빠른 시작

#### Windows (설치 파일 사용)
1. [Releases](https://github.com/octxxiii/Nobody3/releases)에서 최신 `OctXXIII-Setup-v2.0.exe` 다운로드
2. 설치 파일 실행하여 자동 설치
3. 바탕화면 바로가기로 실행

#### Windows (소스에서 빌드)
```cmd
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
pyinstaller --onefile --windowed --name OctXXIII Nobody3.py
install.bat
```

#### macOS
```bash
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
chmod +x build.sh
./build.sh
```

### 수동 설치

1. **저장소 클론**
   ```bash
   git clone https://github.com/octxxiii/Nobody3.git
   cd Nobody3
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **실행**
   ```bash
   # Windows
   python Nobody3.py
   
   # macOS
   python3 Nobody3.py
   ```

### 배포용 빌드

FFmpeg를 포함한 독립 실행 파일을 생성합니다:

```bash
python build_all.py
```

**생성되는 파일:**
- Windows: `OctXXIII.exe` (실행 파일) + `install.bat` (설치 스크립트)
- macOS: `OctXXIII.dmg` (설치 파일)

자세한 빌드 가이드는 [BUILD_README.md](BUILD_README.md)를 참조하세요.

## 🛠️ 기술 스택

- **GUI**: PyQt5
- **다운로드**: yt-dlp
- **미디어 처리**: FFmpeg
- **웹 엔진**: QWebEngineView
- **빌드**: cx_Freeze

## 📋 시스템 요구사항

### Windows
- Windows 10/11 (64-bit)
- Python 3.8+
- 4GB RAM 권장

### macOS
- macOS 10.15+
- Python 3.8+
- Intel 또는 Apple Silicon
- 4GB RAM 권장

## 🎯 사용법

1. **스트리밍**
   - 내장 브라우저에서 YouTube/SoundCloud 접속
   - 플레이어 컨트롤로 재생 제어
   - 최소화하면 미니 플레이어 모드 활성화

2. **다운로드**
   - URL 입력 또는 📋 버튼으로 현재 페이지 URL 복사
   - 🔍 버튼으로 비디오 정보 검색
   - 원하는 비디오 선택 후 📥 다운로드

3. **미니 플레이어**
   - 창 최소화 시 자동 활성화
   - 📌 버튼으로 최상위 고정 토글
   - 🔼 버튼으로 원래 크기 복원

## 🔧 개발

### 개발 환경 설정
```bash
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
pip install -r requirements.txt
python create_icon.py  # 아이콘 생성
```

### 프로젝트 구조
```
Nobody3/
├── Nobody3.py           # 메인 애플리케이션 파일
├── resources_rc.py      # Qt 리소스 파일
├── requirements.txt     # Python 의존성
├── setup.py            # 빌드 설정
├── build_all.py        # 통합 빌드 스크립트
├── build_windows.py    # Windows 빌드
├── build_macos.py      # macOS 빌드
├── install.bat         # Windows 설치 스크립트
├── uninstall.bat       # Windows 제거 스크립트
├── installer.iss       # Inno Setup 스크립트
└── BUILD_README.md     # 빌드 가이드
```

## 📝 라이선스

이 프로젝트는 GPL 라이선스 하에 배포됩니다. FFmpeg 포함으로 인한 라이선스 제약이 있습니다.

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 있거나 제안사항이 있으시면 [Issues](https://github.com/octxxiii/Nobody3/issues)에 등록해주세요.

## 🎉 업데이트 히스토리

### v1.0 (2024-04-08)
- ✅ 미니 플레이어 모드 추가
- ✅ 최상위 고정 토글 기능
- ✅ 최대화 버튼 활성화
- ✅ FFmpeg 포함 빌드 시스템
- ✅ 크로스 플랫폼 지원

### 이전 버전들
- 240405: 클립보드 복사, 새로고침, SoundCloud 지원
- 240401: 브라우저 숨기기, YouTube Music 지원
- 240328: 브라우저 통합, 테마 시스템
- 240327: 플레이리스트 지원, URL 관리
- 240326: 기본 다운로드 기능, 썸네일 지원

---

**Created by nobody 😜**  
**Distribution date: 2024-04-01**