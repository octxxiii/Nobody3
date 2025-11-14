# 스크린샷 플레이스홀더

## 현재 상태

스크린샷 자동 캡처를 시도했지만, GUI 애플리케이션의 완전 자동화는 제한적입니다.

## 해결 방법

### 방법 1: 애플리케이션에서 직접 캡처 (가장 쉬움)

1. Nobody 3 실행
2. 각 화면으로 이동
3. **Ctrl+S** 누르기 (스크린샷 자동 저장)
4. 파일명을 적절하게 변경:
   - `screenshot_*.png` → `main_interface.png`
   - `screenshot_*.png` → `format_selection.png`
   - `screenshot_*.png` → `mini_player.png`
   - `screenshot_*.png` → `settings_dialog.png`

### 방법 2: Windows Snipping Tool 사용

1. Nobody 3 실행
2. `Windows + Shift + S` 누르기
3. 영역 선택
4. `docs/screenshots/`에 저장

### 방법 3: 수동 스크립트 실행

```bash
python scripts/simple_capture.py
```

그 후 애플리케이션에서 Ctrl+S 사용

## 추가된 기능

- **Ctrl+S 단축키**: 애플리케이션에서 스크린샷 캡처
- **자동 저장**: `docs/screenshots/` 폴더에 자동 저장
- **타임스탬프**: 파일명에 타임스탬프 자동 추가

## 다음 단계

스크린샷을 캡처한 후:
```bash
git add docs/screenshots/*.png
git commit -m "docs: add screenshots"
git push origin main
```

