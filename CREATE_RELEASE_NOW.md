# 🚀 GitHub Release 생성 가이드

## 방법 1: 웹에서 직접 생성 (권장)

### 단계별 가이드

1. **릴리즈 페이지로 이동**
   ```
   https://github.com/octxxiii/Nobody3/releases/new
   ```

2. **태그 선택**
   - "Choose a tag" 드롭다운에서 `v1.0.0` 선택
   - 또는 "Create new tag: v1.0.0" 클릭

3. **릴리즈 제목 입력**
   ```
   Nobody 3 v1.0.0
   ```

4. **릴리즈 설명 입력**
   - 아래 파일 내용을 복사해서 붙여넣기:
   - `RELEASE_NOTES_v1.0.0.md` 파일 열기
   - 전체 내용 복사
   - GitHub 릴리즈 설명란에 붙여넣기

5. **바이너리 파일 업로드**
   - "Attach binaries by dropping them here or selecting them" 영역 클릭
   - 또는 드래그 앤 드롭
   - 파일: `releases/Nobody3-Windows.zip` (248MB)
   - 업로드 완료까지 시간이 걸릴 수 있습니다 (약 1-2분)

6. **릴리즈 발행**
   - "Publish release" 버튼 클릭
   - 완료!

---

## 방법 2: GitHub CLI 사용 (자동화)

### GitHub CLI 설치
```powershell
# Windows (winget)
winget install --id GitHub.cli

# 또는 Chocolatey
choco install gh
```

### 릴리즈 생성
```powershell
cd C:\dev\Nobody3
gh release create v1.0.0 `
  --title "Nobody 3 v1.0.0" `
  --notes-file RELEASE_NOTES_v1.0.0.md `
  releases/Nobody3-Windows.zip
```

---

## 방법 3: Python 스크립트 사용 (토큰 필요)

### GitHub Personal Access Token 생성
1. https://github.com/settings/tokens 접속
2. "Generate new token" → "Generate new token (classic)" 클릭
3. Token name: `Nobody3 Release`
4. Expiration: 원하는 기간 선택
5. Scopes: `repo` 체크
6. "Generate token" 클릭
7. 토큰 복사 (한 번만 표시됨!)

### 환경 변수 설정
```powershell
$env:GITHUB_TOKEN = "your_token_here"
```

### 스크립트 실행
```powershell
cd C:\dev\Nobody3
.venv\Scripts\python.exe create_github_release.py
```

---

## 📋 릴리즈 정보 요약

- **태그**: v1.0.0
- **제목**: Nobody 3 v1.0.0
- **설명**: RELEASE_NOTES_v1.0.0.md 내용
- **바이너리**: releases/Nobody3-Windows.zip (248MB)
- **릴리즈 URL**: https://github.com/octxxiii/Nobody3/releases/tag/v1.0.0

---

## ✅ 완료 확인

릴리즈 생성 후 다음 URL에서 확인:
```
https://github.com/octxxiii/Nobody3/releases
```

---

**가장 간단한 방법은 방법 1 (웹에서 직접 생성)입니다!** 🎉

