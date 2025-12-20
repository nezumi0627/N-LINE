# インストーラー作成ガイド

N-LINEのWindowsインストーラーを作成する方法を説明します。

## 📋 目次

- [前提条件](#前提条件)
- [インストール方法](#インストール方法)
- [インストーラーの作成](#インストーラーの作成)
- [トラブルシューティング](#トラブルシューティング)

## 前提条件

### 必要なソフトウェア

1. **Python 3.8以上**
   - プロジェクトの実行に必要

2. **PyInstaller**
   - Pythonアプリケーションを実行ファイルにパッケージ化
   - インストール: `pip install pyinstaller`

3. **Inno Setup**
   - Windowsインストーラー作成ツール
   - ダウンロード: https://jrsoftware.org/isdl.php
   - 推奨バージョン: Inno Setup 6

### 依存関係のインストール

```bash
# プロジェクトの依存関係をインストール
pip install -r requirements.txt

# PyInstallerをインストール
pip install pyinstaller
```

## インストール方法

### 方法1: 自動スクリプトを使用（推奨）

```bash
# 実行ファイルとインストーラーの両方を作成
python scripts/build_installer.py

# 実行ファイルのみ作成
python scripts/build_installer.py --exe-only

# インストーラーのみ作成（実行ファイルが既にある場合）
python scripts/build_installer.py --installer-only

# ビルドファイルをクリーンアップ
python scripts/build_installer.py --clean
```

### 方法2: 手動で作成

#### ステップ1: 実行ファイルの作成

```bash
# PyInstallerで実行ファイルを作成
pyinstaller --clean n-line.spec
```

実行ファイルは `dist/N-LINE.exe` に作成されます。

#### ステップ2: インストーラーの作成

1. Inno Setup Compilerを起動
2. `installer.iss` を開く
3. 「ビルド」→「コンパイル」を実行

または、コマンドラインから：

```bash
# Inno Setupのパスを指定
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

インストーラーは `installer/N-LINE-Setup-0.2.0.exe` に作成されます。

## インストーラーの作成

### 設定ファイル

#### `n-line.spec` (PyInstaller設定)

実行ファイルのパッケージ化設定を定義します。

主な設定項目：
- `hiddenimports`: PyInstallerが検出できないモジュール
- `datas`: データファイル
- `console`: GUIアプリケーションなので `False`

#### `installer.iss` (Inno Setup設定)

インストーラーの設定を定義します。

主な設定項目：
- `AppName`: アプリケーション名
- `AppVersion`: バージョン番号
- `DefaultDirName`: デフォルトインストール先
- `OutputBaseFilename`: インストーラーファイル名

### カスタマイズ

#### アイコンの追加

1. アイコンファイル（`.ico`）を準備
2. `n-line.spec` の `icon` パラメータを更新:
   ```python
   icon='path/to/icon.ico',
   ```
3. `installer.iss` の `SetupIconFile` を更新:
   ```iss
   SetupIconFile=path/to/icon.ico
   ```

#### ライセンスファイルの追加

1. ライセンスファイル（`.txt`）を準備
2. `installer.iss` の `LicenseFile` を更新:
   ```iss
   LicenseFile=LICENSE.txt
   ```

#### 追加ファイルのインストール

`installer.iss` の `[Files]` セクションに追加:

```iss
[Files]
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs
```

## トラブルシューティング

### PyInstaller関連

#### モジュールが見つからない

**問題:** `ModuleNotFoundError` が発生する

**解決方法:**
1. `n-line.spec` の `hiddenimports` にモジュールを追加
2. 再ビルド: `pyinstaller --clean n-line.spec`

#### 実行ファイルが大きすぎる

**問題:** 実行ファイルのサイズが大きい

**解決方法:**
1. `n-line.spec` の `excludes` に不要なモジュールを追加
2. UPX圧縮を使用（`upx=True`）

#### アンチウイルスソフトに検出される

**問題:** 実行ファイルがウイルスとして検出される

**解決方法:**
1. コード署名証明書を使用
2. アンチウイルスソフトに例外を追加
3. PyInstallerの最新版を使用

### Inno Setup関連

#### Inno Setupが見つからない

**問題:** `iscc` コマンドが見つからない

**解決方法:**
1. Inno Setupがインストールされているか確認
2. パスを環境変数に追加
3. `scripts/build_installer.py` のパスを確認

#### インストーラーが作成されない

**問題:** コンパイルエラーが発生する

**解決方法:**
1. `installer.iss` の構文を確認
2. Inno Setup Compilerで直接開いてエラーを確認
3. ログファイルを確認

### その他

#### 実行ファイルが起動しない

**問題:** 実行ファイルをダブルクリックしても起動しない

**解決方法:**
1. コマンドプロンプトから実行してエラーメッセージを確認
2. 依存関係が正しく含まれているか確認
3. ウイルス対策ソフトがブロックしていないか確認

#### パフォーマンスが悪い

**問題:** 実行ファイルの起動が遅い

**解決方法:**
1. ワンファイルモードではなく、フォルダモードを使用
2. 不要なモジュールを除外
3. 起動時のインポートを最適化

## 配布

### インストーラーの配布

作成されたインストーラー（`installer/N-LINE-Setup-0.2.0.exe`）を配布できます。

### 署名（オプション）

コード署名証明書を使用してインストーラーに署名すると、セキュリティ警告を回避できます。

```bash
# 署名の例（実際の証明書パスに置き換え）
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com installer/N-LINE-Setup-0.2.0.exe
```

## 参考資料

- [PyInstaller公式ドキュメント](https://pyinstaller.org/)
- [Inno Setup公式ドキュメント](https://jrsoftware.org/ishelp/)
- [Pythonアプリケーションの配布](https://docs.python.org/ja/3/distributing/index.html)

