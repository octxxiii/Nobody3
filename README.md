# Nobody 3 - YouTube/Music Converter & Player

## 📖 프로젝트 소개

Nobody 3는 YouTube, YouTube Music, SoundCloud를 하나의 GUI에서 탐색하고 플레이리스트 단위로 음악을 다운로드/재생하기 위해 만든 개인 프로젝트입니다. 혼자 쓰던 도구였지만, 더 많은 사람들이 활용할 수 있도록 공유 가능한 구조로 정리했습니다.

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
├── README.md          # 이 문서
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

- **내장 브라우저**: YouTube / YouTube Music / SoundCloud 탐색 및 재생
- **포맷 필터**: 비디오/오디오 포맷 표시 제어, 최대 해상도 제한
- **다운로드 관리**: 선택 포맷으로 일괄 다운로드, 진행 상황 표시
- **미니 플레이어**: 창 최소화와 상관없이 항상 위에서 제어 가능
- **자동 FFmpeg 처리**: 실행 시 필요한 경우 백그라운드 다운로드
- **로깅 & 설정**: 사용자별 캐시에 로그/설정 저장

---

## 🛠️ 실행 방법

### 1) 개발 환경

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python -m Nobody.main
```

### 2) 빌드 & 배포 (Windows 예시)

```bash
# scripts/ 에서 실행
python scripts/build_windows.py
```

결과물은 `dist/build_new/Nobody 3.exe`와 `lib/` 폴더로 제공됩니다.

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

## 📦 배포 체크 리스트

1. `dist/build_new/` 내용 확인 (Nobody 3.exe, lib/ 등)
2. 필요한 경우 `ffmpeg.exe`/`ffprobe.exe` 추가 포함
3. `docs/사용자_가이드.md` 등 문서 동봉
4. `requirements.txt`는 개발자 참고용으로만 제공

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

## 👤 개발자 정보

- **Creator**: nobody 😜
- **Last Updated**: 2025-01-11
- **문의**: GitHub Issues / Pull Request

---

> 💡 **팁**: 안정적인 인터넷 연결이 어렵다면, 배포 시 `ffmpeg.exe`와 `ffprobe.exe`를 실행 파일과 함께 제공하세요. 자동 다운로드가 불가능한 환경에서도 즉시 사용할 수 있습니다.
