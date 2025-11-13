# 루트 디렉터리 정리 계획

## 목표
- 문서/스크립트/레거시 파일을 폴더별로 정리
- 사용하지 않는 파일 제거 또는 legacy 보관
- tests 및 Nobody 패키지 구조는 유지

## 단계별 작업
1. 문서 정리
   - `docs/` 디렉터리 생성
   - 다음 파일/폴더 이동: `IMPROVEMENT_PLAN.md`, `IMPROVEMENT_REPORT.md`, `INDEPENDENCE_PLAN.md`, `REFACTORING_REPORT.md`, `BUILD_README.md`, `MSI_BUILD_GUIDE.md`, `빌드_가이드.md`, `빌드_스크립트_가이드.md`, `빌드_진행_가이드.md`, `사용자_가이드.md`
   - `Nobody/INDEPENDENCE_STATUS.md`도 `docs/`로 이동

2. 스크립트 정리
   - `scripts/` 디렉터리 생성
   - 빌드/배포 관련 스크립트 이동: `build_all.py`, `build_windows.py`, `build_macos.py`, `build.bat`, `build.sh`, `create_icon.py`, `create_windows_icon.py`, `install.bat`, `uninstall.bat`, `setup.py`

3. 레거시/산출물 정리
   - `legacy/` 디렉터리 생성
   - `Nobody3.py`와 `OctXXIII_v2.0/` 폴더 이동
   - `build/` 및 `build_new/`는 임시 산출물이므로 `dist/` 폴더로 이동하거나 정리 (필요 시)

4. 불필요 파일 확인 및 삭제
   - 중복 `resources_rc.py` 존재 여부 확인
   - 더 이상 사용하지 않는 로그/임시 파일 삭제 (`build_log.txt` 등)

5. 테스트
   - 이동 후 `pytest` 다시 실행
   - `python -m Nobody.main` 실행 확인

6. 문서 업데이트
   - 루트 `README.md`에 새 디렉터리 구조 반영
