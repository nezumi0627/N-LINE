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

    @staticmethod
    def scan_for_resources() -> Dict[str, List[str]]:
        """
        Recursively scans LINE directories for potentially moddable resources.
        Looking for: .qss (Qt Stylesheets), .css, .json (configs), .png (assets), .theme
        """
        targets = [".qss", ".css", ".json", ".theme", ".style"]
        found_resources = {}

        search_paths = []

        # 1. Install Path
        install_path = LineManager.get_install_path()
        if install_path:
            search_paths.append(("Install Dir", install_path))

        # 2. Data Path
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            data_path = os.path.join(user_profile, "AppData", "Local", "LINE")
            search_paths.append(("Data Dir", data_path))

        for label, root_path in search_paths:
            if not os.path.exists(root_path):
                continue

            found_resources[label] = []
            try:
                # Walk with limit to avoid scanning deep caches too much
                for root, dirs, files in os.walk(root_path):
                    # Skip heavy cache folders
                    if "Cache" in root or "logs" in root.lower():
                        continue

                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        if ext in targets:
                            # Verify if it looks interesting (skip minified huge jsons maybe? keep for now)
                            full_path = os.path.join(root, file)
                            # Store relative path for readability
                            rel_path = os.path.relpath(full_path, root_path)
                            found_resources[label].append(rel_path)
            except Exception as e:
                found_resources[label].append(f"Error scanning: {e}")

        return found_resources
