"""N-LINE エントリーポイント"""
from n_line.gui.app import NLineApp


def main() -> None:
    """メイン関数"""
    app = NLineApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
