# Nobody 3 - YouTube/Music Converter & Player

<div align="center">

![Nobody 3](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-green.svg)
![License](https://img.shields.io/badge/license-Open%20Source-lightgrey.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**크로스 플랫폼 개인 미디어 관리자 및 플레이어**

[English](README.md) | [한국어](README.ko.md)

[기능](#-주요-기능) • [설치](#-설치) • [사용법](#-사용법) • [개발](#-개발) • [기여](#-기여)

</div>

---

## 📖 프로젝트 소개

Nobody 3는 YouTube, YouTube Music, SoundCloud를 하나의 GUI에서 탐색하고 플레이리스트 단위로 음악을 다운로드/재생하기 위해 만든 개인 프로젝트입니다. 혼자 쓰던 도구였지만, 더 많은 사람들이 활용할 수 있도록 공유 가능한 구조로 정리했습니다.

---

## 📸 스크린샷

### 메인 인터페이스
![메인 인터페이스](docs/screenshots/main_interface.png)
*통합 브라우저와 비디오 테이블이 있는 메인 창*

### 포맷 선택
![포맷 선택](docs/screenshots/format_selection.png)
*품질 표시기가 있는 포맷 선택 테이블*

### 미니 플레이어
![미니 플레이어](docs/screenshots/mini_player.png)
*항상 위에 표시되는 옵션이 있는 컴팩트 미니 플레이어*

### 설정 다이얼로그
![설정 다이얼로그](docs/screenshots/settings_dialog.png)
*접을 수 있는 섹션이 있는 설정 다이얼로그*

---

## 📁 저장소 구조

```
.
├── Nobody/            # 애플리케이션 소스 패키지
├── docs/              # 사용자/빌드/개선 문서
├── scripts/           # 빌드 및 배포 스크립트
├── dist/              # 빌드 산출물 (Nobody 3.exe 등)
├── legacy/            # 이전 버전 및 참고 자료
├── plans/             # 작업 계획 문서
├── tests/             # pytest 기반 단위 테스트
├── README.md          # 이 문서 (영어)
├── README.ko.md       # 이 문서 (한국어)
└── requirements.txt   # 파이썬 의존성 목록
```

### 배포 산출물 (`dist/`)

```
dist/
├── build/             # 기존 빌드 결과 (Nobody 3.exe 포함)
└── build_new/         # 최신 빌드 산출물
    ├── Nobody 3.exe   # 메인 실행 파일
    ├── python312.dll  # 내장 파이썬 런타임
    ├── resources_rc.py
    └── lib/           # 의존성 라이브러리
```

---

## ✨ 주요 기능

### 핵심 기능
- **내장 브라우저**: YouTube / YouTube Music / SoundCloud 탐색 및 재생
- **포맷 필터**: 비디오/오디오 포맷 표시 제어, 최대 해상도 제한
- **다운로드 관리**: 선택 포맷으로 일괄 다운로드, 진행 상황 표시
- **미니 플레이어**: 창 최소화와 상관없이 항상 위에서 제어 가능
- **자동 FFmpeg 처리**: 실행 시 필요한 경우 백그라운드 다운로드
- **로깅 & 설정**: 사용자별 캐시에 로그/설정 저장

### 2025 업데이트
- ✨ 미니 플레이어 모드 및 항상 위에 표시 옵션
- 🔧 향상된 포맷 선택 UI
- 📦 FFmpeg 포함 빌드 (Windows)
- 🌐 개선된 크로스 플랫폼 호환성
- 🔐 보안 개선 (입력 검증, 경로 정리)

---

## 🛠️ 설치

### 방법 1: 사전 빌드된 실행 파일 (권장)

플랫폼별 최신 릴리즈 다운로드:

- **Windows**: [다운로드 `Nobody3-Windows.zip`](https://github.com/octxxiii/Nobody3/releases)
- **macOS**: [다운로드 `Nobody3-macOS.zip`](https://github.com/octxxiii/Nobody3/releases)
- **Linux**: [다운로드 `Nobody3-Linux.tar.gz`](https://github.com/octxxiii/Nobody3/releases)

**Windows**: 압축 해제 후 `Nobody3.exe` 실행  
**macOS**: 압축 해제 후 `Nobody3.app` 열기  
**Linux**: 압축 해제 후 `./Nobody3` 실행

### 방법 2: 소스에서 빌드

#### 필수 요구사항
- Python 3.12 이상
- pip

#### 단계
```bash
# 저장소 클론
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3

# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python -m Nobody.main
```

#### 실행 파일 빌드
```bash
# Windows
pyinstaller --clean --noconfirm Nobody3.spec

# macOS/Linux
chmod +x build_macos.sh  # 또는 build_linux.sh
./build_macos.sh
```

---

## 📖 사용법

### 기본 워크플로우

1. **앱 실행**: 실행 파일 실행 또는 `python -m Nobody.main`
2. **콘텐츠 탐색**: 통합 브라우저를 사용하여 비디오/음악 찾기
3. **URL 복사**: "CopyURL" 버튼 클릭 또는 URL 수동 붙여넣기
4. **포맷 선택**: 테이블에서 원하는 포맷 선택
5. **다운로드**: 다운로드 버튼 클릭하여 선택한 디렉토리에 저장

### 미니 플레이어

- 최소화 버튼을 클릭하여 미니 플레이어 모드로 전환
- 핀 버튼으로 항상 위에 표시 토글
- 창 전환 없이 재생 제어

### 포맷 설정

설정 메뉴를 통해 포맷 필터 접근:
- 비디오 포맷 표시/숨기기
- 오디오 포맷 표시/숨기기
- 최대 품질/해상도 설정

---

## 🏗️ 아키텍처

```
Nobody/
├── main.py                 # 애플리케이션 진입점
├── config/                 # 설정
│   └── constants.py       # 테마 및 상수
├── models/                 # 도메인 모델
│   └── settings.py        # 앱 설정
├── services/               # 백그라운드 워커
│   ├── searcher.py        # 메타데이터 가져오기
│   ├── downloader.py      # 다운로드 워커
│   └── ffmpeg_checker.py  # FFmpeg 다운로드
├── utils/                  # 유틸리티
│   ├── cache.py           # 캐시 디렉토리 도우미
│   ├── logging.py         # 로깅 설정
│   ├── ffmpeg.py          # FFmpeg 발견
│   └── security.py        # 보안 유틸리티
└── views/                  # UI 컴포넌트
    ├── main_window.py     # 메인 창
    ├── mini_player.py     # 미니 플레이어 컨트롤러
    ├── video_table.py     # 테이블 관리자
    ├── presenter.py       # 비즈니스 로직
    └── layout_builder.py  # UI 레이아웃
```

### 디자인 패턴

- **MVP (Model-View-Presenter)**: 관심사 분리
- **서비스 레이어**: QThread의 백그라운드 작업
- **유틸리티 레이어**: 재사용 가능한 도우미 함수

---

## 🔧 개발

### 개발 환경 설정

```bash
# 클론 및 설치
git clone https://github.com/octxxiii/Nobody3.git
cd Nobody3
pip install -r requirements.txt

# 테스트 실행
pytest

# 로깅과 함께 실행
python -m Nobody.main
```

### 프로젝트 구조

```
.
├── Nobody/            # 애플리케이션 소스 패키지
├── docs/              # 문서
├── scripts/           # 빌드 및 배포 스크립트
├── tests/             # 단위 테스트 (pytest)
├── legacy/            # 레거시 코드 (참고용)
└── releases/          # 릴리즈 패키지
```

### 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=Nobody

# 특정 테스트 파일 실행
pytest tests/test_video_table.py
```

### 로깅

로그는 다음 위치에 기록됩니다:
- **Windows**: `%LOCALAPPDATA%\Nobody 3\Caches\nobody3.log`
- **macOS**: `~/Library/Caches/Nobody 3/nobody3.log`
- **Linux**: `~/.cache/Nobody 3/nobody3.log`

---

## 🔒 보안

### 구현된 보안 기능

- ✅ **SSL/TLS 검증**: 인증서 확인 활성화
- ✅ **URL 검증**: SSRF 보호, 프로토콜 화이트리스트
- ✅ **파일명 정리**: 경로 순회 방지
- ✅ **입력 검증**: 사용자 입력 정리

자세한 내용은 [SECURITY_AUDIT.md](SECURITY_AUDIT.md)를 참조하세요.

---

## 📦 의존성

- **PyQt5** (5.15.10): GUI 프레임워크
- **PyQtWebEngine** (≥5.15.7): 내장 브라우저
- **yt-dlp** (≥2023.12.30): 미디어 추출
- **requests** (≥2.31.0): HTTP 클라이언트
- **FFmpeg**: 미디어 처리 (Windows에서 자동 다운로드)

---

## 🤝 기여

기여를 환영합니다! Pull Request를 자유롭게 제출해주세요.

### 기여 방법

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

### 코드 스타일

- Python 코드는 PEP 8 준수
- 가능한 경우 타입 힌트 사용
- 공개 함수/클래스에 docstring 추가
- 새 기능에 대한 테스트 작성

---

## 📝 라이선스

이 프로젝트는 오픈소스입니다. 책임감 있게 사용하고 저작권법을 존중해주세요.

**중요**: 이 도구는 개인 사용 목적으로만 사용하세요. 다운로드한 콘텐츠는 원 저작자의 저작권이 있습니다. 무단 배포 또는 상업적 사용은 불법입니다.

---

## 🙏 감사의 말

- **yt-dlp**: 미디어 추출 엔진
- **FFmpeg**: 미디어 처리
- **PyQt5**: GUI 프레임워크
- **Python 커뮤니티**: 훌륭한 도구와 라이브러리

---

## 📞 지원

- **Issues**: [GitHub Issues](https://github.com/octxxiii/Nobody3/issues)
- **Discussions**: [GitHub Discussions](https://github.com/octxxiii/Nobody3/discussions)

---

## 🔧 FFmpeg 취급 방식

실행 시 `Nobody/utils/ffmpeg.py`의 `find_ffmpeg_executable()`이 다음 순서로 FFmpeg를 찾습니다.

1. 패키징된 경우: 실행 파일과 같은 폴더 (`Nobody 3.exe`와 동일 위치)
2. 개발 중인 경우: 프로젝트 루트 (`C:\dev\Nobody3\ffmpeg.exe` 등)
3. 현재 작업 디렉터리
4. 시스템 PATH

**없다면?** `FFmpegChecker`가 백그라운드에서 자동 다운로드 후 동일 위치에 저장합니다.

**즉, 함께 배포하지 않아도 되지만** 인터넷 접근이 어려운 환경이면 `ffmpeg.exe`/`ffprobe.exe`를 실행 파일과 같은 폴더에 포함하는 것이 안전합니다. 자동 설치가 막힌 환경에서도 곧바로 사용할 수 있습니다.

---

## 📚 문서 모음 (docs/)

- `docs/사용자_가이드.md` : GUI 사용법 (국문)
- `docs/빌드_가이드.md` : 개발자용 빌드 절차 (국문)
- `docs/BUILD_README.md` : 빌드 개요 (영문)

그 외 개선 계획/보고서는 `docs/` 폴더에서 확인하세요.

---

## ✅ 테스트 & 품질

```bash
# 단위 테스트 실행
pytest
```

현재는 `VideoTableManager` 등 핵심 모듈에 대한 테스트가 포함되어 있으며, 지속적으로 보강 예정입니다.

실행 로그는 사용자 캐시 경로(`%LOCALAPPDATA%/Nobody 3/Caches`)에 기록됩니다.

---

## 🗂 legacy 폴더

- `legacy/Nobody3.py` : 리팩터링 전 모놀리식 버전 (참고용)
- `legacy/OctXXIII_v2.0/` : 이전 빌드 결과물 및 문서 (명칭 유지)

---

## 🧭 향후 개선 방향

- Presenter/Manager 단위 테스트 확장
- 멀티다운로드 큐 UI 개선
- 자동 업데이트 채널 검토

---

<div align="center">

**Made with ❤️ by nobody**

⭐ 이 저장소가 유용하다면 스타를 눌러주세요!

</div>

