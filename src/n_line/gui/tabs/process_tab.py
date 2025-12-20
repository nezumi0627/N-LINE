"""Processタブモジュール

LINEプロセスの詳細情報とシステム情報を表示するタブを提供するモジュールです。
"""
import datetime

import customtkinter

from n_line.core.debug_tools import DebugTools


class ProcessTab(customtkinter.CTkFrame):
    """Processタブクラス

    LINEプロセスの詳細情報とシステム情報を表示します。
    """

    def __init__(self, master, **kwargs) -> None:
        """タブを初期化"""
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.process_textbox = customtkinter.CTkTextbox(self, font=("Consolas", 12))
        self.process_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.refresh_btn = customtkinter.CTkButton(
            self,
            text="Refresh Process Info",
            command=self.refresh_process_info,
        )
        self.refresh_btn.grid(row=1, column=0, pady=10)

        # Initial Load
        self.refresh_process_info()

    def refresh_process_info(self) -> None:
        """プロセス情報を更新して表示"""
        self.process_textbox.configure(state="normal")
        self.process_textbox.delete("0.0", "end")

        details = DebugTools.get_line_process_details()
        system_info = DebugTools.get_system_info()

        report = "--- System Info ---\n"
        for k, v in system_info.items():
            report += f"{k}: {v}\n"

        report += f"\n--- LINE Process Details ({datetime.datetime.now().strftime('%H:%M:%S')}) ---\n"
        if not details:
            report += "No LINE process found.\n"
        else:
            for i, proc in enumerate(details):
                report += f"\nProcess #{i + 1} (PID: {proc.get('pid')})\n"
                report += f"  Name: {proc.get('name')}\n"
                report += (
                    f"  Memory: {proc.get('memory_info').rss / 1024 / 1024:.2f} MB\n"
                )
                report += f"  CPU: {proc.get('cpu_percent')}%\n"
                report += f"  Cmdline: {proc.get('cmdline')}\n"

        self.process_textbox.insert("0.0", report)
        self.process_textbox.configure(state="disabled")
