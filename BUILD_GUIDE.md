# Nobody 3 빌드 가이드

## Windows 빌드

```bash
# 1. PyInstaller 설치
pip install pyinstaller Pillow

# 2. 빌드 실행
pyinstaller --clean --noconfirm Nobody3.spec

# 3. FFmpeg 복사 (선택사항)
copy ffmpeg.exe dist\ffmpeg.exe
copy ffprobe.exe dist\ffprobe.exe

# 4. 패키지 생성
python create_release_package.py
```

결과: `releases/Nobody3-Windows.zip`

## macOS 빌드

```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 빌드 실행
pyinstaller --clean --noconfirm Nobody3.spec

# 3. 패키지 생성
python create_release_package.py
```

결과: `releases/Nobody3-macOS.zip`

## Linux 빌드

```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 빌드 실행
pyinstaller --clean --noconfirm Nobody3.spec

# 3. 패키지 생성
python create_release_package.py
```

결과: `releases/Nobody3-Linux.tar.gz`

## 테스트

각 플랫폼에서 생성된 실행 파일을 테스트하세요:

### Windows
```bash
cd releases\Nobody3-Windows
Nobody3.exe
```

### macOS
```bash
cd releases
unzip Nobody3-macOS.zip
open Nobody3.app
```

### Linux
```bash
cd releases
tar -xzf Nobody3-Linux.tar.gz
cd Nobody3-Linux
./Nobody3
```

## 포함된 파일

- 실행 파일 (Nobody3.exe / Nobody3.app / Nobody3)
- FFmpeg 바이너리 (Windows만 포함)
- README.txt (Windows만 포함)

