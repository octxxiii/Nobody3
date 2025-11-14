# 스크린샷 촬영 가이드

## 빠른 시작

### 방법 1: Windows 기본 도구 사용 (가장 쉬움)

1. **Nobody 3 실행**
   ```bash
   python -m Nobody.main
   ```

2. **캡처할 화면으로 이동**

3. **스크린샷 촬영**
   - `Windows + Shift + S` 누르기 (Snipping Tool)
   - 또는 `Alt + Print Screen` (활성 창만)

4. **저장**
   - Paint나 이미지 편집기에서 붙여넣기 (`Ctrl + V`)
   - `docs/screenshots/` 폴더에 적절한 이름으로 저장

### 방법 2: 스크립트 사용

```bash
# 간단한 캡처 도구 실행
python scripts/capture_screenshots_simple.py

# 또는 수동 도우미 실행
python scripts/take_screenshots_manual.py
```

## 필요한 스크린샷

### 1. main_interface.png
- **촬영 시점**: 애플리케이션 시작 후 메인 화면
- **포함 내용**:
  - 통합 브라우저 (YouTube/SoundCloud)
  - 비디오 테이블 (포맷 목록)
  - 다운로드 패널
  - 다크 테마 적용 상태

### 2. format_selection.png
- **촬영 시점**: URL 검색 후 포맷 테이블 표시
- **포함 내용**:
  - 포맷 목록 (MP3, MP4, WebM 등)
  - 품질 표시기
  - 파일 크기 정보
  - 체크박스 선택 상태

### 3. mini_player.png
- **촬영 시점**: 미니 플레이어 모드 활성화
- **포함 내용**:
  - 컴팩트한 미니 플레이어 창
  - 재생 컨트롤
  - 볼륨 슬라이더
  - 항상 위에 표시 옵션

### 4. settings_dialog.png
- **촬영 시점**: 설정 다이얼로그 열림
- **포함 내용**:
  - 접을 수 있는 섹션들
  - 한영 전환 버튼
  - 후원 링크 버튼
  - 캐시 관리

## 촬영 팁

1. **해상도**: 최소 1280x720, 권장 1920x1080
2. **형식**: PNG (투명도 지원)
3. **테마**: 다크 테마로 촬영
4. **상태**: 깔끔한 상태로 촬영 (불필요한 창 제거)
5. **개인정보**: 민감한 정보는 가리기

## 파일 저장 위치

모든 스크린샷은 다음 위치에 저장:
```
docs/screenshots/
├── main_interface.png
├── format_selection.png
├── mini_player.png
└── settings_dialog.png
```

## 확인

스크린샷을 추가한 후:
```bash
git add docs/screenshots/*.png
git commit -m "docs: add screenshots for README"
git push origin main
```

