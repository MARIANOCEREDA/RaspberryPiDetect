from collections.abc import Callable, Iterable, Mapping
import time
from typing import Any
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QImage
from picamera2 import Picamera2, Preview
import threading

class CameraThread(threading.Thread):

    def __init__(self, ui) -> None:
        super().__init__()
        self.picam = Picamera2()
        self._configure_camera()
        self.ui = ui
        self.running = True
    
    def _configure_camera(self):
        self.photo_config = {
            "resolution":{
                    "x":3000,
                    "y":2000
            }
        }
        size = (self.photo_config["resolution"]["x"], self.photo_config["resolution"]["y"])
        config = self.picam.create_preview_configuration(main={"size": size}, lores={"size": (640, 480)}, display="lores")
        self.picam.configure(config)

    
    def start(self):
    
        for frame in self.picam.start_preview(Preview.QT):
            if not self.running:
                break
            image = frame.array
            h, w, ch = image.shape
            bytes_per_line = 3 * w
            q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(self.ui.size().width(), self.ui.size().height())
            self.ui.setPixmap(scaled_pixmap)
            QApplication.process_events()
            # time.sleep(0.03)

    def capture_photo(self, result_path:str):

        self.picam.capture_file(result_path)

    def stop(self):
        self.running = False
        self.picam.close()