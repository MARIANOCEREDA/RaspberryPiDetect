import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.uic import load_ui

class MainWindow(QMainWindow):

    def __init__(self, ui_file_path:str) -> None:
        super().__init__(MainWindow, self)

        load_ui(ui_file_path)

    pass