# GitHub 릴리즈 생성 가이드

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

