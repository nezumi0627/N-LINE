"""LINEプロセス管理モジュール

LINEアプリケーションの起動、終了、パス取得、キャッシュクリアなどの
基本操作を提供するモジュールです。
"""
import os
import shutil
import subprocess
import time
from typing import List, Optional

import psutil


class LineManager:
    """LINEプロセスとインストールパスを管理するクラス

    このクラスは静的メソッドのみを提供し、LINEアプリケーションの
    基本的な操作（起動、終了、パス取得など）を実行します。
    """

    PROCESS_NAME = "LINE.exe"
    """LINEプロセスの実行ファイル名"""

    @staticmethod
    def get_line_processes() -> List[psutil.Process]:
        """実行中のLINEプロセスのリストを取得

        Returns:
            LINEプロセスのリスト。見つからない場合は空リスト
        """
        line_processes = []
        for proc in psutil.process_iter(["pid", "name", "exe"]):
            try:
                if proc.info["name"] == LineManager.PROCESS_NAME:
                    line_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return line_processes

    @staticmethod
    def is_line_running() -> bool:
        """LINEが実行中かどうかを確認

        Returns:
            LINEが実行中の場合はTrue、そうでなければFalse
        """
        return len(LineManager.get_line_processes()) > 0

    @staticmethod
    def kill_line() -> bool:
        """すべてのLINEプロセスを終了

        Returns:
            プロセスが見つかり終了処理を試みた場合はTrue、
            プロセスが見つからなかった場合はFalse
        """
        procs = LineManager.get_line_processes()
        if not procs:
            return False

        for proc in procs:
            try:
                proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return True

    @staticmethod
    def get_install_path() -> Optional[str]:
        """LINEのインストールパスを取得

        実行中のプロセスから取得を試み、失敗した場合は
        一般的なパスを確認します。

        Returns:
            インストールパス。見つからない場合はNone
        """
        procs = LineManager.get_line_processes()
        if procs:
            try:
                exe_path = procs[0].info["exe"]
                if exe_path:
                    return os.path.dirname(exe_path)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # フォールバック: 一般的なパスを確認
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            common_path = os.path.join(
                user_profile, "AppData", "Local", "LINE", "bin"
            )
            if os.path.exists(common_path):
                return common_path

        return None

    @staticmethod
    def clear_cache() -> str:
        """LINEのキャッシュディレクトリをクリア

        Returns:
            処理結果を示すメッセージ
        """
        user_profile = os.environ.get("USERPROFILE")
        if not user_profile:
            return "Error: Could not determine user profile."

        # キャッシュパス: %LOCALAPPDATA%\LINE\Cache
        cache_path = os.path.join(user_profile, "AppData", "Local", "LINE", "Cache")

        if not os.path.exists(cache_path):
            return f"Cache directory not found at: {cache_path}"

        try:
            # フォルダ自体は削除せず、内容のみを削除（安全のため）
            count = 0
            for filename in os.listdir(cache_path):
                file_path = os.path.join(cache_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        count += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        count += 1
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            return f"Successfully cleared {count} items from cache."
        except Exception as e:
            return f"Error clearing cache: {str(e)}"

    @staticmethod
    def launch_line() -> str:
        """LINEを起動

        Returns:
            処理結果を示すメッセージ
        """
        if LineManager.is_line_running():
            return "LINE is already running."

        install_path = LineManager.get_install_path()
        if not install_path:
            return "Error: Could not find LINE installation path."

        # 実行ファイルの候補（優先順位順）
        candidates = [
            os.path.join(install_path, "LineLauncher.exe"),
            os.path.join(install_path, "current", "LINE.exe"),
            os.path.join(install_path, "LINE.exe"),
        ]

        exe_to_run = None
        for candidate in candidates:
            if os.path.exists(candidate):
                exe_to_run = candidate
                break

        if not exe_to_run:
            return f"Error: No valid LINE executable found in {install_path}"

        try:
            os.startfile(exe_to_run)
            return "Success: LINE launching..."
        except Exception as e:
            return f"Error launching LINE: {str(e)}"

    @staticmethod
    def relaunch_with_params(args: List[str]) -> str:
        """LINEを終了し、指定された引数で再起動

        Args:
            args: 起動時に渡すコマンドライン引数のリスト

        Returns:
            処理結果を示すメッセージ
        """
        LineManager.kill_line()
        # クリーンアップのため少し待機
        time.sleep(1)

        install_path = LineManager.get_install_path()
        if not install_path:
            return "Error: Could not find LINE installation path."

        # 実行ファイルを探す
        exe_path = os.path.join(install_path, "LineLauncher.exe")
        if not os.path.exists(exe_path):
            exe_path = os.path.join(install_path, "LINE.exe")

        if not os.path.exists(exe_path):
            return "Error: LINE executable not found."

        try:
            cmd = [exe_path] + args
            subprocess.Popen(cmd, cwd=install_path, shell=False)
            return f"Restarted LINE with: {' '.join(args)}"
        except Exception as e:
            return f"Error launching LINE: {e}"
