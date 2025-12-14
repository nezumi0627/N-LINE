import customtkinter
import os
from threading import Thread
import time
from n_line.core.line_manager import LineManager
from n_line.gui.debug_window import DebugWindow

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (default), "green", "dark-blue"


class NLineApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("N-LINE (Mod Manager)")
        self.geometry("600x550")
        self.resizable(True, True)

        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Footer

        # Header
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text="N-LINE",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        )
        self.title_label.pack(pady=10, padx=20, side="left")

        self.subtitle_label = customtkinter.CTkLabel(
            self.header_frame, text="Desktop Mod & Utility", text_color="gray"
        )
        self.subtitle_label.pack(pady=15, padx=20, side="left")

        # Content Frame
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(5, weight=1)

        # Status Section
        self.status_frame = customtkinter.CTkFrame(self.content_frame)
        self.status_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        self.status_label = customtkinter.CTkLabel(
            self.status_frame,
            text="Checking Status...",
            font=customtkinter.CTkFont(size=14),
        )
        self.status_label.pack(pady=10)

        # Actions
        self.launch_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Launch LINE",
            command=self.launch_line_action,
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.launch_btn.grid(row=1, column=0, padx=10, pady=20, sticky="ew")

        self.kill_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Kill LINE Process",
            command=self.kill_line_action,
            fg_color="#c0392b",
            hover_color="#e74c3c",
        )
        self.kill_btn.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        self.folder_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Open Install Folder",
            command=self.open_folder_action,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.folder_btn.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ew")

        self.cache_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Clear Cache",
            command=self.clear_cache_action,
            fg_color="#d35400",
            hover_color="#e67e22",
        )
        self.cache_btn.grid(row=2, column=1, padx=10, pady=(0, 20), sticky="ew")

        # Debug Tools
        self.debug_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Open Debug Tools",
            command=self.open_debug_window,
            fg_color="#34495e",
            hover_color="#2c3e50",
        )
        self.debug_btn.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew"
        )

        # Future Mods Section
        self.separator = customtkinter.CTkLabel(
            self.content_frame,
            text="--- Modifications (Coming Soon) ---",
            text_color="gray",
        )
        self.separator.grid(row=3, column=0, columnspan=2, pady=10)

        self.theme_btn = customtkinter.CTkButton(
            self.content_frame,
            text="Apply Dark N-LINE Theme",
            state="disabled",
            fg_color="#2980b9",
        )
        self.theme_btn.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        # Logger / Console
        self.log_textbox = customtkinter.CTkTextbox(self.content_frame, height=100)
        self.log_textbox.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.log_textbox.insert("0.0", "Welcome to N-LINE Project.\nReady.\n")
        self.log_textbox.configure(state="disabled")

        # Footer
        self.footer_label = customtkinter.CTkLabel(
            self.content_frame, text="N-LINE Manager v0.2.0", text_color="gray"
        )
        self.footer_label.grid(row=8, column=0, pady=10)

        # Start Monitor Thread
        self.monitor_running = True
        self.monitor_thread = Thread(target=self.monitor_status)
        self.monitor_thread.daemon = True  # Kill when app closes
        self.monitor_thread.start()

    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")

    def monitor_status(self):
        while self.monitor_running:
            try:
                is_running = LineManager.is_line_running()
                status_text = (
                    "LINE Status: APP RUNNING" if is_running else "LINE Status: STOPPED"
                )
                color = "#2ecc71" if is_running else "#e74c3c"  # Green or Red

                # Update UI thread-safely (mostly works in CTk, strictly should us after)
                self.status_label.configure(text=status_text, text_color=color)
            except Exception:
                pass
            time.sleep(2)

    def kill_line_action(self):
        self.log("Attempting to kill LINE process...")
        if LineManager.kill_line():
            self.log("Success: LINE process terminated.")
        else:
            self.log("Info: LINE was not running or could not be killed.")

    def launch_line_action(self):
        self.log(LineManager.launch_line())

    def clear_cache_action(self):
        self.log("Clearing LINE cache...")
        if LineManager.is_line_running():
            self.log("WARNING: Please close LINE before clearing cache.")
            return

        result = LineManager.clear_cache()
        self.log(result)

    def open_folder_action(self):
        path = LineManager.get_install_path()
        if path and os.path.exists(path):
            self.log(f"Opening folder: {path}")
            os.startfile(path)
        else:
            self.log("Error: Could not find LINE installation folder.")

    def open_debug_window(self):
        if (
            hasattr(self, "debug_window")
            and self.debug_window is not None
            and self.debug_window.winfo_exists()
        ):
            self.debug_window.focus()
        else:
            self.debug_window = DebugWindow(self)
            self.debug_window.focus()

    def on_closing(self):
        self.monitor_running = False
        self.destroy()


if __name__ == "__main__":
    app = NLineApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
