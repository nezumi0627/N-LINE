# ビルドガイド

N-LINEの実行ファイルとインストーラーを作成する手順です。

## 前提条件

1. **Python 3.8以上**がインストールされていること
2. **すべての依存関係**がインストールされていること
3. **PyInstaller**がインストールされていること

## ビルド前の確認

### 1. 依存関係のインストール

```bash
# 仮想環境を作成（推奨）
python -m venv venv
venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt
pip install pyinstaller
```

### 2. ビルド前テスト

```bash
# 必要なモジュールがインポートできるかテスト
python scripts/test_build.py
```

すべてのモジュールが正常にインポートできることを確認してください。

## 実行ファイルの作成

### 方法1: 自動スクリプトを使用（推奨）

```bash
# 実行ファイルとインストーラーの両方を作成
python scripts/build_installer.py

# 実行ファイルのみ作成
python scripts/build_installer.py --exe-only
```

### 方法2: 手動で作成

```bash
# PyInstallerで実行ファイルを作成
pyinstaller --clean n-line.spec
```

実行ファイルは `dist/N-LINE.exe` に作成されます。

## トラブルシューティング

### customtkinterが見つからない

**問題:** `ModuleNotFoundError: No module named 'customtkinter'`

**解決方法:**

1. **仮想環境を使用しているか確認**
   ```bash
   # 仮想環境をアクティベート
   venv\Scripts\activate
   
   # customtkinterがインストールされているか確認
   python -c "import customtkinter; print(customtkinter.__file__)"
   ```

2. **依存関係を再インストール**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **PyInstallerを最新版に更新**
   ```bash
   pip install --upgrade pyinstaller
   ```

4. **ビルド前テストを実行**
   ```bash
   python scripts/test_build.py
   ```

### アセットファイルが見つからない

customtkinterのアセットファイルが含まれていない場合：

1. `n-line.spec`の`datas`セクションを確認
2. customtkinterのパスが正しいか確認：
   ```bash
   python -c "import customtkinter; from pathlib import Path; print(Path(customtkinter.__file__).parent / 'assets')"
   ```

### 実行ファイルが起動しない

1. **コンソールモードでテスト**
   `n-line.spec`で`console=True`に変更してビルドし、エラーメッセージを確認

2. **デバッグモードでビルド**
   ```bash
   pyinstaller --clean --debug=all n-line.spec
   ```

3. **フォルダモードで試す**
   `n-line.spec`を一時的にフォルダモードに変更（`exclude_binaries=True`）

詳細は [docs/TROUBLESHOOTING_INSTALLER.md](docs/TROUBLESHOOTING_INSTALLER.md) を参照してください。

## インストーラーの作成

実行ファイルが正常に作成されたら、インストーラーを作成できます：

```bash
# インストーラーを作成
python scripts/build_installer.py --installer-only
```

インストーラーは `installer/N-LINE-Setup-0.2.0.exe` に作成されます。

