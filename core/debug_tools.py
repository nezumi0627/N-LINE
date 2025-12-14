import psutil
import os
import sys
from typing import Dict, Any, List
from .line_manager import LineManager


class DebugTools:
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        info = {
            "OS": os.name,
            "Platform": sys.platform,
            "Python Version": sys.version.split()[0],
            "User Profile": os.environ.get("USERPROFILE", "Unknown"),
        }
        return info

    @staticmethod
    def get_line_process_details() -> List[Dict[str, Any]]:
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
        """
        Scans interesting directories for files.
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
