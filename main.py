import sys
import os

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gui.app import NLineApp

if __name__ == "__main__":
    app = NLineApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
