# OctXXIII v2.0 - 실행파일 배포

## 📖 프로젝트 소개

이 프로그램은 개인적인 취미 프로젝트로 시작되었습니다. 저는 이 프로그램을 혼자 개발하여 오랫동안 만족스럽게 사용해 왔습니다. 플레이어와 다운로더로 활용하면서, 개인적인 취미로 플레이리스트를 만들어 SoundCloud에 업로드하는 데 많은 도움이 되었습니다. 이제는 더 많은 사람들과 공유하고 싶어 배포를 결정하게 되었습니다.

## 📁 저장소 구조

```
.
├── Nobody/            # 애플리케이션 소스 코드 (패키지)
├── docs/              # 사용자/빌드/개선 문서 모음
├── scripts/           # 빌드 및 배포 스크립트
├── dist/              # 빌드 산출물 (실행 파일 등)
├── legacy/            # 이전 버전 및 참고용 파일
├── plans/             # 작업 계획 문서
├── tests/             # pytest 기반 단위 테스트
├── README.md          # 현재 문서
└── requirements.txt   # 파이썬 의존성 목록
```

## 📦 배포 파일 목록

### 실행파일
- `OctXXIII.exe` - 메인 애플리케이션
- `ffmpeg.exe` - 비디오/오디오 변환 도구
- `ffprobe.exe` - 미디어 정보 분석 도구

### 문서
- `docs/사용자_가이드.md` - 사용자 매뉴얼 (국문)
- `docs/빌드_가이드.md` - 개발자용 빌드 가이드 (국문)
- `docs/BUILD_README.md` - 빌드 개요 (영문)
- 그 외 문서는 `docs/` 폴더 참조 (개선 계획/보고서 등)

## 🚀 설치 및 실행

### 시스템 요구사항
- **운영체제**: Windows 10/11 (64비트)
- **메모리**: 최소 4GB RAM 권장
- **저장공간**: 500MB 이상 여유 공간
- **인터넷**: 안정적인 인터넷 연결

### 설치 방법
1. 모든 파일을 같은 폴더에 저장
2. `OctXXIII.exe` 더블클릭하여 실행
3. 첫 실행 시 Windows Defender 경고가 나타날 수 있음 (정상)

### 실행 방법
```bash
# 명령줄에서 실행
OctXXIII.exe

# 또는 더블클릭으로 실행
```

## 🎮 주요 기능

### ✨ 새로워진 기능 (v2.0)
- **미니 플레이어**: 최소화 시 자동 전환
- **최상위 고정**: 미니 플레이어 항상 위에 표시
- **FFmpeg 내장**: 별도 설치 불필요
- **크로스 플랫폼**: Windows, macOS, Linux 지원

### 🎵 핵심 기능
- YouTube, YouTube Music, SoundCloud 지원
- 다양한 포맷 다운로드 (MP3, MP4, WebM, M4A)
- 플레이리스트 전체 다운로드
- 실시간 미디어 컨트롤
- 포맷 설정 및 필터링
- 다크 테마 인터페이스

## 📋 사용법 요약

### 기본 사용법
1. **실행**: `OctXXIII.exe` 더블클릭
2. **브라우저**: 내장 브라우저에서 원하는 영상 찾기
3. **복사**: 📋 버튼으로 URL 자동 복사
4. **선택**: 원하는 포맷 선택
5. **다운로드**: 📥 버튼으로 다운로드 시작

### 미니 플레이어 사용법
- 창 최소화 시 자동으로 미니 플레이어로 전환
- 📌 버튼으로 최상위 고정 토글
- 🔼 버튼으로 원래 크기로 복원
- 재생 컨트롤 및 볼륨 조절 가능

## ⚙️ 설정

### 포맷 설정
- ⚙️ 버튼 클릭하여 설정 창 열기
- 기본 포맷 선택 (mp3, mp4, webm, m4a, best)
- 표시할 포맷 타입 선택
- 최대 품질 제한 설정

### 브라우저 컨트롤
- 👈👉 이전/다음 페이지
- 🔄 새로고침
- 🏠 YouTube 홈
- 🎵 YouTube Music
- 🎧 SoundCloud
- 🦕 브라우저 숨기기/보이기

## 🔧 FFmpeg 배포 가이드

### FFmpeg 포함 방법

이 프로그램은 오디오/비디오 변환을 위해 FFmpeg를 사용합니다. 배포 시 FFmpeg를 포함하는 방법은 다음과 같습니다:

#### 방법 1: 자동 빌드 스크립트 사용 (권장)

**Windows:**
```bash
python build_windows.py
```
이 스크립트는 자동으로 FFmpeg를 다운로드하고 `ffmpeg/windows/` 폴더에 저장합니다.

**macOS:**
```bash
python build_macos.py
```
이 스크립트는 자동으로 FFmpeg를 다운로드하고 `ffmpeg/macos/` 폴더에 저장합니다.

#### 방법 2: 수동 다운로드

1. **Windows용 FFmpeg 다운로드:**
   - https://github.com/BtbN/FFmpeg-Builds/releases 에서 최신 Windows 빌드 다운로드
   - 압축 해제 후 `ffmpeg.exe`와 `ffprobe.exe`를 `ffmpeg/windows/` 폴더에 복사

2. **macOS용 FFmpeg 다운로드:**
   - https://evermeet.cx/ffmpeg/ 에서 다운로드
   - `ffmpeg`와 `ffprobe`를 `ffmpeg/macos/` 폴더에 복사
   - 실행 권한 부여: `chmod +x ffmpeg/macos/ffmpeg ffmpeg/macos/ffprobe`

#### 방법 3: setup.py를 통한 자동 포함

`setup.py`는 빌드 시 자동으로 다음 경로에서 FFmpeg를 찾아 포함합니다:
- Windows: `ffmpeg/windows/ffmpeg.exe`, `ffmpeg/windows/ffprobe.exe`
- macOS: `ffmpeg/macos/ffmpeg`, `ffmpeg/macos/ffprobe`

빌드 명령:
```bash
python setup.py build
```

빌드된 실행파일과 같은 디렉토리에 `ffmpeg.exe` (또는 `ffmpeg`)가 포함됩니다.

### 배포 시 주의사항

1. **FFmpeg 라이선스**: FFmpeg는 GPL 라이선스를 따릅니다. 배포 시 라이선스 준수를 확인하세요.
2. **파일 위치**: 실행파일과 FFmpeg 바이너리는 같은 폴더에 있어야 합니다.
3. **경로 설정**: 프로그램은 실행파일과 같은 디렉토리에서 `ffmpeg`를 찾습니다.

## 🔧 문제 해결

### 일반적인 문제
1. **실행 안됨**: 관리자 권한으로 실행 시도
2. **다운로드 실패**: 인터넷 연결 확인
3. **포맷 없음**: 다른 포맷 선택 시도
4. **느린 속도**: 캐시 정리 (💬 → Clear Cache)
5. **FFmpeg 오류**: FFmpeg 바이너리가 실행파일과 같은 폴더에 있는지 확인

### Windows Defender 경고
- 첫 실행 시 "Windows에서 이 앱의 실행을 차단했습니다" 경고가 나타날 수 있음
- "추가 정보" → "실행" 클릭하여 실행
- 또는 Windows Defender에서 예외 추가

## 📁 파일 구조

### 저장소 루트
```
.
├── Nobody/            # 메인 소스 패키지
├── docs/              # 사용자/빌드/개선 문서
├── scripts/           # 빌드 및 배포 스크립트 모음
├── dist/              # 빌드 산출물 (실행 파일 등)
├── legacy/            # 이전 버전 및 참고 자료
├── plans/             # 작업 계획 문서
├── tests/             # 단위 테스트
├── README.md          # 현재 문서
└── requirements.txt   # 파이썬 의존성 목록
```

### 배포 산출물 (`dist/`)
```
dist/
├── build/             # 기존 빌드 출력물 (OctXXIII.exe 등)
└── build_new/         # 최신 빌드 출력물
    ├── OctXXIII.exe   # 메인 실행 파일
    ├── python312.dll  # Python 런타임
    ├── resources_rc.py
    └── lib/           # 의존성 라이브러리
```

## 🆕 업데이트 내역

### v2.0 (2025-01-03)
- 미니 플레이어 모드 추가
- 최상위 고정 토글 기능
- 최대화 버튼 활성화
- FFmpeg 포함 빌드 시스템
- 크로스 플랫폼 지원

### v1.0 (2024-04-08)
- 기본 다운로드 기능
- 브라우저 통합
- 플레이리스트 지원
- SoundCloud 지원

## 👨‍💻 개발자 정보
- **Creator**: nobody 😜
- **Last Updated**: 2025-01-03
- **Version**: 2.0

## 📞 지원 및 문의
- 문제 발생 시 GitHub Issues를 통해 문의
- 기능 요청 및 버그 리포트 환영
- 사용자 피드백을 통한 지속적인 개선

---

**OctXXIII v2.0** - YouTube/Music Converter & Player  
*Made with ❤️ by nobody*

> 💡 **팁**: 최상의 사용 경험을 위해 안정적인 인터넷 연결을 유지하고, 정기적으로 캐시를 정리해주세요.