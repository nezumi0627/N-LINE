# N-LINE 利用ガイド

## インストールとセットアップ

### 前提条件
- Windows 10 または 11
- Python 3.11 以上
- LINE デスクトップ版アプリがインストールされていること

### クイックスタート
1. `run.bat` をダブルクリックして起動します。
   - 初回起動時に自動的に仮想環境 (`venv`) が構築され、必要なライブラリ (`uiautomation`, `customtkinter` 等) がインストールされます。

---

## 🚀 高度な使用方法 (Advanced Usage)

### 1. UI Inspector Mode (Spy Mode) の使い方
LINEの内部構造（ボタンのIDや構造）を調査するための機能です。

1. **Debug Tools** を開き、**"UI Inspector"** タブを選択します。
2. **"Inspector Mode (Ctrl+Shift to Spy)"** スイッチを **ON** にします。
3. LINEのウィンドウ上にマウスカーソルを持っていきます。
4. キーボードの **`Ctrl`** と **`Shift`** を同時に押します。
5. ポイントしている要素が**赤い枠**で一瞬ハイライトされ、Debugウィンドウに詳細情報が表示されます。

### 2. Arg Injection による UI カスタマイズ (Revolution)
LINEの見た目をCSS (Qt Stylesheet / .qss) で強制的に変更する機能です。

#### 準備
適用したいデザインを記述した `.qss` ファイルを作成します。
（サンプルとして `test_style.qss` がプロジェクトルートに生成されています）

このファイルを、LINEがアクセス可能な以下のフォルダのいずれかにコピーすることをお勧めします：
- `%USERPROFILE%\AppData\Local\LINE\bin\current\`

#### 実行手順
1. **Debug Tools** を開き、**"Window Mods"** タブを選択します。
2. 一番下の **"Arg Injection (Relaunch)"** 欄を探します。
3. 入力欄に引数を入力します。
   - 例: `-stylesheet test_style.qss`
   - フルパス例: `-stylesheet "C:\Path\To\Your\style.qss"`
4. **"Relaunch with Args"** ボタンをクリックします。
5. LINEが再起動し、指定したスタイルが適用されます。

---

## 基本操作

### メインダッシュボード
- **Kill Process**: LINEを強制終了します。
- **Clear Cache**: キャッシュ（画像や一時ファイル）を削除し、動作を軽くします。
- **Launch LINE**: LINEを起動します。

### Debug & Mods
- **Opacity / Topmost**: ウィンドウの透明化や最前面固定を行います。
- **Automation**: チャット画面が開いている状態で、テキスト送信のテストを行えます。
