import sys
import os
from src.main_window import * 
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import load_ui

UI_FILE_PATH = os.path.dirname(__file__) + "/ui/detect_sticks.ui"

if __name__ == "__main__":

    app = QApplication(sys.argv)
    my_app = MainWindow(app, UI_FILE_PATH)
    my_app.show()
    sys.exit(app.exec_())
