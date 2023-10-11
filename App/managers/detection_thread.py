from config.logger_config import get_logger
from PyQt5.QtCore import QThread, pyqtSignal

from App.yoloV5.custom_detect import main as run_detect

# Setup global variables
logger = get_logger("DetectionThread")

class DetectionThread(QThread):

    finished = pyqtSignal(float, int, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stop_flag = False
        self.distance = 0

    def run(self):

        message = ""

        try:
            logger.info(f"Distance measured before detection: {self.distance}")
            diameter, sticks, image_detect_path, image_path, message = run_detect(self.distance)
            logger.info("Detection Finished.")
            self.finished.emit(diameter, sticks, image_detect_path, image_path, message)
        
        except Exception as e:
            logger.info("Detection Timed out.")
            message = "Exceso de tiempo intentando detectar!"
            self.finished.emit(0 ,0 ,"","", message)
    
    def set_distance(self, distance:float):
        self.distance = distance