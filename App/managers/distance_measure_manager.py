import RPi.GPIO as GPIO
import time
from config.logger_config import get_logger
from PyQt5.QtCore import QThread, pyqtSignal

from managers.errors import WarningMessage

# Setup global variables
logger = get_logger("DistanceMeasure")
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24


class MeasureDistanceThread(QThread):

    finished = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self._stop_flag = False

    def run(self):

        while not self._stop_flag:
            # set Trigger to HIGH
            logger.debug("Triggerint SET...")
            GPIO.output(GPIO_TRIGGER, True)

            # set Trigger after 0.01ms to LOW
            logger.debug("Triggerint RESET...")
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            start_time = time.time()
            stop_time = time.time()

            # save start_time
            while GPIO.input(GPIO_ECHO) == 0:
                start_time = round(time.time(), 4)

            # save time of arrival
            while GPIO.input(GPIO_ECHO) == 1:
                stop_time = round(time.time(), 4)

            # time difference between start and arrival
            time_elapsed = stop_time - start_time
            distance = round(time_elapsed * 17150, 2)

            logger.info("Measured distance: " + str(distance))

            self.finished.emit(float(distance))
            time.sleep(1)

    def stop(self):
        # Set the stop flag to indicate the thread should stop
        logger.debug("Stopping measure distance worker thread ...")
        GPIO.cleanup()
        self._stop_flag = True
        
        
 
