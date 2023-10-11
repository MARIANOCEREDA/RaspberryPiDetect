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
        self.finish_complete_app = False

    def run(self):
        '''
        run

        Description:
            Inicializa y corre el hilo. Por cada loop while, realiza una medición de distancia.
        '''

        logger.info("Starting distance measure worker thread ...")

        while True:

            # set Trigger to HIGH
            logger.debug("Triggering SET...")
            GPIO.output(GPIO_TRIGGER, True)

            # set Trigger after 0.01ms to LOW
            logger.debug("Triggering RESET...")
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
            distance = round(time_elapsed * 17150, 0)

            logger.info("Measured distance: " + str(distance))

            if self._stop_flag and self.finish_complete_app:
                GPIO.cleanup()
                self.finished.emit(float(distance))
                break

            elif self._stop_flag:
                self._stop_flag = False
                self.finished.emit(float(distance))
                break

            self.finished.emit(float(distance))
            time.sleep(1)

        logger.debug("Measure distance worker thread stopped ...")

    def stop(self, finish_app=False):
        '''
        stop

        Description:
            Setea un flag para finalizar el hilo. Se puede finizar totalmente, de forma que no se puede reinicializar, 
            o parcialmente, con posiilidad de ser reejecutado.

        Parameters:

            - finish_app (boolean): Si es falso, permite que el hilo se vuelva a inicializar desde 
            la app principal. Si es verdadero, significa que la main app esta siendo finalizada tambien.
        '''
        logger.info("Stopping measure distance worker thread...")

        if finish_app:
            self.finish_complete_app = True
        self._stop_flag = True
        
        
 
