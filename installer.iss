; Inno Setup スクリプト
; N-LINE インストーラー

#define AppName "N-LINE"
#define AppVersion "0.2.0"
#define AppPublisher "N-LINE Project"
#define AppURL "https://github.com/nezumi0627/n-line"
#define AppExeName "N-LINE.exe"
#define BuildDir "dist"
; フォルダモードの場合、実行ファイルは dist\N-LINE\N-LINE.exe にある
#define ExePath "dist\N-LINE\N-LINE.exe"
#define OutputDir "installer"
#define AppIdGuid "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"

[Setup]
; 基本情報
AppId={#AppIdGuid}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir={#OutputDir}
OutputBaseFilename=N-LINE-Setup-{#AppVersion}
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; フォルダモードの場合、N-LINEフォルダ全体を含める
Source: "{#BuildDir}\N-LINE\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
; 追加ファイルがある場合はここに追加
; Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  UninstallKey: String;
begin
  Result := True;
  // 既存のインストールをチェック
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#AppIdGuid}_is1';
  if RegKeyExists(HKEY_LOCAL_MACHINE, UninstallKey) or RegKeyExists(HKEY_CURRENT_USER, UninstallKey) then
  begin
    if MsgBox('既にN-LINEがインストールされています。' + #13#10 + '上書きインストールしますか？', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

