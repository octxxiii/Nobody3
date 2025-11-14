"""Simple screenshot capture - just run the app and use Ctrl+S."""

import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent.parent
screenshots_dir = project_root / "docs" / "screenshots"
screenshots_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Nobody 3 Screenshot Capture Helper")
print("=" * 60)
print("\nStarting Nobody 3...")
print("\nINSTRUCTIONS:")
print("1. Wait for the application to load")
print("2. Navigate to each screen you want to capture")
print("3. Press Ctrl+S to take a screenshot")
print("4. Screenshots will be saved to: docs/screenshots/")
print("\nRequired screenshots:")
print("  - main_interface.png (Main window)")
print("  - format_selection.png (After searching a URL)")
print("  - mini_player.png (Click mini player button)")
print("  - settings_dialog.png (Click info button)")
print("\n" + "=" * 60)
print("\nStarting application...\n")

# Start the application
subprocess.Popen(
    [sys.executable, "-m", "Nobody.main"],
    cwd=str(project_root)
)

print("Application started!")
print("\nUse Ctrl+S in the application to capture screenshots.")
print("Close this window when done capturing.")

