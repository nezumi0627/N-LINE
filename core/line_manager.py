import psutil
import os
import shutil
from typing import List, Dict, Optional


class LineManager:
    PROCESS_NAME = "LINE.exe"

    @staticmethod
    def get_line_processes() -> List[psutil.Process]:
        """Returns a list of running LINE processes."""
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
        """Checks if LINE is currently running."""
        return len(LineManager.get_line_processes()) > 0

    @staticmethod
    def kill_line() -> bool:
        """Terminates all LINE processes."""
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
        """Attempts to find the LINE installation path from a running process."""
        procs = LineManager.get_line_processes()
        if procs:
            try:
                exe_path = procs[0].info["exe"]
                if exe_path:
                    return os.path.dirname(exe_path)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Fallback check common paths
        user_profile = os.environ.get("USERPROFILE")
        common_path = os.path.join(user_profile, "AppData", "Local", "LINE", "bin")
        if os.path.exists(common_path):
            return common_path

        return None

    @staticmethod
    def clear_cache() -> str:
        """
        Clears the LINE cache directory.
        Returns a status message.
        """
        user_profile = os.environ.get("USERPROFILE")
        if not user_profile:
            return "Error: Could not determine user profile."

        # Typical Cache Path: %LOCALAPPDATA%\LINE\Cache
        # Note: This path might vary by version, using a safe guess
        cache_path = os.path.join(user_profile, "AppData", "Local", "LINE", "Cache")

        if not os.path.exists(cache_path):
            return f"Cache directory not found at: {cache_path}"

        try:
            # We don't delete the folder itself, just contents, to be safe
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
        """
        Attempts to launch LINE.
        Returns a status message.
        """
        if LineManager.is_line_running():
            return "LINE is already running."

        install_path = LineManager.get_install_path()
        if not install_path:
            return "Error: Could not find LINE installation path."

        # Try common executables in order of preference
        # 1. LineLauncher.exe (Standard launcher in bin)
        # 2. current/LINE.exe (Actual executable through 'current' link)
        # 3. LINE.exe (Direct executable)
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
