; Inno Setup script for OctXXIII v2.0
; Builds a Windows installer that includes the PyInstaller output in dist\OctXXIII

[Setup]
AppName=OctXXIII
AppVersion=2.0
AppId=OctXXIII
AppPublisher=nobody
DefaultDirName={autopf}\OctXXIII
DefaultGroupName=OctXXIII
OutputDir=dist
OutputBaseFilename=OctXXIII-Setup-v2.0
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
; SetupIconFile can be set to an .ico if available (e.g., app.ico)
; SetupIconFile=app.ico

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create &Desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\\OctXXIII\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\OctXXIII"; Filename: "{app}\\OctXXIII.exe"
Name: "{commondesktop}\\OctXXIII"; Filename: "{app}\\OctXXIII.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\OctXXIII.exe"; Description: "Run OctXXIII"; Flags: nowait postinstall skipifsilent