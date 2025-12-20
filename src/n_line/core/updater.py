"""アップデーターモジュール

オンラインで最新バージョンを確認し、更新をダウンロード・インストールする
機能を提供するモジュールです。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

import customtkinter


class Updater:
    """アップデータークラス

    バージョン確認、ダウンロード、インストール機能を提供します。
    """

    # バージョン情報のURL（GitHub Releases API）
    VERSION_URL = "https://api.github.com/repos/nezumi0627/n-line/releases/latest"
    # または、カスタムAPIエンドポイント
    # VERSION_URL = "https://your-domain.com/api/version"

    def __init__(self, current_version: str) -> None:
        """アップデーターを初期化

        Args:
            current_version: 現在のバージョン番号
        """
        self.current_version = current_version
        self.latest_version: Optional[str] = None
        self.download_url: Optional[str] = None
        self.release_info: Optional[Dict] = None

    def check_update(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """最新バージョンを確認

        Returns:
            (更新があるか, 最新バージョン, エラーメッセージ)
        """
        try:
            with urllib.request.urlopen(self.VERSION_URL, timeout=10) as response:
                data = json.loads(response.read().decode())
                self.latest_version = data.get("tag_name", "").lstrip("v")
                self.release_info = data

                # ダウンロードURLを取得
                assets = data.get("assets", [])
                if assets:
                    # Windowsインストーラーを探す
                    for asset in assets:
                        if asset.get("name", "").endswith(".exe"):
                            self.download_url = asset.get("browser_download_url")
                            break

                if self.latest_version and self._is_newer_version(
                    self.latest_version, self.current_version
                ):
                    return True, self.latest_version, None
                else:
                    return False, self.latest_version, None

        except urllib.error.URLError as e:
            return False, None, f"ネットワークエラー: {str(e)}"
        except json.JSONDecodeError as e:
            return False, None, f"JSON解析エラー: {str(e)}"
        except Exception as e:
            return False, None, f"エラー: {str(e)}"

    def download_update(self, progress_callback=None) -> Tuple[bool, Optional[str]]:
        """更新をダウンロード

        Args:
            progress_callback: 進捗を報告するコールバック関数 (bytes_downloaded, total_bytes)

        Returns:
            (成功したか, エラーメッセージ)
        """
        if not self.download_url:
            return False, "ダウンロードURLが取得できませんでした"

        try:
            # 一時ディレクトリにダウンロード
            temp_dir = tempfile.gettempdir()
            installer_path = Path(temp_dir) / f"N-LINE-Setup-{self.latest_version}.exe"

            def report_progress(block_num, block_size, total_size):
                if progress_callback and total_size > 0:
                    downloaded = block_num * block_size
                    progress_callback(downloaded, total_size)

            urllib.request.urlretrieve(
                self.download_url, str(installer_path), report_progress
            )

            self.installer_path = installer_path
            return True, None

        except Exception as e:
            return False, f"ダウンロードエラー: {str(e)}"

    def install_update(self) -> Tuple[bool, Optional[str]]:
        """更新をインストール

        Returns:
            (成功したか, エラーメッセージ)
        """
        if not hasattr(self, "installer_path") or not self.installer_path.exists():
            return False, "インストーラーファイルが見つかりません"

        try:
            # インストーラーを実行（管理者権限で）
            subprocess.Popen(
                [str(self.installer_path), "/SILENT", "/FORCECLOSEAPPLICATIONS"],
                shell=True,
            )
            return True, None
        except Exception as e:
            return False, f"インストールエラー: {str(e)}"

    def _is_newer_version(self, version1: str, version2: str) -> bool:
        """バージョン1がバージョン2より新しいかチェック

        Args:
            version1: 比較するバージョン1
            version2: 比較するバージョン2

        Returns:
            version1がversion2より新しい場合True
        """
        try:
            v1_parts = [int(x) for x in version1.split(".")]
            v2_parts = [int(x) for x in version2.split(".")]

            # パディングして同じ長さにする
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))

            return v1_parts > v2_parts
        except ValueError:
            # パースできない場合は文字列比較
            return version1 > version2

    @staticmethod
    def get_current_version() -> str:
        """現在のバージョンを取得

        Returns:
            現在のバージョン番号
        """
        try:
            from n_line import __version__

            return __version__
        except ImportError:
            return "0.0.0"


class UpdateDialog(customtkinter.CTkToplevel):
    """アップデート確認ダイアログ"""

    def __init__(self, parent, updater: Updater) -> None:
        """ダイアログを初期化"""
        super().__init__(parent)
        self.updater = updater
        self.downloaded = False

        self.title("アップデート確認")
        self.geometry("500x400")
        self.resizable(False, False)

        # メインフレーム
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # タイトル
        title_label = customtkinter.CTkLabel(
            main_frame,
            text="アップデート確認",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(pady=(10, 20))

        # 現在のバージョン
        current_label = customtkinter.CTkLabel(
            main_frame, text=f"現在のバージョン: {updater.current_version}"
        )
        current_label.pack(pady=5)

        # ステータス
        self.status_label = customtkinter.CTkLabel(
            main_frame, text="最新バージョンを確認中...", text_color="gray"
        )
        self.status_label.pack(pady=10)

        # 進捗バー
        self.progress_bar = customtkinter.CTkProgressBar(main_frame)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)

        # ボタンフレーム
        button_frame = customtkinter.CTkFrame(main_frame)
        button_frame.pack(pady=20)

        self.check_button = customtkinter.CTkButton(
            button_frame, text="確認", command=self.check_update
        )
        self.check_button.pack(side="left", padx=5)

        self.download_button = customtkinter.CTkButton(
            button_frame,
            text="ダウンロード",
            command=self.download_update,
            state="disabled",
        )
        self.download_button.pack(side="left", padx=5)

        self.install_button = customtkinter.CTkButton(
            button_frame,
            text="インストール",
            command=self.install_update,
            state="disabled",
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.install_button.pack(side="left", padx=5)

        self.close_button = customtkinter.CTkButton(
            button_frame, text="閉じる", command=self.destroy
        )
        self.close_button.pack(side="left", padx=5)

        # 自動的にチェック
        self.after(100, self.check_update)

    def check_update(self) -> None:
        """アップデートをチェック"""
        self.status_label.configure(text="最新バージョンを確認中...", text_color="gray")
        self.check_button.configure(state="disabled")

        has_update, latest_version, error = self.updater.check_update()

        if error:
            self.status_label.configure(text=f"エラー: {error}", text_color="red")
            self.check_button.configure(state="normal")
        elif has_update and latest_version:
            self.status_label.configure(
                text=f"新しいバージョン {latest_version} が利用可能です！",
                text_color="green",
            )
            self.download_button.configure(state="normal")
        else:
            self.status_label.configure(
                text="最新バージョンです", text_color="gray"
            )
            self.check_button.configure(state="normal")

    def download_update(self) -> None:
        """アップデートをダウンロード"""
        self.status_label.configure(text="ダウンロード中...", text_color="blue")
        self.download_button.configure(state="disabled")

        def progress_callback(downloaded: int, total: int) -> None:
            progress = downloaded / total if total > 0 else 0
            self.progress_bar.set(progress)
            self.status_label.configure(
                text=f"ダウンロード中... {downloaded // 1024 // 1024}MB / {total // 1024 // 1024}MB"
            )

        success, error = self.updater.download_update(progress_callback)

        if success:
            self.status_label.configure(
                text="ダウンロード完了！", text_color="green"
            )
            self.progress_bar.set(1.0)
            self.downloaded = True
            self.install_button.configure(state="normal")
        else:
            self.status_label.configure(text=f"エラー: {error}", text_color="red")
            self.download_button.configure(state="normal")

    def install_update(self) -> None:
        """アップデートをインストール"""
        self.status_label.configure(
            text="インストーラーを起動しています...", text_color="blue"
        )
        self.install_button.configure(state="disabled")

        success, error = self.updater.install_update()

        if success:
            self.status_label.configure(
                text="インストーラーを起動しました。アプリケーションを終了します...",
                text_color="green",
            )
            self.after(2000, sys.exit)
        else:
            self.status_label.configure(text=f"エラー: {error}", text_color="red")
            self.install_button.configure(state="normal")

