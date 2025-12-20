# インストーラー作成のトラブルシューティング

## customtkinterが見つからないエラー

### 問題

実行ファイルを実行すると以下のエラーが発生する：

```
ModuleNotFoundError: No module named 'customtkinter'
```

### 解決方法

#### 1. 仮想環境でビルドする

```bash
# 仮想環境を作成
python -m venv venv
venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 実行ファイルを作成
pyinstaller --clean n-line.spec
```

#### 2. customtkinterが正しくインストールされているか確認

```bash
python -c "import customtkinter; print(customtkinter.__file__)"
```

#### 3. PyInstallerのバージョンを確認

```bash
pip install --upgrade pyinstaller
```

#### 4. ワンファイルモードではなく、フォルダモードで試す

`n-line.spec`の`exe`セクションを一時的に変更：

```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # 空のリスト
    exclude_binaries=True,  # バイナリを除外
    name='N-LINE',
    # ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='N-LINE',
)
```

これで`dist/N-LINE/`フォルダにすべてのファイルが作成されます。

#### 5. デバッグモードでビルド

```python
# n-line.specで
console=True,  # コンソールを表示
debug=True,   # デバッグ情報を出力
```

これでエラーメッセージが詳細に表示されます。

## その他の問題

### アセットファイルが見つからない

customtkinterのアセットファイルが含まれていない場合：

1. `n-line.spec`の`datas`セクションを確認
2. customtkinterのパスが正しいか確認
3. 手動でアセットファイルを追加

### 実行ファイルが大きすぎる

- `upx=True`を`upx=False`に変更
- 不要なモジュールを`excludes`に追加

### 起動が遅い

- ワンファイルモードは起動が遅い
- フォルダモードを使用することを検討

