# Screenshots

This directory contains screenshots for the README files.

## Required Screenshots

1. **main_interface.png** - Main window with integrated browser and video table
2. **format_selection.png** - Format selection table with quality indicators
3. **mini_player.png** - Compact mini player with always-on-top option
4. **settings_dialog.png** - Settings dialog with collapsible sections

## How to Take Screenshots

### Method 1: Using Windows Snipping Tool (Recommended)

1. Run Nobody 3 application
2. Navigate to the screen you want to capture
3. Press `Windows + Shift + S` to open Snipping Tool
4. Select the area to capture
5. Save the screenshot to `docs/screenshots/` with the appropriate name

### Method 2: Using Screenshot Helper Script

```bash
# Run the helper script
python scripts/take_screenshots_manual.py

# Follow the instructions in the helper window
```

### Method 3: Manual Capture

1. Run Nobody 3 application
2. Navigate to the screen you want to capture
3. Press `Alt + Print Screen` to capture the active window
4. Open Paint or any image editor
5. Paste (`Ctrl + V`)
6. Crop and save as PNG to `docs/screenshots/`

## Screenshot Requirements

- **Format**: PNG (preferred) or JPG
- **Size**: Minimum 1280x720, recommended 1920x1080
- **Theme**: Dark theme enabled
- **Content**: Clean state, no sensitive information

## Current Status

- [ ] main_interface.png
- [ ] format_selection.png
- [ ] mini_player.png
- [ ] settings_dialog.png

## Note

Screenshots should be taken with:
- Dark theme enabled
- Main window in a clean state
- No sensitive information visible
- Good lighting/contrast for readability
