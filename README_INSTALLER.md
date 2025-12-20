# インストーラー作成のクイックガイド

## 実行ファイルの作成（Inno Setup不要）

Inno Setupがインストールされていない場合でも、実行ファイルを作成できます：

```bash
# 実行ファイルのみ作成
python scripts/build_installer.py --exe-only

# または make.bat を使用
.\make.bat build-installer
```

実行ファイルは `dist/N-LINE.exe` に作成されます。このファイルを直接配布できます。

## インストーラーの作成（Inno Setup必要）

完全なインストーラーを作成するには、Inno Setupが必要です：

1. **Inno Setupをインストール**
   - ダウンロード: https://jrsoftware.org/isdl.php
   - 推奨バージョン: Inno Setup 6

2. **インストーラーを作成**
   ```bash
   python scripts/build_installer.py
   ```

インストーラーは `installer/N-LINE-Setup-0.2.0.exe` に作成されます。

## トラブルシューティング

### Inno Setupが見つからない

実行ファイルのみを作成する場合は、`--exe-only` オプションを使用してください。

### 実行ファイルが大きい

実行ファイルのサイズは約50-100MBになります。これは正常です（Pythonランタイムとすべての依存関係が含まれています）。

### 実行ファイルが起動しない

1. ウイルス対策ソフトがブロックしていないか確認
2. コマンドプロンプトから実行してエラーメッセージを確認
3. 必要なDLLが含まれているか確認

詳細は [docs/INSTALLER.md](docs/INSTALLER.md) を参照してください。

