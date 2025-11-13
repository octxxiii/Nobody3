; Inno Setup script for Nobody 3 v2.0
; Builds a Windows installer that includes the PyInstaller output in dist\Nobody 3

[Setup]
AppName=Nobody 3
AppVersion=2.0
AppId=Nobody 3
AppPublisher=nobody
DefaultDirName={autopf}\Nobody 3
DefaultGroupName=Nobody 3
OutputDir=dist
OutputBaseFilename=Nobody 3-Setup-v2.0
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
Source: "dist\\Nobody 3.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Nobody 3"; Filename: "{app}\\Nobody 3.exe"
Name: "{commondesktop}\\Nobody 3"; Filename: "{app}\\Nobody 3.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\Nobody 3.exe"; Description: "Run Nobody 3"; Flags: nowait postinstall skipifsilent
