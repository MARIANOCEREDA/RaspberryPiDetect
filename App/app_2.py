import sys
import cv2
import threading
import os
import numpy as np
import yaml
import time
import logging

from App.yoloV5.custom_detect import main as run_detect
from Gui_.detect_sticks_app import Ui_MainWindow

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt  # Agrega esta línea


from managers.api_requests import PackageDetectAPIRequests
from managers.local_storage_manager import LocalStorageManager

from picamera2.picamera2 import Picamera2
from config.logger_config import get_logger

from managers.errors import WarningMessage

# Setup global variables
logger = get_logger("DetectSticksApp")
config_data = None
video_thread = None

def setup_config_file(env):
    CONFIG_FILE = os.path.dirname(__file__) + f"/config/config.{env}.yaml"
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    return config

class DetectSticksApp(QApplication):

    def __init__(self, arg) -> None:
        super().__init__(arg)
        self.sticks = 0
        self.total_sticks = 0
        self.stick_correct = 0
        self.conf = 0
        self.n_package = ""
        self.diameter = 0
        self.picam:Picamera2 = None
        self.confirm = False

        # Windows development variables
        self.capture_video = False
        self.current_frame = None
    
    def _setup_button_callbacks(self):
        self.ui.button_detect.clicked.connect(self.on_detect_click)
        self.ui.button_plas.clicked.connect(self.on_plus_click)
        self.ui.button_less.clicked.connect(self.on_less_click)
        self.ui.button_send.clicked.connect(self.on_send_click)
        self.ui.button_conf.clicked.connect(self.on_confirm_click)
        self.ui.button_close.clicked.connect(self.on_close_click)
        self.ui.button_max.clicked.connect(self.on_toggle_maximize)
        self.ui.button_min.clicked.connect(self.on_min_click)
        self.aboutToQuit.connect(self.on_app_quit)
        
    def _setup_gui(self):
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.setWindowState(Qt.WindowFullScreen)
        self.main_window.show()
    
    def run(self):
        self._setup_gui()
        self._setup_button_callbacks()
        self.start_camera()
    
    def show_warning_message_box(self, message:WarningMessage):

        message = message if isinstance(message, str) else message.value
        QMessageBox.warning(None, 'Advertencia', message, QMessageBox.Ok)


    def show_success_message_box(self, message:str):
        QMessageBox.information(None, 'Éxito', message, QMessageBox.Ok)

    
    def on_detect_click(self):
        '''
        on_detect_click

        Description:
            Callback de boton 'detectar'.
            Ejecuta el algoritmo de detección y setea los resultados.
        '''
 
        self.sticks = 0
        self.diameter = 0

        self.ui.out_sticks.setPlainText(str(self.sticks))
        self.ui.out_diameter.setPlainText(str(round(self.diameter, 3)) + " cm")
    
        if not self.confirm:

            size = (config_data["camera"]["res_x"], config_data["camera"]["res_y"])

            if config_data["environment"] == "prod":
                #path = config_data["local_storage_folder"] + "/image.jpeg"
                path = "/home/mariano/workspace/tesis/test_photos/image.jpeg"

                cam_cfg = self.ui.picam.create_still_configuration(main={"size": size},
                                                               lores={"size": (640, 480)},
                                                               display="lores")
            
                self.ui.picam.switch_mode_and_capture_file(cam_cfg, 
                                                           path, 
                                                           signal_function=self.ui.qpicamera2.signal_done)
            
            else:
                if self.current_frame is not None:
                    image_filename = "captura_.png"
                    cam_path = os.path.join(os.path.dirname(__file__), "capturs", "captura_.png")
                    self.current_frame.save(cam_path)

            logger.info("Starting detection ...")

            diameter, sticks, image_detect_path, image_path, message = run_detect()

            self.diameter = diameter
            self.sticks = sticks

            if self.sticks == 0:
                self.show_warning_message_box(WarningMessage.NOT_STICKS_DETECTED)

            else:
                self.ui.out_sticks.setPlainText(str(self.sticks))
                self.ui.out_diameter.setPlainText(str(round(self.diameter, 3)) + " cm")

                img_stick = QPixmap(image_path)

                img_stick_500 = img_stick.scaled(self.ui.out_img.size().width(), self.ui.out_img.size().height())
                self.ui.out_img.setPixmap(img_stick_500)    

                img_detecction = QPixmap(image_detect_path)
                img_detecction_500 = img_detecction.scaled(self.ui.out_img.size().width(), self.ui.out_img.size().height())
                self.ui.out_detect.setPixmap(img_detecction_500)
                self.stick_correct = 0
                self.ui.out_correction.setPlainText(str(self.stick_correct))
                self.total_sticks = self.sticks + self.stick_correct
                self.ui.out_total.setPlainText(str(self.total_sticks))

                success_message = f"""Palos detectados: {str(self.sticks)} \n
                                - Palos totales: {str(self.total_sticks)} \n
                                - Diametro Promedio: {str(round(self.diameter, 3))} \n
                                - Número de paquete: {str(self.n_package)}"""
                
                logger.info(f"{success_message}")

        else :
            self.show_warning_message_box(WarningMessage.NOT_MODIFY_AFTER_CONFIRM)


    def on_confirm_click(self):
        '''
        on_confirm_click

        Description:
            Callback boton 'Confirmar'
            Se le da el estilo para que cuando este cliqueado quede en negro.
            Ademas, setea la variable confirm, que es utilizada por los demás 
            métodos.
        '''

        if not self.confirm :
            self.ui.in_npackage.setEnabled(False)
            self.n_package = self.ui.in_npackage.text()
            self.ui.style_confirm_button(conf=False)
            self.confirm = True

        else:
            self.ui.in_npackage.setEnabled(True)
            self.ui.style_confirm_button(self.confirm)
            self.confirm = False


    def on_plus_click(self):
        '''
        on_plus_click

        Description:
            Callback de Boton '+'
            Agrega 1 palo a la correción y a los palos totales.
        '''

        if not self.confirm:
            self.stick_correct = self.stick_correct + 1
            self.ui.out_correction.setPlainText(str(self.stick_correct))
            total_sticks = self.sticks + self.stick_correct
            self.ui.out_total.setPlainText(str(total_sticks))

        else:
            self.show_warning_message_box(WarningMessage.NOT_MODIFY_AFTER_CONFIRM)
    
    def on_less_click(self):
        '''
        on_less_click

        Description:
            Callback de Boton '+'
            Resta 1 palo a la correción y a los palos totales.
        '''

        if not self.confirm:
            self.stick_correct = self.stick_correct - 1
            self.ui.out_correction.setPlainText(str(self.stick_correct))
            self.total_sticks = self.sticks + self.stick_correct
            self.ui.out_total.setPlainText(str(self.total_sticks))

        else :
            self.show_warning_message_box(WarningMessage.NOT_MODIFY_AFTER_CONFIRM)
    

    def on_send_click(self):
        '''
        on_send_click

        Description:
            Callback de boton 'Enviar'
            Realiza la request a la API para realizar un post de paquetes.
        '''

        if not self.confirm:
            self.show_warning_message_box(WarningMessage.CONFIRM_BEFORE_SEND)

        elif self.sticks == 0:
            self.show_warning_message_box(WarningMessage.DETECT_BEFORE_SEND)

        elif self.n_package == "":
            self.show_warning_message_box(WarningMessage.INPUT_PACKAGE_NUMBER)

        else:

            package_data = {
                "packageNumber": self.n_package,
                "sticksAmount": self.total_sticks,
                "stickType": "medio poste",
                "averageDiameter": self.diameter
            }

            logger.debug(package_data)

            api_manager = PackageDetectAPIRequests(package_data=package_data)
            local_storage_manager = LocalStorageManager(config_data, package_data=package_data)

            local_storage_result = local_storage_manager.store_data()

            api_result = api_manager.post_package()

            if local_storage_result:
                logger.info(f"Information succesfully stored in local fs.")
            
            else:
                logger.error(f"Information could not be stored in local fs.")

            if not api_result["success"]:
                response_code = api_result["code"]
                logger.debug(f"Not able to store data in the server: {response_code}")
                self.show_warning_message_box(WarningMessage.INFORMATION_NOT_STORED_IN_SERVER)

            else:
                response_from_server = api_result["response"]
                logger.debug(f"Information succesfully sent to the server: {response_from_server}")
                success_message = "La información fue enviada correctamente."
                self.show_success_message_box(success_message)


    def on_app_quit(self):

        global video_thread

        logger.info("Quitting app ...")

        if config_data["environment"] == "prod":
            self.ui.picam.close()
        else:
            video_thread.join()

        sys.exit()


    def on_close_click(self):
        QCoreApplication.instance().quit()

    
    def on_toggle_maximize(self):
        if self.main_window.isMaximized() or self.main_window.isFullScreen():
            self.main_window.showNormal()  # Restaura la ventana al tamaño normal
        else:
            self.main_window.setWindowState(Qt.WindowFullScreen)

    
    def on_min_click(self):
        self.main_window.showMinimized()  # Minimiza la ventana


    def start_camera_thread(self):

        global video_thread

        video_thread = threading.Thread(target=self.start_camera)
        video_thread.start()

    
    def start_camera(self):

        if config_data["environment"] == "prod":

            logger.info("Starting picamera camera ...")
            self.ui.picam.start()
        
        elif config_data["environment"] == "dev":

            cap = cv2.VideoCapture(0)
            self.capture_video = True

            while self.capture_video:
                ret, frame = cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = frame_rgb.shape
                    bytes_per_line = ch * w
                    img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(img)
                    self.current_frame = pixmap #image actual
                    scaled_pixmap=pixmap.scaled(self.ui.out_cam.size().width(), self.ui.out_cam.size().height())
                    self.ui.out_cam.setPixmap(scaled_pixmap)
                    self.processEvents()
        

if __name__ == "__main__":

    # Get the platform information to make initial configuration
    platform_info = sys.platform
    logger.info(f"Detected plaform: {platform_info}")

    if platform_info == "linux":
        config_data = setup_config_file(env="prod")

    elif platform_info == "windows":
        config_data = setup_config_file(env="dev")

    # Start Qt app
    qt_app = DetectSticksApp(sys.argv)
    qt_app.run()

    sys.exit(qt_app.exec_())

