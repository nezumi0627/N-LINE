import customtkinter
import os
import shutil
from tkinter import filedialog
from n_line.core.line_manager import LineManager


class QSSTab(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)  # Editor column
        self.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Controls ---
        self.controls_frame = customtkinter.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.controls_frame.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self.controls_frame,
            text="Style Manager",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, pady=(10, 5))

        self.desc_label = customtkinter.CTkLabel(
            self.controls_frame,
            text="Inject & Edit Qt Stylesheets.\nWARNING: Relaunch required.",
            text_color="gray",
            font=customtkinter.CTkFont(size=11),
        )
        self.desc_label.grid(row=1, column=0, pady=(0, 10))

        # File Selection
        self.file_label = customtkinter.CTkLabel(
            self.controls_frame,
            text="Target Style File (.qss)",
            font=customtkinter.CTkFont(size=12, weight="bold"),
        )
        self.file_label.grid(row=2, column=0, pady=(10, 0))

        self.path_entry = customtkinter.CTkEntry(
            self.controls_frame, placeholder_text="Select a .qss file..."
        )
        self.path_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.browse_btn = customtkinter.CTkButton(
            self.controls_frame,
            text="Browse File...",
            command=self.browse_file,
            fg_color="#34495e",
            hover_color="#2c3e50",
        )
        self.browse_btn.grid(row=4, column=0, padx=10, pady=5)

        # Actions
        self.action_separator = customtkinter.CTkLabel(
            self.controls_frame, text="--- Actions ---", text_color="gray"
        )
        self.action_separator.grid(row=5, column=0, pady=(15, 5))

        self.load_btn = customtkinter.CTkButton(
            self.controls_frame,
            text="Load to Editor ->",
            command=self.load_to_editor,
            fg_color="#3498db",
        )
        self.load_btn.grid(row=6, column=0, padx=10, pady=5)

        self.deploy_btn = customtkinter.CTkButton(
            self.controls_frame,
            text="Deploy to LINE Folder",
            command=self.deploy_file,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.deploy_btn.grid(row=7, column=0, padx=10, pady=5)

        self.relaunch_btn = customtkinter.CTkButton(
            self.controls_frame,
            text="Apply & Relaunch LINE",
            command=self.relaunch_line,
            fg_color="#d35400",
            hover_color="#e67e22",
            height=40,
        )
        self.relaunch_btn.grid(row=8, column=0, padx=10, pady=20)

        self.status_label = customtkinter.CTkLabel(
            self.controls_frame, text="Ready.", text_color="gray", wraplength=200
        )
        self.status_label.grid(row=9, column=0, pady=5)

        # --- Right Panel: Editor ---
        self.editor_frame = customtkinter.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)

        self.editor_header = customtkinter.CTkFrame(self.editor_frame, height=30)
        self.editor_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.editor_label = customtkinter.CTkLabel(
            self.editor_header,
            text="QSS Editor",
            font=customtkinter.CTkFont(weight="bold"),
        )
        self.editor_label.pack(side="left", padx=5)

        self.save_btn = customtkinter.CTkButton(
            self.editor_header,
            text="Save Changes",
            command=self.save_editor_content,
            width=100,
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.save_btn.pack(side="right", padx=5)

        self.editor_textbox = customtkinter.CTkTextbox(
            self.editor_frame, font=("Consolas", 13), wrap="none"
        )
        self.editor_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.editor_textbox.insert(
            "0.0",
            "/* Open a file or start typing... */\n\nQWidget {\n    /* background-color: white; */\n}",
        )

        # Initial checks
        if os.path.exists("test_style.qss"):
            self.path_entry.insert(0, os.path.abspath("test_style.qss"))
            self.load_to_editor()

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("QSS Files", "*.qss"), ("All Files", "*.*")]
        )
        if file_path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, file_path)
            self.load_to_editor()

    def load_to_editor(self):
        path = self.path_entry.get().strip()
        if not path or not os.path.exists(path):
            self.status_label.configure(text="File not found.", text_color="red")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor_textbox.delete("0.0", "end")
            self.editor_textbox.insert("0.0", content)
            self.status_label.configure(
                text=f"Loaded: {os.path.basename(path)}", text_color="green"
            )
        except Exception as e:
            self.status_label.configure(text=f"Load Error: {str(e)}", text_color="red")

    def save_editor_content(self):
        path = self.path_entry.get().strip()
        if not path:
            # If no path, ask where to save
            path = filedialog.asksaveasfilename(
                defaultextension=".qss", filetypes=[("QSS Files", "*.qss")]
            )
            if not path:
                return
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

        content = self.editor_textbox.get("0.0", "end")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status_label.configure(
                text="File saved successfully.", text_color="green"
            )
        except Exception as e:
            self.status_label.configure(text=f"Save Error: {str(e)}", text_color="red")

    def deploy_file(self):
        """Copies the current file to LINE's local appdata folder for easier loading."""
        source_path = self.path_entry.get().strip()
        if not source_path or not os.path.exists(source_path):
            self.status_label.configure(
                text="Select a valid file first.", text_color="red"
            )
            return

        user_profile = os.environ.get("USERPROFILE")
        target_dir = os.path.join(user_profile, "AppData", "Local", "LINE")

        if not os.path.exists(target_dir):
            self.status_label.configure(
                text="LINE Data folder not found.", text_color="red"
            )
            return

        filename = os.path.basename(source_path)
        target_path = os.path.join(target_dir, filename)

        try:
            # Save first if editing
            self.save_editor_content()
            shutil.copy2(source_path, target_path)
            self.status_label.configure(
                text=f"Deployed to: {target_path}", text_color="green"
            )
            # Update entry to point to deployed file
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, target_path)
        except Exception as e:
            self.status_label.configure(
                text=f"Deploy Error: {str(e)}", text_color="red"
            )

    def relaunch_line(self):
        args_text = self.path_entry.get()
        if not args_text:
            self.status_label.configure(
                text="Error: Please enter a filename.", text_color="red"
            )
            return

        # Prepare arguments
        # If absolute path is given with spaces, quote it
        clean_path = args_text.replace('"', "")
        final_args = ["-stylesheet", clean_path]

        # Call manager
        self.status_label.configure(text="Relaunching...", text_color="blue")
        self.update()
        result = LineManager.relaunch_with_params(final_args)
        self.status_label.configure(
            text=result, text_color="green" if "Success" in result else "red"
        )
