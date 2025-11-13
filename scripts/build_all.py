#!/usr/bin/env python3
"""
?„ì²´ ë¹Œë“œ ?„ë¡œ?¸ìŠ¤ ê´€ë¦??¤í¬ë¦½íŠ¸
"""

import sys
import os
import platform
import subprocess

def check_python_version():
    """Python ë²„ì „ ?•ì¸"""
    if sys.version_info < (3, 8):
        print("Python 3.8 ?´ìƒ???„ìš”?©ë‹ˆ??")
        print(f"?„ì¬ ë²„ì „: {sys.version}")
        return False
    return True

def install_build_dependencies():
    """ë¹Œë“œ???„ìš”??ê¸°ë³¸ ?¨í‚¤ì§€ ?¤ì¹˜"""
    print("ê¸°ë³¸ ë¹Œë“œ ?˜ì¡´???¤ì¹˜ ì¤?..")
    
    packages = ["cx_Freeze", "Pillow"]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"??{package} ?¤ì¹˜??)
        except subprocess.CalledProcessError as e:
            print(f"??{package} ?¤ì¹˜ ?¤íŒ¨: {e}")
            return False
    
    return True

def create_icons():
    """?„ì´ì½??ì„±"""
    print("?„ì´ì½??ì„± ì¤?..")
    try:
        subprocess.run([sys.executable, "create_icon.py"], check=True)
        print("???„ì´ì½??ì„± ?„ë£Œ")
        return True
    except subprocess.CalledProcessError:
        print("???„ì´ì½??ì„± ?¤íŒ¨ (? íƒ?¬í•­?´ë?ë¡?ê³„ì† ì§„í–‰)")
        return True

def build_for_platform():
    """?Œë«?¼ë³„ ë¹Œë“œ ?¤í–‰"""
    system = platform.system()
    
    if system == "Windows":
        print("Windows??ë¹Œë“œ ?œì‘...")
        try:
            subprocess.run([sys.executable, "build_windows.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Windows ë¹Œë“œ ?¤íŒ¨: {e}")
            return False
            
    elif system == "Darwin":
        print("macOS??ë¹Œë“œ ?œì‘...")
        try:
            subprocess.run([sys.executable, "build_macos.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"macOS ë¹Œë“œ ?¤íŒ¨: {e}")
            return False
            
    else:
        print(f"ì§€?í•˜ì§€ ?ŠëŠ” ?Œë«?? {system}")
        print("Windows ?ëŠ” macOS?ì„œ ?¤í–‰?´ì£¼?¸ìš”.")
        return False

def main():
    """ë©”ì¸ ë¹Œë“œ ?„ë¡œ?¸ìŠ¤"""
    print("=" * 50)
    print("Nobody 3 ?µí•© ë¹Œë“œ ?œìŠ¤??)
    print("=" * 50)
    print()
    
    # ?œìŠ¤???•ë³´ ì¶œë ¥
    print(f"?Œë«?? {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print()
    
    # ?¨ê³„ë³?ë¹Œë“œ ?¤í–‰
    steps = [
        ("Python ë²„ì „ ?•ì¸", check_python_version),
        ("ë¹Œë“œ ?˜ì¡´???¤ì¹˜", install_build_dependencies),
        ("?„ì´ì½??ì„±", create_icons),
        ("?Œë«?¼ë³„ ë¹Œë“œ", build_for_platform),
    ]
    
    for step_name, step_func in steps:
        print(f"[{step_name}]")
        if not step_func():
            print(f"??{step_name} ?¤íŒ¨")
            return 1
        print()
    
    print("=" * 50)
    print("??ëª¨ë“  ë¹Œë“œ ê³¼ì •???„ë£Œ?˜ì—ˆ?µë‹ˆ??")
    print("=" * 50)
    
    # ê²°ê³¼ ?Œì¼ ?ˆë‚´
    system = platform.system()
    if system == "Windows":
        print("?ì„±???Œì¼:")
        print("- build/exe.win-amd64-3.x/ (?¤í–‰ ?Œì¼)")
        print("- Nobody 3.msi (?¤ì¹˜ ?Œì¼)")
    elif system == "Darwin":
        print("?ì„±???Œì¼:")
        print("- Nobody 3.app (??ë²ˆë“¤)")
        print("- Nobody 3.dmg (?¤ì¹˜ ?Œì¼)")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\në¹Œë“œê°€ ì¤‘ë‹¨?˜ì—ˆ?µë‹ˆ??")
        sys.exit(1)
    except Exception as e:
        print(f"\n?ˆìƒì¹?ëª»í•œ ?¤ë¥˜: {e}")
        sys.exit(1)
