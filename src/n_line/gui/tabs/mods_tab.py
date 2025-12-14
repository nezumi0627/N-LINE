import customtkinter
from n_line.core.line_manager import LineManager
from n_line.core.window_manipulator import WindowManipulator


class ModsTab(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.target_hwnd = 0  # Initialize to avoid AttributeError

        self.mod_label = customtkinter.CTkLabel(
            self,
            text="Real-time Window Manipulation",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.mod_label.grid(row=0, column=0, pady=10)

        self.status_mod_label = customtkinter.CTkLabel(
            self, text="Target: Not Found - Click Find", text_color="red"
        )
        self.status_mod_label.grid(row=1, column=0, pady=5)

        self.find_btn = customtkinter.CTkButton(
            self, text="Find Main Window", command=self.find_window_target
        )
        self.find_btn.grid(row=2, column=0, pady=10)

        # Controls Frame
        self.controls_frame = customtkinter.CTkFrame(self)
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

        # --- Exploit (Argument Injection) ---
        self.exploit_label = customtkinter.CTkLabel(
            self.controls_frame,
            text="Exploit (Argument Injection)",
            text_color="#e74c3c",
            font=customtkinter.CTkFont(weight="bold"),
        )
        self.exploit_label.grid(row=5, column=0, pady=(15, 0))

        self.arg_entry = customtkinter.CTkEntry(
            self.controls_frame, placeholder_text="e.g. --remote-debugging-port=8080"
        )
        self.arg_entry.grid(row=6, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.relaunch_btn = customtkinter.CTkButton(
            self.controls_frame,
            text="Inject & Relaunch",
            command=self.inject_arguments,
            fg_color="#c0392b",
            hover_color="#e74c3c",
        )
        self.relaunch_btn.grid(row=7, column=0, padx=20, pady=5)

        # --- Debug Port Checker ---
        self.debug_port_frame = customtkinter.CTkFrame(
            self.controls_frame, fg_color="transparent"
        )
        self.debug_port_frame.grid(row=8, column=0, padx=20, pady=(15, 5), sticky="ew")

        self.port_label = customtkinter.CTkLabel(self.debug_port_frame, text="Port:")
        self.port_label.pack(side="left", padx=(0, 5))

        self.port_entry = customtkinter.CTkEntry(
            self.debug_port_frame, width=60, placeholder_text="8080"
        )
        self.port_entry.pack(side="left")
        self.port_entry.insert(0, "8080")

        self.check_port_btn = customtkinter.CTkButton(
            self.debug_port_frame,
            text="Scan /json",
            width=100,
            command=self.check_debug_port,
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.check_port_btn.pack(side="left", padx=10)

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

    def inject_arguments(self):
        """
        Exploit: Relaunch LINE with custom arguments directly.
        """
        args = self.arg_entry.get()
        if not args:
            self.status_mod_label.configure(
                text="No arguments specified.", text_color="yellow"
            )
            return

        import shlex

        try:
            # Basic usage: just pass the raw string if simple, or parse if complex.
            # LineManager expects a list of args.
            arg_list = shlex.split(args)

            self.status_mod_label.configure(
                text="Injecting payload...", text_color="orange"
            )

            # Execute
            success = LineManager.relaunch_with_params(arg_list)

            if success:
                self.status_mod_label.configure(
                    text="Exploit Successful: Process Relaunched", text_color="green"
                )
                # Reset state
                self.target_hwnd = 0
            else:
                self.status_mod_label.configure(
                    text="Exploit Failed: Could not relaunch", text_color="red"
                )
        except Exception as e:
            self.status_mod_label.configure(text=f"Error: {e}", text_color="red")
