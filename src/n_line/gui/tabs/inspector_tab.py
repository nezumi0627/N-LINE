import customtkinter
import threading
import keyboard
import datetime
from n_line.core.ui_inspector import UIInspector
from n_line.core.line_manager import LineManager


class InspectorTab(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.ui_textbox = customtkinter.CTkTextbox(
            self, font=("Consolas", 12), wrap="none"
        )
        self.ui_textbox.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )

        self.inspect_btn = customtkinter.CTkButton(
            self, text="Scan Top Windows", command=self.inspect_ui
        )
        self.inspect_btn.grid(row=1, column=0, pady=10, padx=(0, 10), sticky="e")

        self.inspect_deep_btn = customtkinter.CTkButton(
            self,
            text="Deep Scan (Buttons/Input)",
            command=self.inspect_deep_ui,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.inspect_deep_btn.grid(row=1, column=1, pady=10, padx=(10, 0), sticky="w")

        self.extract_classes_btn = customtkinter.CTkButton(
            self,
            text="Extract Style Classes",
            command=self.extract_style_classes,
            fg_color="#d35400",
            hover_color="#e67e22",
        )
        self.extract_classes_btn.grid(
            row=1, column=2, pady=10, padx=(10, 10), sticky="w"
        )

        # --- Point-to-Inspect Features ---
        self.inspector_frame = customtkinter.CTkFrame(self)
        self.inspector_frame.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.inspector_frame.grid_columnconfigure(1, weight=1)

        self.inspector_switch = customtkinter.CTkSwitch(
            self.inspector_frame,
            text="Inspector Mode (Ctrl+Shift to Spy)",
            command=self.toggle_inspector_mode,
        )
        self.inspector_switch.grid(row=0, column=0, padx=10, pady=5)

        self.inspector_status = customtkinter.CTkLabel(
            self.inspector_frame, text="OFF", text_color="gray"
        )
        self.inspector_status.grid(row=0, column=1, padx=10, sticky="w")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

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

    def toggle_inspector_mode(self):
        if self.inspector_switch.get():
            self.inspector_status.configure(
                text="ON (Monitoring 'ctrl+shift')", text_color="green"
            )
            keyboard.add_hotkey("ctrl+shift", self.on_inspector_hotkey)
        else:
            self.inspector_status.configure(text="OFF", text_color="gray")
            try:
                keyboard.remove_hotkey("ctrl+shift")
            except Exception:
                pass

    def on_inspector_hotkey(self):
        # Run inspection in a separate thread to avoid freezing key hook
        # Simple throttling: check if we are already inspecting or just spamming
        if hasattr(self, "_inspecting") and self._inspecting:
            return
        self._inspecting = True
        threading.Thread(target=self._run_point_inspection).start()

    def _run_point_inspection(self):
        import uiautomation as auto

        try:
            # Need to initialize COM for this thread
            with auto.UIAutomationInitializerInThread(debug=False):
                try:
                    element = UIInspector.get_element_at_cursor()
                    if not element:
                        return

                    details = UIInspector.get_detailed_info(element)
                    UIInspector.highlight_element(element)

                    # Format output
                    report = f"\n--- SPY RESULT ({datetime.datetime.now().strftime('%H:%M:%S')}) ---\n"
                    report += f"Name: {details.get('Name')}\n"
                    report += f"Type: {details.get('ControlType')}\n"
                    report += f"Class: {details.get('ClassName')}\n"
                    report += f"AutoID: {details.get('AutomationId')}\n"
                    report += f"Process: {details.get('ProcessId')}\n"
                    report += f"Rect: {details.get('Rect')}\n"
                    report += f"Patterns: {', '.join(details.get('Patterns'))}\n"
                    if details.get("Value"):
                        report += f"Value: {details.get('Value')}\n"

                    # --- Legacy/Extra Info ---
                    if "LegacyName" in details:
                        report += f"Legacy Name: {details.get('LegacyName')}\n"
                    if "LegacyDescription" in details and details.get(
                        "LegacyDescription"
                    ):
                        report += f"Legacy Desc: {details.get('LegacyDescription')}\n"
                    if "LegacyValue" in details and details.get("LegacyValue"):
                        report += f"Legacy Value: {details.get('LegacyValue')}\n"

                    # --- Ancestor Chain ---
                    if details.get("Ancestors"):
                        report += "\n[Ancestors]:\n"
                        for anc in details["Ancestors"]:
                            report += f"  ^ {anc}\n"

                    # Write to textbox safely
                    self.after(0, lambda: self._update_ui_textbox(report))
                except Exception:
                    # Log if needed, or silently fail on COM error during heavy load
                    pass
        finally:
            self._inspecting = False

    def _update_ui_textbox(self, text):
        self.ui_textbox.configure(state="normal")
        self.ui_textbox.insert("end", text)
        self.ui_textbox.see("end")
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

    def extract_style_classes(self):
        """
        Scans LINE UI tree and extracts unique ClassNames for QSS styling.
        """
        self.ui_textbox.configure(state="normal")
        self.ui_textbox.delete("0.0", "end")
        self.ui_textbox.insert("end", "Scanning for potential QSS classes... wait...\n")
        self.update()

        procs = LineManager.get_line_processes()
        if not procs:
            self.ui_textbox.insert("end", "Error: LINE process not running.\n")
            self.ui_textbox.configure(state="disabled")
            return

        report = ""
        all_classes = set()

        for proc in procs:
            pid = proc.pid
            classes = UIInspector.get_unique_style_classes(pid)
            for cls in classes:
                all_classes.add(cls)

        if all_classes:
            report = "\n--- Found Potential QSS Selectors ---\n"
            report += "Note: Valid QSS selectors usually match C++ Class Names (e.g. LcWidget).\n\n"
            for cls in sorted(list(all_classes)):
                if cls:  # Skip empty
                    report += f"{cls}\n"
        else:
            report = "No classes found or scan failed."

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

    def cleanup(self):
        try:
            keyboard.remove_hotkey("ctrl+shift")
        except Exception:
            pass
