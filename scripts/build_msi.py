#!/usr/bin/env python3
"""
Nobody 3 MSI ?¤ì¹˜ ?Œì¼ ?ì„± ?¤í¬ë¦½íŠ¸
PyInstaller + Advanced Installer ?ëŠ” cx_Freeze + WiX ?¬ìš©
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

class MSIBuilder:
    def __init__(self):
        self.app_name = "Nobody 3"
        self.version = "1.0.0"
        self.author = "Nobody 3"
        self.description = "YouTube/Music Converter & Player"
        self.main_script = "Nobody3.py"
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        
    def check_dependencies(self):
        """?„ìš”???„êµ¬?¤ì´ ?¤ì¹˜?˜ì–´ ?ˆëŠ”ì§€ ?•ì¸"""
        print("?˜ì¡´???•ì¸ ì¤?..")
        
        # Python ?¨í‚¤ì§€ ?•ì¸
        required_packages = ["PyQt5", "yt-dlp", "requests", "pyinstaller"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"??{package}")
            except ImportError:
                missing_packages.append(package)
                print(f"??{package} (?„ë½)")
        
        if missing_packages:
            print(f"\n?„ë½???¨í‚¤ì§€ ?¤ì¹˜ ì¤? {', '.join(missing_packages)}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        return True
    
    def create_pyinstaller_spec(self):
        """PyInstaller spec ?Œì¼ ?ì„±"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.main_script}'],
    pathex=[],
    binaries=[
        ('ffmpeg.exe', '.') if os.path.exists('ffmpeg.exe') else None,
    ],
    datas=[
        ('resources_rc.py', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtMultimedia',
        'yt_dlp',
        'requests',
        'urllib3',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ë¶ˆí•„?”í•œ ë°”ì´?ˆë¦¬ ?œê±°
a.binaries = [x for x in a.binaries if x[0] is not None]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{self.app_name}',
)
'''
        
        with open(f"{self.app_name}.spec", "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        print(f"??{self.app_name}.spec ?Œì¼ ?ì„±??)
    
    def build_with_pyinstaller(self):
        """PyInstallerë¡??¤í–‰ ?Œì¼ ë¹Œë“œ"""
        print("PyInstallerë¡??¤í–‰ ?Œì¼ ë¹Œë“œ ì¤?..")
        
        self.create_pyinstaller_spec()
        
        cmd = [
            "pyinstaller",
            "--clean",
            "--noconfirm",
            f"{self.app_name}.spec"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PyInstaller ë¹Œë“œ ?¤íŒ¨:")
            print(result.stderr)
            return False
        
        print("??PyInstaller ë¹Œë“œ ?„ë£Œ")
        return True
    
    def create_advanced_installer_project(self):
        """Advanced Installer ?„ë¡œ?íŠ¸ ?Œì¼ ?ì„±"""
        aip_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<DOCUMENT Type="Advanced Installer" CreateVersion="20.0" version="20.0" Modules="simple" RootPath="." Language="en" Id="{{12345678-1234-1234-1234-123456789012}}">
  <COMPONENT cid="caphyon.advinst.msicomp.ProjectOptionsComponent">
    <ROW Name="HiddenItems" Value="AppXProductDetailsComponent;AppXDependenciesComponent;AppXAppDetailsComponent;AppXVisualAssetsComponent;AppXCapabilitiesComponent;AppXAppDeclarationsComponent;AppXUriRulesComponent"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiPropsComponent">
    <ROW Property="AI_BITMAP_DISPLAY_MODE" Value="0"/>
    <ROW Property="ALLUSERS" Value="1"/>
    <ROW Property="ARPCOMMENTS" Value="{self.description}"/>
    <ROW Property="ARPCONTACT" Value="{self.author}"/>
    <ROW Property="ARPHELPLINK" Value="https://github.com/Nobody 3/Nobody3"/>
    <ROW Property="ARPPRODUCTICON" Value="icon.exe" Type="8"/>
    <ROW Property="ARPURLINFOABOUT" Value="https://github.com/Nobody 3/Nobody3"/>
    <ROW Property="Manufacturer" Value="{self.author}"/>
    <ROW Property="ProductCode" Value="1033"/>
    <ROW Property="ProductLanguage" Value="1033"/>
    <ROW Property="ProductName" Value="{self.app_name}"/>
    <ROW Property="ProductVersion" Value="{self.version}"/>
    <ROW Property="SecureCustomProperties" Value="OLDPRODUCTS;AI_NEWERPRODUCTFOUND"/>
    <ROW Property="UpgradeCode" Value="{{87654321-4321-4321-4321-210987654321}}"/>
    <ROW Property="WindowsType9X" MultiBuildValue="DefaultBuild:Windows 9x/ME" ValueLocId="-"/>
    <ROW Property="WindowsType9XDisplay" MultiBuildValue="DefaultBuild:Windows 9x/ME" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT40" MultiBuildValue="DefaultBuild:Windows NT 4.0" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT40Display" MultiBuildValue="DefaultBuild:Windows NT 4.0" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT50" MultiBuildValue="DefaultBuild:Windows 2000" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT50Display" MultiBuildValue="DefaultBuild:Windows 2000" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT5X" MultiBuildValue="DefaultBuild:Windows XP/2003" ValueLocId="-"/>
    <ROW Property="WindowsTypeNT5XDisplay" MultiBuildValue="DefaultBuild:Windows XP/2003" ValueLocId="-"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiDirsComponent">
    <ROW Directory="APPDIR" Directory_Parent="TARGETDIR" DefaultDir="APPDIR:." IsPseudoRoot="1"/>
    <ROW Directory="DesktopFolder" Directory_Parent="TARGETDIR" DefaultDir="DESKTO~1|DesktopFolder" IsPseudoRoot="1"/>
    <ROW Directory="ProgramMenuFolder" Directory_Parent="TARGETDIR" DefaultDir="PROGRA~1|ProgramMenuFolder" IsPseudoRoot="1"/>
    <ROW Directory="SHORTCUTDIR" Directory_Parent="ProgramMenuFolder" DefaultDir="{self.app_name}"/>
    <ROW Directory="TARGETDIR" DefaultDir="SourceDir"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiCompsComponent">
    <ROW Component="APPDIR" ComponentId="{{12345678-1234-1234-1234-123456789013}}" Directory_="APPDIR" Attributes="0"/>
    <ROW Component="ProductInformation" ComponentId="{{12345678-1234-1234-1234-123456789014}}" Directory_="APPDIR" Attributes="4" KeyPath="Version"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiFeatsComponent">
    <ROW Feature="MainFeature" Title="Main Feature" Description="Description" Display="1" Level="1" Directory_="APPDIR" Attributes="0"/>
    <ROW Feature="ProductInformation" Title="Product Information" Description="Product Information" Display="0" Level="1" Directory_="APPDIR" Attributes="0"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiFilesComponent">
    <ROW File="{self.app_name}.exe" Component_="APPDIR" FileName="{self.app_name}.exe" Attributes="0" SourcePath="dist\\{self.app_name}\\{self.app_name}.exe" SelfReg="false" NextFile="Version"/>
    <ROW File="Version" Component_="ProductInformation" FileName="Version" Attributes="0" SourcePath="&lt;AI_STUBS&gt;Version" SelfReg="false"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.MsiFileHashComponent">
    <ROW File_="{self.app_name}.exe" Options="0" HashPart1="0" HashPart2="0" HashPart3="0" HashPart4="0"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.BootstrOptComponent">
    <ROW BootstrOptKey="GlobalOptions" DownloadFolder="[AppDataFolder][|Manufacturer]\\[|ProductName]\\prerequisites" Options="2"/>
  </COMPONENT>
  <COMPONENT cid="caphyon.advinst.msicomp.BuildComponent">
    <ROW BuildKey="DefaultBuild" BuildName="DefaultBuild" BuildOrder="1" BuildType="0" PackageFolder="." PackageFileName="{self.app_name}-{self.version}" Languages="en" InstallationType="4" UseLargeSchema="true"/>
  </COMPONENT>
</DOCUMENT>
'''
        
        with open(f"{self.app_name}.aip", "w", encoding="utf-8") as f:
            f.write(aip_content)
        
        print(f"??{self.app_name}.aip ?„ë¡œ?íŠ¸ ?Œì¼ ?ì„±??)
    
    def build_with_advanced_installer(self):
        """Advanced Installerë¡?MSI ë¹Œë“œ"""
        print("Advanced Installerë¡?MSI ë¹Œë“œ ì¤?..")
        
        # Advanced Installer ?¤ì¹˜ ?•ì¸
        ai_paths = [
            r"C:\Program Files (x86)\Caphyon\Advanced Installer 20.0\bin\x86\AdvancedInstaller.com",
            r"C:\Program Files\Caphyon\Advanced Installer 20.0\bin\x86\AdvancedInstaller.com",
        ]
        
        ai_exe = None
        for path in ai_paths:
            if os.path.exists(path):
                ai_exe = path
                break
        
        if not ai_exe:
            print("Advanced Installerê°€ ?¤ì¹˜?˜ì? ?Šì•˜?µë‹ˆ??")
            print("https://www.advancedinstaller.com/ ?ì„œ ?¤ìš´ë¡œë“œ?˜ì„¸??")
            return False
        
        self.create_advanced_installer_project()
        
        # MSI ë¹Œë“œ
        cmd = [ai_exe, "/build", f"{self.app_name}.aip"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Advanced Installer ë¹Œë“œ ?¤íŒ¨:")
            print(result.stderr)
            return False
        
        print("??MSI ?Œì¼ ?ì„± ?„ë£Œ")
        return True
    
    def create_simple_msi_with_cx_freeze(self):
        """cx_Freeze?€ ê°„ë‹¨??MSI ?ì„±"""
        print("cx_Freezeë¡?ê°„ë‹¨??MSI ?ì„± ì¤?..")
        
        # cx_Freeze ?¤ì¹˜ ?•ì¸
        try:
            import cx_Freeze
        except ImportError:
            print("cx_Freeze ?¤ì¹˜ ì¤?..")
            subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"])
        
        # setup.py ?¤í–‰
        if os.path.exists("setup.py"):
            cmd = [sys.executable, "setup.py", "bdist_msi"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("??cx_Freeze MSI ?ì„± ?„ë£Œ")
                return True
            else:
                print(f"cx_Freeze MSI ?ì„± ?¤íŒ¨: {result.stderr}")
        
        return False
    
    def create_inno_setup_script(self):
        """Inno Setup ?¤í¬ë¦½íŠ¸ ?ì„± (MSI ?€??"""
        iss_content = f'''[Setup]
AppName={self.app_name}
AppVersion={self.version}
AppPublisher={self.author}
AppPublisherURL=https://github.com/Nobody 3/Nobody3
AppSupportURL=https://github.com/Nobody 3/Nobody3
AppUpdatesURL=https://github.com/Nobody 3/Nobody3
DefaultDirName={{autopf}}\\{self.app_name}
DefaultGroupName={self.app_name}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=dist
OutputBaseFilename={self.app_name}-{self.version}-setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "dist\\{self.app_name}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{self.app_name}"; Filename: "{{app}}\\{self.app_name}.exe"
Name: "{{autodesktop}}\\{self.app_name}"; Filename: "{{app}}\\{self.app_name}.exe"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{self.app_name}.exe"; Description: "{{cm:LaunchProgram,{self.app_name}}}"; Flags: nowait postinstall skipifsilent
'''
        
        with open(f"{self.app_name}.iss", "w", encoding="utf-8") as f:
            f.write(iss_content)
        
        print(f"??{self.app_name}.iss ?¤í¬ë¦½íŠ¸ ?ì„±??)
    
    def build_with_inno_setup(self):
        """Inno Setup?¼ë¡œ ?¤ì¹˜ ?Œì¼ ?ì„±"""
        print("Inno Setup?¼ë¡œ ?¤ì¹˜ ?Œì¼ ?ì„± ì¤?..")
        
        # Inno Setup ?¤ì¹˜ ?•ì¸
        iscc_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
        ]
        
        iscc_exe = None
        for path in iscc_paths:
            if os.path.exists(path):
                iscc_exe = path
                break
        
        if not iscc_exe:
            print("Inno Setup???¤ì¹˜?˜ì? ?Šì•˜?µë‹ˆ??")
            print("https://jrsoftware.org/isinfo.php ?ì„œ ?¤ìš´ë¡œë“œ?˜ì„¸??")
            return False
        
        self.create_inno_setup_script()
        
        # ?¤ì¹˜ ?Œì¼ ë¹Œë“œ
        cmd = [iscc_exe, f"{self.app_name}.iss"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Inno Setup ë¹Œë“œ ?¤íŒ¨:")
            print(result.stderr)
            return False
        
        print("???¤ì¹˜ ?Œì¼ ?ì„± ?„ë£Œ")
        return True
    
    def build(self):
        """?„ì²´ ë¹Œë“œ ?„ë¡œ?¸ìŠ¤"""
        print(f"=== {self.app_name} MSI ë¹Œë“œ ?œì‘ ===")
        
        if not self.check_dependencies():
            return False
        
        # 1?¨ê³„: PyInstallerë¡??¤í–‰ ?Œì¼ ë¹Œë“œ
        if not self.build_with_pyinstaller():
            print("?¤í–‰ ?Œì¼ ë¹Œë“œ???¤íŒ¨?ˆìŠµ?ˆë‹¤.")
            return False
        
        # 2?¨ê³„: MSI ?ì„± (?¬ëŸ¬ ë°©ë²• ?œë„)
        print("\nMSI ?ì„± ë°©ë²•??? íƒ?˜ì„¸??")
        print("1. Advanced Installer (ê¶Œì¥)")
        print("2. cx_Freeze (ê°„ë‹¨)")
        print("3. Inno Setup (EXE ?¤ì¹˜ ?Œì¼)")
        
        choice = input("? íƒ (1-3): ").strip()
        
        if choice == "1":
            success = self.build_with_advanced_installer()
        elif choice == "2":
            success = self.build_with_cx_freeze()
        elif choice == "3":
            success = self.build_with_inno_setup()
        else:
            print("?˜ëª»??? íƒ?…ë‹ˆ?? cx_Freezeë¥??¬ìš©?©ë‹ˆ??")
            success = self.create_simple_msi_with_cx_freeze()
        
        if success:
            print(f"\n=== {self.app_name} ë¹Œë“œ ?„ë£Œ! ===")
            print("?ì„±???Œì¼???•ì¸?˜ì„¸??")
            print(f"- dist/{self.app_name}/ (?¤í–‰ ?Œì¼)")
            print("- dist/ (?¤ì¹˜ ?Œì¼)")
        else:
            print("ë¹Œë“œ???¤íŒ¨?ˆìŠµ?ˆë‹¤.")
        
        return success

def main():
    """ë©”ì¸ ?¨ìˆ˜"""
    if sys.platform != "win32":
        print("???¤í¬ë¦½íŠ¸??Windows?ì„œë§??¤í–‰?????ˆìŠµ?ˆë‹¤.")
        return 1
    
    builder = MSIBuilder()
    success = builder.build()
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\në¹Œë“œê°€ ì¤‘ë‹¨?˜ì—ˆ?µë‹ˆ??")
        sys.exit(1)
    except Exception as e:
        print(f"\n?ˆìƒì¹?ëª»í•œ ?¤ë¥˜: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
