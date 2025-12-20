"""Automationタブモジュール

UI Automationを使用したLINEアプリケーションの自動操作を行うタブを
提供するモジュールです。
"""
import customtkinter

from n_line.core.automation_manager import AutomationManager


class AutomationTab(customtkinter.CTkFrame):
    """Automationタブクラス

    実験的な自動化機能を提供するタブです。
    """

    def __init__(self, master, **kwargs) -> None:
        """タブを初期化"""
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.auto_label = customtkinter.CTkLabel(
            self,
            text="Experimental Automation",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.auto_label.grid(row=0, column=0, pady=10)

        self.auto_status_label = customtkinter.CTkLabel(
            self, text="Ready", text_color="gray"
        )
        self.auto_status_label.grid(row=1, column=0, pady=5)

        # Message Injection
        self.auto_entry = customtkinter.CTkEntry(
            self, placeholder_text="Message to type..."
        )
        self.auto_entry.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.send_text_btn = customtkinter.CTkButton(
            self,
            text="Type Text (AutoSuggestTextArea)",
            command=self.send_automation_text,
        )
        self.send_text_btn.grid(row=3, column=0, padx=20, pady=5)

        self.send_key_btn = customtkinter.CTkButton(
            self,
            text="Send 'Enter' Key",
            command=self.send_enter_key,
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.send_key_btn.grid(row=4, column=0, padx=20, pady=20)

    def send_automation_text(self) -> None:
        """チャット入力欄にテキストを送信"""
        text = self.auto_entry.get()
        if not text:
            self.auto_status_label.configure(
                text="Please enter text.", text_color="yellow"
            )
            return

        result = AutomationManager.type_in_chat(text)
        color = "green" if "Success" in result else "red"
        self.auto_status_label.configure(text=result, text_color=color)

    def send_enter_key(self) -> None:
        """Enterキーを送信してメッセージを送信"""
        result = AutomationManager.press_send()
        color = "green" if "Success" in result else "red"
        self.auto_status_label.configure(text=result, text_color=color)
