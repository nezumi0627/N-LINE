"""デバッグウィンドウモジュール

各種デバッグツールをタブ形式で提供するウィンドウを提供するモジュールです。
"""
import customtkinter

from n_line.gui.tabs.automation_tab import AutomationTab
from n_line.gui.tabs.files_tab import FilesTab
from n_line.gui.tabs.inspector_tab import InspectorTab
from n_line.gui.tabs.mods_tab import ModsTab
from n_line.gui.tabs.process_tab import ProcessTab
from n_line.gui.tabs.qss_tab import QSSTab


class DebugWindow(customtkinter.CTkToplevel):
    """デバッグウィンドウクラス

    プロセス情報、ファイル構造、UI Inspector、ウィンドウ操作、
    QSS編集、自動化などのデバッグツールをタブ形式で提供します。
    """

    def __init__(self, *args, **kwargs) -> None:
        """デバッグウィンドウを初期化"""
        super().__init__(*args, **kwargs)
        self.geometry("800x700")
        self.title("N-LINE Debug Tools")
        self.resizable(True, True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tab View for Debug Categories
        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create Tabs
        self.tab_view.add("Process Info")
        self.tab_view.add("File Structure")
        self.tab_view.add("UI Inspector")
        self.tab_view.add("Window Mods")
        self.tab_view.add("Styles (QSS)")
        self.tab_view.add("Automation")

        # Initialize Tab Content classes
        # Process Tab
        self.process_content = ProcessTab(self.tab_view.tab("Process Info"))
        self.process_content.pack(fill="both", expand=True)

        # Files Tab
        self.files_content = FilesTab(self.tab_view.tab("File Structure"))
        self.files_content.pack(fill="both", expand=True)

        # UI Inspector Tab
        self.inspector_content = InspectorTab(self.tab_view.tab("UI Inspector"))
        self.inspector_content.pack(fill="both", expand=True)

        # Mods Tab
        self.mods_content = ModsTab(self.tab_view.tab("Window Mods"))
        self.mods_content.pack(fill="both", expand=True)

        # QSS Tab
        self.qss_content = QSSTab(self.tab_view.tab("Styles (QSS)"))
        self.qss_content.pack(fill="both", expand=True)

        # Automation Tab
        self.automation_content = AutomationTab(self.tab_view.tab("Automation"))
        self.automation_content.pack(fill="both", expand=True)

        # Bind close event to cleanup resources (like hotkeys)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self) -> None:
        """ウィンドウクローズ時の処理

        タブのリソースをクリーンアップしてからウィンドウを破棄します。
        """
        if hasattr(self.inspector_content, "cleanup"):
            self.inspector_content.cleanup()
        self.destroy()
