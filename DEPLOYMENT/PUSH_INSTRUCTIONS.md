# GitHub 푸시 지침

## ✅ 완료된 작업

1. ✅ `.gitignore` 업데이트 완료
2. ✅ 임시 파일 Git에서 제거 완료
3. ✅ 새 파일들 스테이징 완료
4. ✅ 커밋 완료
5. ✅ 릴리즈 태그 생성 완료

## 🚀 다음 단계: GitHub에 푸시

### 현재 브랜치 확인
```bash
git branch --show-current
```

### 푸시 명령어

#### 메인 브랜치 푸시
```bash
# main 브랜치인 경우
git push -u origin main

# master 브랜치인 경우
git push -u origin master
```

#### 태그 푸시
```bash
git push origin v2.0.0
```

또는 모든 태그 푸시:
```bash
git push origin --tags
```

## 📦 GitHub Releases 설정

푸시 완료 후:

1. **GitHub 저장소로 이동**: https://github.com/octxxiii/Nobody3
2. **Releases 페이지**: https://github.com/octxxiii/Nobody3/releases
3. **"Draft a new release" 클릭**
4. **태그 선택**: `v2.0.0`
5. **제목**: `Nobody 3 v2.0.0`
6. **릴리즈 노트** (아래 내용 복사):

```markdown
## Nobody 3 v2.0.0 - Initial Public Release

### Features
- ✨ Cross-platform support (Windows/macOS/Linux)
- 🌐 Integrated browser for YouTube, YouTube Music, SoundCloud
- 📋 Format selection with quality indicators
- 🎵 Mini player mode with always-on-top option
- 🎨 Dark theme UI
- 🔒 Security improvements (SSL verification, input validation)
- ⚡ FFmpeg automatic download and bundling (Windows)

### Technical
- Built with PyQt5 for native performance
- MVP architecture with service layer
- Comprehensive error handling and logging
- Security-focused design

### Downloads
- **Windows**: Download `Nobody3-Windows.zip` from Releases
- **macOS**: Build from source (see README)
- **Linux**: Build from source (see README)

### Installation
1. Download the release for your platform
2. Extract the archive
3. Run the executable

### Documentation
See [README.md](README.md) for detailed documentation.

### Security
This release includes security improvements:
- SSL/TLS certificate verification enabled
- URL validation to prevent SSRF attacks
- Filename sanitization to prevent path traversal

### Contributing
Contributions welcome! Please see the repository for details.
```

7. **바이너리 첨부**:
   - `releases/Nobody3-Windows.zip` 업로드
   - (macOS/Linux 빌드 후 추가 가능)

8. **"Publish release" 클릭**

## ✅ 완료 확인

- [ ] Git 푸시 완료
- [ ] 태그 푸시 완료
- [ ] GitHub Releases 생성 완료
- [ ] 바이너리 업로드 완료
- [ ] 릴리즈 노트 작성 완료

## 🔗 유용한 링크

- **저장소**: https://github.com/octxxiii/Nobody3
- **Releases**: https://github.com/octxxiii/Nobody3/releases
- **Issues**: https://github.com/octxxiii/Nobody3/issues
- **README**: https://github.com/octxxiii/Nobody3/blob/main/README.md

