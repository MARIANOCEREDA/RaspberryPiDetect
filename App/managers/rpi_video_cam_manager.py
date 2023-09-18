import time
from PyQt5.QtWidgets import QMainWindow, QApplication
from picamera2 import Picamera2, Preview

class RPiCameraManager:

    def __init__(self) -> None:
        self.picam = Picamera2()
        config = self.picam.create_preview_configuration()
        self.picam.configure(config)

    def start_loop(self):

        while True:
                
            self.picam.start_preview(Preview.QTGL)

            self.picam.start()
            self.picam.start_preview()
            
            QApplication.processEvents()
    
    def capture_photo(self, result_path:str):

        self.picam.capture_file(result_path)

    def finish(self):

        self.picam.close()