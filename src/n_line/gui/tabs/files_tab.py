"""Filesタブモジュール

LINE関連のディレクトリとファイル構造を表示するタブを提供するモジュールです。
"""
import customtkinter

from n_line.core.debug_tools import DebugTools


class FilesTab(customtkinter.CTkFrame):
    """Filesタブクラス

    LINE関連のディレクトリとファイルをスキャンして表示します。
    """

    def __init__(self, master, **kwargs) -> None:
        """タブを初期化"""
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.files_textbox = customtkinter.CTkTextbox(self, font=("Consolas", 12))
        self.files_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.scan_btn = customtkinter.CTkButton(
            self, text="Scan Directories", command=self.scan_files
        )
        self.scan_btn.grid(row=1, column=0, pady=(10, 5), padx=5, sticky="ew")

        # Initial Load
        self.scan_files()

    def scan_files(self) -> None:
        """ディレクトリをスキャンしてファイル一覧を表示"""
        self.files_textbox.configure(state="normal")
        self.files_textbox.delete("0.0", "end")

        paths = DebugTools.scan_line_directories()
        report = "--- Directory Scan ---\n\n"

        for name, files in paths.items():
            report += f"[{name}]\n"
            for f in files:
                report += f"  - {f}\n"
            report += "\n"

        self.files_textbox.insert("0.0", report)
        self.files_textbox.configure(state="disabled")
