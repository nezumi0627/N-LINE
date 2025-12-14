from n_line.gui.app import NLineApp

if __name__ == "__main__":
    app = NLineApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
