# PyInstaller runtime hook: set QtWebEngine process path for --onefile bundle.
# Runs before the main script so Qt finds QtWebEngineProcess.exe in _MEIPASS.
import os
import sys

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    base = sys._MEIPASS
    # PyInstaller puts QtWebEngineProcess in PyQt5/Qt/bin (Windows)
    for name in ("QtWebEngineProcess.exe", "QtWebEngineProcess"):
        path = os.path.join(base, "PyQt5", "Qt", "bin", name)
        if os.path.isfile(path):
            os.environ["QTWEBENGINEPROCESS_PATH"] = path
            break
    else:
        # Fallback: point to bin dir so Qt can search for the process
        bin_dir = os.path.join(base, "PyQt5", "Qt", "bin")
        if os.path.isdir(bin_dir):
            os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(bin_dir, "QtWebEngineProcess.exe")
