# GitHub Release 생성 가이드

## v1.0.0 릴리즈 생성

### 1. GitHub 웹사이트에서 릴리즈 생성

1. https://github.com/octxxiii/Nobody3 로 이동
2. **Releases** 섹션 클릭
3. **"Create a new release"** 또는 **"Draft a new release"** 클릭

### 2. 릴리즈 정보 입력

- **Tag**: `v1.0.0` 선택 (이미 생성됨)
- **Release title**: `Nobody 3 v1.0.0`
- **Description**: 아래 내용 복사/붙여넣기

```markdown
# Nobody 3 v1.0.0

## 🎉 Initial Release

This is the first stable release of Nobody 3 (OctXXIII v2.0).

## ✨ Features

### Core Functionality
- **YouTube & SoundCloud Downloader**: Download videos and audio from YouTube and SoundCloud
- **Built-in Browser**: Integrated web browser for easy navigation
- **Format Selection**: Choose from multiple video/audio formats
- **Playlist Support**: Download entire playlists
- **Thumbnail Preview**: Visual preview of videos in the download list

### Mini Player Mode
- **Compact Player**: Switch to mini player mode for minimal interface
- **Always-on-Top Toggle**: Keep the mini player on top of other windows
- **Volume Control**: Adjust playback volume
- **Playback Controls**: Play, pause, next, previous controls

### User Interface
- **Dark Theme**: Modern dark theme for comfortable viewing
- **Bilingual Support**: Korean and English language support
- **Responsive Layout**: Adjustable splitter layout
- **Customizable Settings**: Format preferences and quality settings

### Technical Features
- **FFmpeg Integration**: Built-in FFmpeg for media processing
- **Cross-Platform**: Windows, macOS, and Linux support
- **Cache Management**: Built-in cache clearing functionality
- **Error Handling**: Robust error handling and user feedback

## 📦 Installation

### Windows
1. Download `Nobody3-Windows.zip` below
2. Extract to your desired location
3. Run `Nobody3.exe`
4. FFmpeg is included in the package

### macOS
1. Download `Nobody3-macOS.dmg` (or `.zip`) below
2. Extract and run the application
3. FFmpeg is included in the package

### Linux
1. Download `Nobody3-Linux.tar.gz` below
2. Extract and run the executable
3. FFmpeg is included in the package

## ⚠️ Important Notes

- **Personal Use Only**: This tool is for personal use only
- **Copyright**: Downloaded content is copyrighted by original creators
- **Legal**: Unauthorized distribution or commercial use is illegal
- **Responsibility**: Please respect copyright laws and use responsibly

## 📅 Release Date

2025-01-03

---

**Made with ❤️ by nobody**
```

### 3. 바이너리 파일 업로드

**Attach binaries** 섹션에서 다음 파일들을 드래그 앤 드롭:

- `releases/Nobody3-Windows.zip` (248MB - GitHub Releases는 2GB까지 지원)
- macOS 빌드가 있다면: `releases/Nobody3-macOS.dmg` 또는 `.zip`
- Linux 빌드가 있다면: `releases/Nobody3-Linux.tar.gz`

### 4. 릴리즈 발행

- **"Publish release"** 클릭

### 5. (선택) Pre-release로 설정

- 아직 베타/알파라면 **"Set as a pre-release"** 체크

---

## GitHub CLI를 사용하는 경우

```bash
gh release create v1.0.0 \
  --title "Nobody 3 v1.0.0" \
  --notes-file RELEASE_NOTES_v1.0.0.md \
  releases/Nobody3-Windows.zip
```

주의: Windows zip 파일이 248MB이므로 GitHub CLI로 업로드할 때 시간이 걸릴 수 있습니다.

