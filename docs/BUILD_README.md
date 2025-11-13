# Nobody 3 λΉλ“ κ°€?΄λ“

FFmpegλ¥??¬ν•¨???¤μΉ ?μΌ???μ„±?λ” λ°©λ²•?…λ‹??

## ?„μ” μ΅°κ±΄

### Windows
- Python 3.8 ?΄μƒ
- pip
- WiX Toolset (MSI ?μ„±?? ? νƒ?¬ν•­)
  - ?¤μ΄λ΅λ“: https://wixtoolset.org/releases/

### macOS
- Python 3.8 ?΄μƒ
- pip
- Xcode Command Line Tools
  ```bash
  xcode-select --install
  ```

## λΉλ“ λ°©λ²•

### Windows?μ„ λΉλ“

1. **?λ™ λΉλ“ (κ¶μ¥)**
   ```cmd
   build.bat
   ```

2. **?λ™ λΉλ“**
   ```cmd
   python build_windows.py
   ```

### macOS?μ„ λΉλ“

1. **?λ™ λΉλ“ (κ¶μ¥)**
   ```bash
   ./build.sh
   ```

2. **?λ™ λΉλ“**
   ```bash
   python3 build_macos.py
   ```

## λΉλ“ κ³Όμ •

### ?λ™?Όλ΅ ?ν–‰?λ” ?‘μ—…:

1. **FFmpeg ?¤μ΄λ΅λ“**
   - Windows: μµμ‹  Windows??FFmpeg λ°”μ΄?λ¦¬
   - macOS: Apple Silicon/Intel λ§μ¶¤ FFmpeg λ°”μ΄?λ¦¬

2. **?μ΅΄???¤μΉ**
   - PyQt5
   - yt-dlp
   - requests
   - cx_Freeze (λΉλ“ ?„κµ¬)

3. **?¤ν–‰ ?μΌ ?μ„±**
   - λª¨λ“  ?μ΅΄?±μ„ ?¬ν•¨???…λ¦½ ?¤ν–‰ ?μΌ

4. **?¤μΉ ?μΌ ?μ„±**
   - Windows: MSI ?¤μΉ ?μΌ
   - macOS: DMG ?¤μΉ ?μΌ

## ?μ„±?λ” ?μΌ

### Windows
- `build/exe.win-amd64-3.x/` - ?¤ν–‰ ?μΌ ?΄λ”
- `Nobody 3.msi` - MSI ?¤μΉ ?μΌ

### macOS
- `Nobody 3.app` - ??λ²λ“¤
- `Nobody 3.dmg` - DMG ?¤μΉ ?μΌ

## λ¬Έμ  ?΄κ²°

### Windows

**WiX Toolset ?†μ**
- MSI ?μΌ???μ„±?μ? ?μ?λ§??¤ν–‰ ?μΌ?€ ?•μƒ ?μ„±?©λ‹??
- WiX Toolset ?¤μΉ ???¤μ‹ λΉλ“?μ„Έ??

**FFmpeg ?¤μ΄λ΅λ“ ?¤ν¨**
- ?Έν„°???°κ²°???•μΈ?μ„Έ??
- λ°©ν™”λ²½μ΄ ?¤μ΄λ΅λ“λ¥?μ°¨λ‹¨?μ? ?λ”μ§€ ?•μΈ?μ„Έ??

### macOS

**κ¶ν• ?¤λ¥**
```bash
chmod +x build.sh
sudo xattr -rd com.apple.quarantine Nobody 3.app
```

**DMG ?μ„± ?¤ν¨**
- dmgbuild ?¨ν‚¤μ§€κ°€ ?¤μΉ?μ? ?μ? κ²½μ°:
```bash
pip3 install dmgbuild
```

**???λª… (? νƒ?¬ν•­)**
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" Nobody 3.app
```

## λ°°ν¬

### Windows
- `Nobody 3.msi` ?μΌ??λ°°ν¬
- ?¬μ©?λ” MSI ?μΌ???¤ν–‰?μ—¬ ?¤μΉ

### macOS
- `Nobody 3.dmg` ?μΌ??λ°°ν¬
- ?¬μ©?λ” DMGλ¥?λ§μ΄?Έν•κ³??±μ„ Applications ?΄λ”λ΅??λκ·?

## μ£Όμ?¬ν•­

1. **FFmpeg ?Όμ΄? μ¤**: FFmpeg??GPL ?Όμ΄? μ¤?…λ‹??
2. **μ½”λ“ ?λª…**: macOS?μ„ λ°°ν¬?λ ¤λ©?Apple Developer κ³„μ •???„μ”?????μµ?λ‹¤
3. **λ°”μ΄?¬μ¤ κ²€??*: Windows Defenderκ°€ ?¤ν–‰ ?μΌ??μ°¨λ‹¨?????μµ?λ‹¤

## μ§€???λ«??

- Windows 10/11 (64-bit)
- macOS 10.15+ (Intel/Apple Silicon)

## λΉλ“ ?κ°„

- Windows: ??5-10λ¶?
- macOS: ??5-10λ¶?

(?Έν„°???λ„???°λΌ FFmpeg ?¤μ΄λ΅λ“ ?κ°„???¬λΌμ§‘λ‹??
