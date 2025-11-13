# Nobody - MVP 구조 리팩터링 버전

이 디렉터리는 Nobody3.py를 MVP (Model-View-Presenter) 구조로 리팩터링한 버전입니다.

## 📁 디렉터리 구조

```
Nobody/
├── __init__.py              # 패키지 초기화
├── main.py                  # 애플리케이션 진입점
├── config/                  # 설정 및 상수
│   ├── __init__.py
│   └── constants.py         # DARK_THEME_STYLESHEET 등
├── utils/                   # 유틸리티 함수
│   ├── __init__.py
│   ├── cache.py            # 캐시 디렉터리 관련
│   ├── logging.py          # 로깅 시스템
│   └── ffmpeg.py           # FFmpeg 관련 유틸리티
├── models/                  # 데이터 모델
│   ├── __init__.py
│   └── settings.py         # AppSettings 클래스
├── services/                # 백그라운드 서비스 (스레드)
│   ├── __init__.py
│   ├── ffmpeg_checker.py   # FFmpeg 체크 및 다운로드
│   ├── searcher.py         # 비디오 검색
│   └── downloader.py       # 비디오 다운로드
└── views/                   # UI 컴포넌트
    ├── __init__.py
    ├── main_window.py       # VideoDownloader (메인 윈도우)
    ├── format_settings_dialog.py  # FormatSettingsDialog
    ├── settings_dialog.py   # SettingsDialog
    └── components.py        # CheckBoxHeader, VideoHandler, MainThreadSignalEmitter
```

## 🚀 사용 방법

### 현재 상태
- ✅ utils 모듈 분리 완료
- ✅ models 모듈 분리 완료
- ✅ services 모듈 분리 완료
- ✅ config 모듈 분리 완료
- ✅ views 모듈 분리 완료
- ✅ main.py 독립 실행 가능 (Nobody3.py 의존성 제거)

### 실행 방법
```bash
# 프로젝트 루트에서 (권장)
python -m Nobody.main

# 또는 Nobody 디렉터리에서
cd Nobody
python main.py
```

**중요**: 프로젝트 루트(Nobody3 디렉터리)에서 실행해야 FFmpeg와 아이콘 파일을 찾을 수 있습니다.

## 📝 리팩터링 진행 상황

### 완료된 작업
1. **utils 모듈**: 로깅, 캐시, FFmpeg 유틸리티 분리
2. **models 모듈**: AppSettings 클래스 분리
3. **services 모듈**: FFmpegChecker, Searcher, Downloader 분리
4. **config 모듈**: 상수 및 스타일시트 분리

### 완료된 작업 (추가)
5. **views 모듈**: 모든 UI 컴포넌트 분리 완료
   - ✅ FormatSettingsDialog → format_settings_dialog.py
   - ✅ SettingsDialog → settings_dialog.py
   - ✅ CheckBoxHeader, VideoHandler, MainThreadSignalEmitter → components.py
   - ✅ VideoDownloader → main_window.py

### 향후 계획
1. VideoDownloader를 여러 작은 컴포넌트로 분리
2. 완전한 MVP 패턴 적용
3. 의존성 주입 패턴 적용
4. 단위 테스트 추가

## 🔄 Nobody3.py와의 관계

- **Nobody3.py**: 원본 파일 (그대로 유지, 독립 실행 가능)
- **Nobody/**: 리팩터링된 MVP 구조 버전 (독립 실행 가능)
- **두 버전 모두 독립적으로 실행 가능하며 서로 의존하지 않음**

## 📚 참고

- MVP 패턴: Model-View-Presenter 아키텍처
- 각 모듈은 독립적으로 테스트 가능하도록 설계
- 의존성은 최소화하여 유지보수성 향상

