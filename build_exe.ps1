# Nobody 3 - Build single Windows exe (onefile) for release
# Run from project root: .\build_exe.ps1
# Output: dist\Nobody3.exe (and releases\Nobody3-Windows-<version>.zip)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Nobody 3 - Build exe" -ForegroundColor Cyan
Write-Host ""

# 1. Ensure dependencies
Write-Host "[1/4] Checking dependencies..."
$pipDeps = @("PyQt5", "PyQtWebEngine", "yt-dlp", "requests")
foreach ($d in $pipDeps) {
    $r = pip show $d 2>$null
    if (-not $r) {
        Write-Host "  Installing runtime deps (pip install -r requirements.txt)..."
        pip install -r requirements.txt
        break
    }
}
$pyinst = pip show pyinstaller 2>$null
if (-not $pyinst) {
    Write-Host "  Installing PyInstaller..."
    pip install -r requirements-build.txt
}

# 2. Clean previous build
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "dist")  { Remove-Item -Recurse -Force dist  }

# 3. Build
Write-Host ""
Write-Host "[2/4] Running PyInstaller (onefile)..."
python -m PyInstaller --noconfirm Nobody3.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller failed." -ForegroundColor Red
    exit 1
}

# 4. Result
$exePath = "dist\Nobody3.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "Expected exe not found: $exePath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/4] Build OK: $exePath" -ForegroundColor Green
Write-Host "     Single exe (onefile) - ready to distribute."
Write-Host ""

# 5. Optional: create release zip (single exe inside)
$version = "v1.0.2"
$date = Get-Date -Format "yyyyMMdd"
$zipName = "Nobody3-Windows-$version-$date.zip"
$zipPath = "releases\$zipName"
if (-not (Test-Path "releases")) { New-Item -ItemType Directory -Path "releases" | Out-Null }
Write-Host "[4/4] Creating release zip: $zipPath"
Compress-Archive -Path $exePath -DestinationPath $zipPath -Force
Write-Host "      Done. Upload $zipPath to GitHub Release." -ForegroundColor Green
Write-Host ""
