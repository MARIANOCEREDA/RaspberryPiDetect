import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import load_ui

class MainWindow(QMainWindow):

    def __init__(self, ui_file_path:str) -> None:
        super().__init__(MainWindow, self)

        load_ui(ui_file_path)

    pass