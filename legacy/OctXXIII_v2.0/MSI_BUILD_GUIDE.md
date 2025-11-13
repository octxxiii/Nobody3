# Nobody 3 MSI ë¹Œë“œ ê°€?´ë“œ

## ê°œìš”
??ê°€?´ë“œ??Nobody 3 ? í”Œë¦¬ì??´ì…˜??Windows MSI ?¤ì¹˜ ?Œì¼ë¡?ë¹Œë“œ?˜ëŠ” ë°©ë²•???¤ëª…?©ë‹ˆ??

## ?„ìš” ì¡°ê±´

### ?„ìˆ˜ ?”êµ¬?¬í•­
- Windows 10/11
- Python 3.8 ?´ìƒ
- Git (? íƒ?¬í•­)

### ê¶Œì¥ ?„êµ¬ (? íƒ?¬í•­)
1. **Advanced Installer** (ê°€???„ë¬¸?ì¸ MSI)
   - ?¤ìš´ë¡œë“œ: https://www.advancedinstaller.com/
   - 30??ë¬´ë£Œ ì²´í—˜???¬ìš© ê°€??

2. **Inno Setup** (EXE ?¤ì¹˜ ?Œì¼)
   - ?¤ìš´ë¡œë“œ: https://jrsoftware.org/isinfo.php
   - ?„ì „ ë¬´ë£Œ

## ë¹Œë“œ ë°©ë²•

### ë°©ë²• 1: ?ë™ ë¹Œë“œ ?¤í¬ë¦½íŠ¸ ?¬ìš© (ê¶Œì¥)

1. **ë°°ì¹˜ ?Œì¼ ?¤í–‰**
   ```cmd
   build_msi.bat
   ```

2. **?ëŠ” Python ?¤í¬ë¦½íŠ¸ ì§ì ‘ ?¤í–‰**
   ```cmd
   python build_msi.py
   ```

### ë°©ë²• 2: ê¸°ì¡´ ë¹Œë“œ ?œìŠ¤???¬ìš©

1. **?„ì²´ ë¹Œë“œ**
   ```cmd
   python build_all.py
   ```

2. **Windows ?„ìš© ë¹Œë“œ**
   ```cmd
   python build_windows.py
   ```

3. **cx_Freeze ?¬ìš©**
   ```cmd
   python setup.py bdist_msi
   ```

## ë¹Œë“œ ?µì…˜

### 1. Advanced Installer (ê¶Œì¥)
- ê°€???„ë¬¸?ì¸ MSI ?Œì¼ ?ì„±
- ?¬ìš©???•ì˜ ?¤ì¹˜ ?µì…˜
- ?”ì????œëª… ì§€??
- ?ë™ ?…ë°?´íŠ¸ ì§€??

### 2. cx_Freeze
- ê°„ë‹¨??MSI ?ì„±
- ë¬´ë£Œ
- ê¸°ë³¸?ì¸ ?¤ì¹˜ ê¸°ëŠ¥

### 3. Inno Setup
- EXE ?¤ì¹˜ ?Œì¼ ?ì„±
- ë¬´ë£Œ?´ë©° ë§¤ìš° ?ˆì •??
- ?¤êµ­??ì§€??
- ?¬ìš©???•ì˜ ?¤ì¹˜ ?”ë©´

## ?ì„±?˜ëŠ” ?Œì¼

ë¹Œë“œ ?„ë£Œ ???¤ìŒ ?Œì¼?¤ì´ ?ì„±?©ë‹ˆ??

```
dist/
?œâ??€ Nobody 3/                 # PyInstaller ?¤í–‰ ?Œì¼ ?´ë”
??  ?œâ??€ Nobody 3.exe         # ë©”ì¸ ?¤í–‰ ?Œì¼
??  ?œâ??€ ffmpeg.exe           # FFmpeg ë°”ì´?ˆë¦¬
??  ?”â??€ ... (ê¸°í? ?¼ì´ë¸ŒëŸ¬ë¦?
?œâ??€ Nobody 3.msi            # MSI ?¤ì¹˜ ?Œì¼ (Advanced Installer/cx_Freeze)
?”â??€ Nobody 3-setup.exe      # EXE ?¤ì¹˜ ?Œì¼ (Inno Setup)
```

## ë¬¸ì œ ?´ê²°

### ?¼ë°˜?ì¸ ë¬¸ì œ

1. **Python ëª¨ë“ˆ ?„ë½**
   ```cmd
   pip install -r requirements.txt
   ```

2. **PyQt5 ?¤ì¹˜ ?¤ë¥˜**
   ```cmd
   pip install --upgrade pip
   pip install PyQt5==5.15.10
   ```

3. **FFmpeg ?„ë½**
   - `ffmpeg.exe`ë¥??„ë¡œ?íŠ¸ ë£¨íŠ¸??ë³µì‚¬
   - ?ëŠ” `build_windows.py`ê°€ ?ë™?¼ë¡œ ?¤ìš´ë¡œë“œ

4. **ê¶Œí•œ ?¤ë¥˜**
   - ê´€ë¦¬ì ê¶Œí•œ?¼ë¡œ ëª…ë ¹ ?„ë¡¬?„íŠ¸ ?¤í–‰

### ë¹Œë“œ ?¤íŒ¨ ??

1. **?˜ì¡´???¬ì„¤ì¹?*
   ```cmd
   pip uninstall -y PyQt5 pyinstaller cx-Freeze
   pip install -r requirements.txt
   ```

2. **ë¹Œë“œ ?´ë” ?•ë¦¬**
   ```cmd
   rmdir /s build
   rmdir /s dist
   del *.spec
   ```

3. **ê°€?í™˜ê²??¬ìš©**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python build_msi.py
   ```

## ê³ ê¸‰ ?¤ì •

### ?„ì´ì½?ë³€ê²?
- `icon.ico` ?Œì¼???„ë¡œ?íŠ¸ ë£¨íŠ¸??ë°°ì¹˜
- 32x32, 48x48, 256x256 ?¬ê¸° ?¬í•¨ ê¶Œì¥

### ë²„ì „ ?•ë³´ ?˜ì •
`build_msi.py` ?Œì¼?ì„œ ?¤ìŒ ê°’ë“¤???˜ì •:
```python
self.version = "1.0.0"        # ë²„ì „ ë²ˆí˜¸
self.author = "nobody"        # ?œì‘??
self.description = "..."      # ?¤ëª…
```

### ì¶”ê? ?Œì¼ ?¬í•¨
PyInstaller spec ?Œì¼??`datas` ?¹ì…˜??ì¶”ê?:
```python
datas=[
    ('resources_rc.py', '.'),
    ('config.json', '.'),      # ì¶”ê? ?Œì¼
    ('docs/', 'docs/'),        # ?´ë” ?„ì²´
],
```

## ë°°í¬

?ì„±??MSI ?ëŠ” EXE ?Œì¼???¬ìš©?ì—ê²?ë°°í¬?????ˆìŠµ?ˆë‹¤:

1. **MSI ?Œì¼**: Windows Installerë¥??µí•œ ?œì? ?¤ì¹˜
2. **EXE ?Œì¼**: ?¬ìš©???•ì˜ ?¤ì¹˜ ë§ˆë²•??

## ?¼ì´? ìŠ¤

??ë¹Œë“œ ?¤í¬ë¦½íŠ¸??Nobody 3 ?„ë¡œ?íŠ¸?€ ?™ì¼???¼ì´? ìŠ¤ë¥??°ë¦…?ˆë‹¤.
