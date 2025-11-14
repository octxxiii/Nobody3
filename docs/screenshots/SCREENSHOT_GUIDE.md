# 스크린샷 가이드

## 필요한 스크린샷

다음 4개의 스크린샷을 준비하세요:

### 1. main_interface.png
- **위치**: 메인 창 전체 화면
- **포함 내용**:
  - 통합 브라우저 (YouTube/SoundCloud)
  - 비디오 테이블 (포맷 목록)
  - 다운로드 패널
  - 다크 테마 적용 상태
- **권장 크기**: 1920x1080 또는 1280x720

### 2. format_selection.png
- **위치**: 포맷 선택 테이블 확대
- **포함 내용**:
  - 포맷 목록 (MP3, MP4, WebM 등)
  - 품질 표시기
  - 파일 크기 정보
  - 체크박스 선택 상태
- **권장 크기**: 1280x720

### 3. mini_player.png
- **위치**: 미니 플레이어 모드
- **포함 내용**:
  - 컴팩트한 미니 플레이어 창
  - 재생 컨트롤 (재생/일시정지, 이전/다음)
  - 볼륨 슬라이더
  - 항상 위에 표시 옵션 (핀 버튼)
- **권장 크기**: 800x200

### 4. settings_dialog.png
- **위치**: 설정 다이얼로그
- **포함 내용**:
  - 접을 수 있는 섹션들
  - 한영 전환 버튼
  - 후원 링크 버튼
  - 캐시 관리
- **권장 크기**: 800x600

## 스크린샷 촬영 팁

1. **다크 테마 사용**: 모든 스크린샷은 다크 테마로 촬영
2. **깔끔한 상태**: 불필요한 창이나 정보는 제거
3. **고해상도**: 최소 1280x720, 권장 1920x1080
4. **PNG 형식**: 투명도가 필요하면 PNG, 아니면 JPG도 가능
5. **민감한 정보**: 개인 정보나 민감한 URL은 가리기

## 파일 이름 규칙

- `main_interface.png`
- `format_selection.png`
- `mini_player.png`
- `settings_dialog.png`

## 업로드 방법

1. 스크린샷 촬영
2. `docs/screenshots/` 폴더에 저장
3. Git에 추가 및 커밋:
   ```bash
   git add docs/screenshots/*.png
   git commit -m "docs: add screenshots for README"
   git push origin main
   ```

