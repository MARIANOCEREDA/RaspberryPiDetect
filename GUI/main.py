import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

UI_FILE_PATH = os.path.dirname(__file__) + "/ui/detect_sticks.ui"

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple PyQt Window")
        self.setGeometry(100, 100, 400, 300)  # (x, y, width, height)

        label = QLabel("Hello, PyQt!", self)
        label.setGeometry(150, 150, 100, 30)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()

    sys.exit(app.exec_())
