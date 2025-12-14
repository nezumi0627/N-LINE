import customtkinter
from core.debug_tools import DebugTools
from core.ui_inspector import UIInspector
from core.line_manager import LineManager
from core.window_manipulator import WindowManipulator
from core.automation_manager import AutomationManager
import json
import datetime


class DebugWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x700")
        self.title("N-LINE Debug Tools")
        self.resizable(True, True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tab View for Debug Categories
        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tab_process = self.tab_view.add("Process Info")
        self.tab_files = self.tab_view.add("File Structure")
        self.tab_ui = self.tab_view.add("UI Inspector")
        self.tab_mods = self.tab_view.add("Window Mods")
        self.tab_auto = self.tab_view.add("Automation")

        # --- Process Info Tab ---
        self.tab_process.grid_columnconfigure(0, weight=1)
        self.tab_process.grid_rowconfigure(0, weight=1)

        self.process_textbox = customtkinter.CTkTextbox(
            self.tab_process, font=("Consolas", 12)
        )
        self.process_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.refresh_btn = customtkinter.CTkButton(
            self.tab_process,
            text="Refresh Process Info",
            command=self.refresh_process_info,
        )
        self.refresh_btn.grid(row=1, column=0, pady=10)

        # --- File Structure Tab ---
        self.tab_files.grid_columnconfigure(0, weight=1)
        self.tab_files.grid_rowconfigure(0, weight=1)

        self.files_textbox = customtkinter.CTkTextbox(
            self.tab_files, font=("Consolas", 12)
        )
        self.files_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.scan_btn = customtkinter.CTkButton(
            self.tab_files, text="Scan Directories", command=self.scan_files
        )
        self.scan_btn.grid(row=1, column=0, pady=10)

        # --- UI Inspector Tab ---
        self.tab_ui.grid_columnconfigure(0, weight=1)
        self.tab_ui.grid_rowconfigure(0, weight=1)

        self.ui_textbox = customtkinter.CTkTextbox(
            self.tab_ui, font=("Consolas", 12), wrap="none"
        )
        self.ui_textbox.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )

        self.inspect_btn = customtkinter.CTkButton(
            self.tab_ui, text="Scan Top Windows", command=self.inspect_ui
        )
        self.inspect_btn.grid(row=1, column=0, pady=10, padx=(0, 10), sticky="e")

        self.inspect_deep_btn = customtkinter.CTkButton(
            self.tab_ui,
            text="Deep Scan (Buttons/Input)",
            command=self.inspect_deep_ui,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.inspect_deep_btn.grid(row=1, column=1, pady=10, padx=(10, 0), sticky="w")

        self.tab_ui.grid_columnconfigure(0, weight=1)
        self.tab_ui.grid_columnconfigure(1, weight=1)

        # --- Window Mods Tab ---
        self.tab_mods.grid_columnconfigure(0, weight=1)

        self.mod_label = customtkinter.CTkLabel(
            self.tab_mods,
            text="Real-time Window Manipulation",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.mod_label.grid(row=0, column=0, pady=10)

        self.status_mod_label = customtkinter.CTkLabel(
            self.tab_mods, text="Target: Not Found - Click Find", text_color="red"
        )
        self.status_mod_label.grid(row=1, column=0, pady=5)

        self.find_btn = customtkinter.CTkButton(
            self.tab_mods, text="Find Main Window", command=self.find_window_target
        )
        self.find_btn.grid(row=2, column=0, pady=10)

        # Controls Frame
        self.controls_frame = customtkinter.CTkFrame(self.tab_mods)
        self.controls_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.controls_frame.grid_columnconfigure(0, weight=1)

        # Opacity
        self.opacity_label = customtkinter.CTkLabel(self.controls_frame, text="Opacity")
        self.opacity_label.grid(row=0, column=0, pady=(10, 0))
        self.opacity_slider = customtkinter.CTkSlider(
            self.controls_frame,
            from_=30,
            to=255,
            number_of_steps=225,
            command=self.change_opacity,
        )
        self.opacity_slider.set(255)
        self.opacity_slider.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Topmost
        self.topmost_switch = customtkinter.CTkSwitch(
            self.controls_frame, text="Always on Top", command=self.toggle_topmost
        )
        self.topmost_switch.grid(row=2, column=0, padx=20, pady=15)

        # Title
        self.title_entry = customtkinter.CTkEntry(
            self.controls_frame, placeholder_text="New Window Title"
        )
        self.title_entry.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.title_btn = customtkinter.CTkButton(
            self.controls_frame, text="Set Title", command=self.set_window_title
        )
        self.title_btn.grid(row=4, column=0, padx=20, pady=5)

        self.target_hwnd = 0

        # --- Automation Tab ---
        self.tab_auto.grid_columnconfigure(0, weight=1)

        self.auto_label = customtkinter.CTkLabel(
            self.tab_auto,
            text="Experimental Automation",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.auto_label.grid(row=0, column=0, pady=10)

        self.auto_status_label = customtkinter.CTkLabel(
            self.tab_auto, text="Ready", text_color="gray"
        )
        self.auto_status_label.grid(row=1, column=0, pady=5)

        # Message Injection
        self.auto_entry = customtkinter.CTkEntry(
            self.tab_auto, placeholder_text="Message to type..."
        )
        self.auto_entry.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.send_text_btn = customtkinter.CTkButton(
            self.tab_auto,
            text="Type Text (AutoSuggestTextArea)",
            command=self.send_automation_text,
        )
        self.send_text_btn.grid(row=3, column=0, padx=20, pady=5)

        self.send_key_btn = customtkinter.CTkButton(
            self.tab_auto,
            text="Send 'Enter' Key",
            command=self.send_enter_key,
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.send_key_btn.grid(row=4, column=0, padx=20, pady=20)

        # Initial Load
        self.refresh_process_info()
        self.scan_files()

    def refresh_process_info(self):
        self.process_textbox.configure(state="normal")
        self.process_textbox.delete("0.0", "end")

        details = DebugTools.get_line_process_details()
        system_info = DebugTools.get_system_info()

        report = f"--- System Info ---\n"
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

    def scan_files(self):
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

    def inspect_ui(self):
        self.ui_textbox.configure(state="normal")
        self.ui_textbox.delete("0.0", "end")

        self.ui_textbox.insert("end", "Analyzing UI Windows...\n")
        self.update()

        report = ""

        # 1. Scan LINE Processes
        procs = LineManager.get_line_processes()
        if procs:
            for proc in procs:
                pid = proc.pid
                windows = UIInspector.get_window_structure(pid)
                if windows:
                    report += f"\n[LINE] Process PID: {pid} ({proc.name()})\n"
                    report += self._format_windows(windows, 0)
        else:
            report += "No visible windows found for LINE processes.\n"

        # 2. Scan Self (N-LINE)
        import os

        self_pid = os.getpid()
        self_windows = UIInspector.get_window_structure(self_pid)
        if self_windows:
            report += f"\n[N-LINE (Self)] Process PID: {self_pid}\n"
            report += self._format_windows(self_windows, 0)

        if not report:
            report = "No windows found."

        self.ui_textbox.insert("end", report)
        self.ui_textbox.configure(state="disabled")

    def inspect_deep_ui(self):
        """
        Performs a deep scan using UI Automation to find internal controls.
        """
        self.ui_textbox.configure(state="normal")
        self.ui_textbox.delete("0.0", "end")
        self.ui_textbox.insert("end", "Performing Deep Scan (SLOW)... wait...\n")
        self.update()

        procs = LineManager.get_line_processes()
        if not procs:
            self.ui_textbox.insert("end", "Error: LINE process not running.\n")
            self.ui_textbox.configure(state="disabled")
            return

        report = ""
        for proc in procs:
            pid = proc.pid
            report += f"\n--- Deep Scan for PID: {pid} ({proc.name()}) ---\n"
            tree = UIInspector.get_extensive_ui_tree(pid)
            report += tree + "\n"

        if not report.strip():
            report = "No accessible UI elements found via UIA."

        self.ui_textbox.insert("end", report)
        self.ui_textbox.configure(state="disabled")

    def _format_windows(self, windows, depth):
        output = ""
        indent = "  " * depth
        for win in windows:
            vis = "[Visible]" if win["visible"] else "[Hidden]"
            title = win["title"] if win["title"] else "<No Title>"
            output += f"{indent}{vis} '{title}' (Class: {win['class']}, Size: {win['size']})\n"
            if win["children"]:
                output += self._format_windows(win["children"], depth + 1)
        return output

    # --- Window Manipulation Handlers ---

    def find_window_target(self):
        # Improved: Find by PID first, which is more robust than title search
        procs = LineManager.get_line_processes()
        hwnd = 0
        if procs:
            # Try to find window of the first LINE process
            hwnd = WindowManipulator.find_process_window(procs[0].pid)

        if not hwnd:
            # Fallback to old title search or just fail
            hwnd = WindowManipulator.find_main_window()

        if hwnd:
            self.target_hwnd = hwnd
            self.status_mod_label.configure(
                text=f"Target: Found (HWND: {hwnd})", text_color="green"
            )
        else:
            self.target_hwnd = 0
            self.status_mod_label.configure(
                text="Target: Not Found (Is LINE running?)", text_color="red"
            )

    def change_opacity(self, value):
        if self.target_hwnd:
            WindowManipulator.set_opacity(self.target_hwnd, int(value))
            self.opacity_label.configure(text=f"Opacity ({int(value / 2.55)}%)")

    def toggle_topmost(self):
        if self.target_hwnd:
            WindowManipulator.set_always_on_top(
                self.target_hwnd, bool(self.topmost_switch.get())
            )

    def set_window_title(self):
        if self.target_hwnd:
            new_title = self.title_entry.get()
            if new_title:
                WindowManipulator.set_title(self.target_hwnd, new_title)

    # --- Automation Handlers ---

    def send_automation_text(self):
        text = self.auto_entry.get()
        if not text:
            self.auto_status_label.configure(
                text="Please enter text.", text_color="yellow"
            )
            return

        result = AutomationManager.type_in_chat(text)
        color = "green" if "Success" in result else "red"
        self.auto_status_label.configure(text=result, text_color=color)

    def send_enter_key(self):
        result = AutomationManager.press_send()
        color = "green" if "Success" in result else "red"
        self.auto_status_label.configure(text=result, text_color=color)
