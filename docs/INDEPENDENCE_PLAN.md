# Nobody 모듈 독립 실행 계획

**작성일**: 2025-01-11  
**목표**: Nobody 폴더만으로 완전히 독립 실행 가능하도록 만들기

## 📋 작업 계획

### Phase 1: 의존성 제거 ✅
- [x] main.py에서 Nobody3.py 임포트 제거
- [x] main.py에서 Nobody.views.VideoDownloader 임포트로 변경
- [x] main_window.py에서 남은 main 코드 제거

### Phase 2: 누락된 의존성 확인 및 수정
- [ ] yt_dlp 임포트 확인
- [ ] 모든 외부 라이브러리 임포트 확인
- [ ] 상대 경로 임포트 검증
- [ ] resources_rc 처리 확인

### Phase 3: 실행 테스트
- [ ] 기본 실행 테스트
- [ ] 오류 수정
- [ ] 기능 동작 확인

## ✅ 완료된 작업

1. **main.py 수정**
   - Nobody3.py 의존성 제거
   - Nobody.views.VideoDownloader 임포트로 변경

2. **main_window.py 정리**
   - 남은 main 코드 블록 제거
   - print 문을 logger로 변경

## 🔍 확인 필요 사항

### 1. yt_dlp 임포트
- services/searcher.py와 services/downloader.py에서 사용
- 외부 라이브러리이므로 requirements.txt에 포함 필요

### 2. resources_rc
- 현재 선택적 임포트로 처리됨 (없어도 동작)
- 확인 필요: 실제로 필요한지

### 3. 아이콘 파일 경로
- main.py에서 "icon.ico", "st2.icns" 등을 찾음
- 프로젝트 루트 기준으로 찾아야 함

### 4. FFmpeg 경로
- utils/ffmpeg.py에서 find_ffmpeg_executable()이 __file__ 기준으로 경로 찾음
- Nobody 모듈 구조에 맞게 수정 필요할 수 있음

## 🚀 실행 방법

### 프로젝트 루트에서 실행
```bash
python -m Nobody.main
```

### Nobody 디렉터리에서 실행
```bash
cd Nobody
python main.py
```

## 📝 다음 단계

1. 실행 테스트 수행
2. 발생하는 오류 수정
3. 모든 기능 동작 확인
4. 문서 업데이트

