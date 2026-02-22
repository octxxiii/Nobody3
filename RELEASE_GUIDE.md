# GitHub 릴리즈 생성 가이드

## exe 빌드 (한 번에 전달용)

Python/모듈이 없는 PC에 전달할 때는 **단일 exe(onefile)**로 빌드한 뒤 그 exe를 zip에 넣어 릴리즈에 올리면 됩니다.

### 1. exe 빌드

프로젝트 루트에서:

```powershell
# 의존성 설치 (최초 1회)
pip install -r requirements.txt
pip install -r requirements-build.txt

# 빌드 (onefile = exe 하나에 전부 포함)
.\build_exe.ps1
```

- **결과**: `dist\Nobody3.exe` 한 파일. 이 exe만 넣은 zip이 `releases\Nobody3-Windows-v1.0.2-YYYYMMDD.zip` 에 생성됩니다.
- **전달 방법**: zip 받아서 압축 해제 후 `Nobody3.exe` 더블클릭 (Python/설치 불필요).
- **FFmpeg**: exe와 같은 폴더에 없으면 앱이 첫 실행 시 자동 다운로드 시도 (기존 로직 유지).

### 2. GitHub 릴리즈에 올리기

아래 "방법 1" 또는 "방법 2"로 릴리즈를 만든 뒤, **Attach binaries**에 `releases\Nobody3-Windows-v1.0.2-YYYYMMDD.zip` 를 업로드하면 됩니다.

---

## 방법 1: 자동 생성 (스크립트 사용)

### 1. GitHub Personal Access Token 생성
1. https://github.com/settings/tokens 접속
2. "Generate new token" → "Generate new token (classic)" 클릭
3. Note: "Nobody3 Release" 입력
4. Expiration: 원하는 기간 선택
5. Scopes: `repo` 체크 (전체 권한)
6. "Generate token" 클릭
7. 생성된 토큰을 복사 (한 번만 표시됨!)

### 2. 환경 변수 설정
PowerShell에서:
```powershell
$env:GITHUB_TOKEN = "your_token_here"
```

또는 영구적으로 설정:
```powershell
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token_here", "User")
```

### 3. 릴리즈 생성 스크립트 실행
```powershell
python create_release.py
```

## 방법 2: 수동 생성 (GitHub 웹사이트)

1. https://github.com/octxxiii/Nobody3/releases/new 접속
2. "Choose a tag"에서 `v1.0.1` 선택 (이미 생성됨)
3. "Release title": `Nobody 3 v1.0.1 - WebEngine Crash Fix`
4. "Describe this release"에 `RELEASE_NOTES_v1.0.1.md` 내용 복사/붙여넣기
5. "Attach binaries"에서 `releases/Nobody3-v1.0.1-20251126.zip` 파일 업로드
6. "Publish release" 클릭

## 준비된 파일들

- ✅ 릴리즈 노트: `RELEASE_NOTES_v1.0.1.md`
- ✅ 릴리즈 패키지: `releases/Nobody3-v1.0.1-20251126.zip`
- ✅ Git 태그: `v1.0.1` (이미 푸시됨)
- ✅ 릴리즈 스크립트: `create_release.py`

