"""デバッグツールモジュール

システム情報の取得、プロセス詳細の取得、ディレクトリスキャンなどの
デバッグ用機能を提供するモジュールです。
"""
import os
import sys
from typing import Any, Dict, List

import psutil

from .line_manager import LineManager


class DebugTools:
    """デバッグ用のユーティリティクラス

    このクラスは静的メソッドのみを提供し、システム情報やプロセス情報の
    取得、ディレクトリスキャンなどのデバッグ機能を提供します。
    """

    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """システム情報を取得

        Returns:
            システム情報を含む辞書
        """
        info = {
            "OS": os.name,
            "Platform": sys.platform,
            "Python Version": sys.version.split()[0],
            "User Profile": os.environ.get("USERPROFILE", "Unknown"),
        }
        return info

    @staticmethod
    def get_line_process_details() -> List[Dict[str, Any]]:
        """LINEプロセスの詳細情報を取得

        Returns:
            プロセス詳細情報のリスト
        """
        details = []
        procs = LineManager.get_line_processes()
        for proc in procs:
            try:
                p_info = proc.as_dict(
                    attrs=[
                        "pid",
                        "name",
                        "cpu_percent",
                        "memory_info",
                        "cmdline",
                        "create_time",
                    ]
                )
                details.append(p_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return details

    @staticmethod
    def scan_line_directories() -> Dict[str, List[str]]:
        """LINE関連のディレクトリをスキャンしてファイル一覧を取得

        Returns:
            ディレクトリ名をキー、ファイル名のリストを値とする辞書
        """
        paths = {}

        # Install Path
        install_path = LineManager.get_install_path()
        if install_path and os.path.exists(install_path):
            try:
                files = os.listdir(install_path)
                paths["Install Dir"] = files[:20]  # Limit to 20 for preview
                if len(files) > 20:
                    paths["Install Dir"].append(f"... and {len(files) - 20} more files")
            except Exception as e:
                paths["Install Dir"] = [f"Error scanning: {str(e)}"]

        # Data Path (Local AppData)
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            data_path = os.path.join(user_profile, "AppData", "Local", "LINE")
            if os.path.exists(data_path):
                try:
                    files = os.listdir(data_path)
                    paths["Data Dir"] = files
                except Exception:
                    pass

        return paths
