import sys
import cv2
import threading
import os
import yaml

# from App.yoloV5.custom_detect import main as run_detect
from Gui_.detect_sticks_app import Ui_MainWindow

from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt, QTimer


from managers.api_requests_thread import PackageDetectAPIRequests
from managers.local_storage_manager import LocalStorageManager
from managers.distance_measure_thread import MeasureDistanceThread
from managers.detection_thread import DetectionThread

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
    """
    DetectSticksApp

    Description:
        - Qt aplication principal

    Methods:
        _setup_button_callbacks: Configura los callbacks de los botones en la interfaz gráfica.
        _setup_gui: Inicializa y configura la interfaz gráfica de la aplicación.
        run: Inicia la aplicación configurando la interfaz gráfica y los hilos necesarios.
        show_warning_message_box: Muestra un cuadro de diálogo de advertencia con un mensaje.
        show_success_message_box: Muestra un cuadro de diálogo de éxito con un mensaje.
        start_camera_thread: Inicia un hilo para la cámara en entornos de desarrollo.
        start_camera: Inicializa la cámara, ya sea la cámara Raspberry Pi (producción) o la cámara principal (desarrollo).
        start_distance_measure_thread: Inicia un hilo para la medición de distancia.
        setup_detection_thread: Configura el hilo para la detección de palos.
        setup_api_request_thread: Configura el hilo para realizar solicitudes a la API.
    
    Callbaks:
        on_detect_click: Maneja el clic en el botón "Detectar".
        on_confirm_click: Maneja el clic en el botón "Confirmar".
        on_plus_click: Maneja el clic en el botón "+".
        on_less_click: Maneja el clic en el botón "-".
        on_send_click: Maneja el clic en el botón "Enviar".
        on_app_quit: Maneja el evento de salida de la aplicación.
        on_close_click: Maneja el clic en el botón de cierre.
        on_toggle_maximize: Maneja el clic en el botón de maximizar/restaurar ventana.
        on_min_click: Maneja el clic en el botón de minimizar ventana.

    Slots:
        distance_measure_slot: Maneja los resultados de la medición de distancia.
        detection_slot: Maneja los resultados de la detección de palos.
        package_send_slot: Maneja la respuesta de la API después de enviar los datos.
    """

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
        self.distance_measure_thread = None
        self.distance = 0
        self.image_detect_path = ""
        self.image_path = ""
        self.detection_thread = None
        self.api_request_thread = None

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
        self.setOverrideCursor(QCursor(Qt.OpenHandCursor))
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
        self.start_distance_measure_thread()
        self.setup_detection_thread()
        self.setup_api_request_thread()
    
    def show_warning_message_box(self, message:WarningMessage):
        '''
        show_warning_message_box

        Description:
            Muestra como pop-up de advertencia el mensaje enviado como parametro.
        
        Params:
            message (WarningMessage | str): Mensaje a enviar
        '''
        message = message if isinstance(message, str) else message.value
        QMessageBox.warning(None, 'Advertencia', message, QMessageBox.Ok)


    def show_success_message_box(self, message:str):
        '''
        show_warning_message_box

        Description:
            Muestra como pop-up de información el mensaje enviado como parametro.
        
        Params:
            message (str): Mensaje a enviar.
        '''
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
                path = config_data["local_storage_folder"] + "/image.jpeg"
                #path = "/home/mariano/workspace/tesis/test_photos/image.jpeg"

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
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.detection_thread.set_distance(self.distance) 
            self.distance_measure_thread.stop()
            self.detection_thread.start()

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
            self.ui.style_confirm_button(conf=True)
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

            QApplication.setOverrideCursor(Qt.WaitCursor)

            package_data = {
                "packageNumber": self.n_package,
                "sticksAmount": self.total_sticks,
                "stickType": "medio poste",
                "averageDiameter": self.diameter
            }

            logger.debug(package_data)

            logger.info("Sending information to server ...")
            self.api_request_thread.set_package_data(package_data)
            self.distance_measure_thread.stop()
            self.api_request_thread.start()

    def on_app_quit(self):
        '''
        on_app_quit

        Description:
            Hay 2 casos para prod y dev.
            - Cierra picam en prod.
            - Finaliza hilo de camara principal en dev.
        '''

        global video_thread

        logger.info("Quitting app ...")

        if config_data["environment"] == "prod":
            self.ui.picam.close()
            self.distance_measure_thread.stop(finish_app=True)
        else:
            video_thread.join()

        logger.info("Quitting app 2 ...")
        QCoreApplication.instance().quit()


    def on_close_click(self):
        '''
        on_close_click

        Description:
            Cierra Qt App.
        '''
        QCoreApplication.instance().quit()

    
    def on_toggle_maximize(self):
        '''
        on_toggle_maximize

        Description:
            Minimiza y maximiza la pantalla, dependiendo del estado previo.
        '''
        if self.main_window.isMaximized() or self.main_window.isFullScreen():
            self.main_window.showNormal()  # Restaura la ventana al tamaño normal
            
        else:
            self.main_window.setWindowState(Qt.WindowFullScreen)

    
    def on_min_click(self):
        '''
        on_min_clisk

        Description:
            Minimiza pantalla.
        '''
        self.main_window.showMinimized()  # Minimiza la ventana


    def start_camera_thread(self):
        '''
        start_camera_thread

        Description:
            Utilizado para comenzar el thread de la camara. Solo necesario en dev.
        '''

        global video_thread

        video_thread = threading.Thread(target=self.start_camera)
        video_thread.start()

    
    def start_camera(self):
        '''
        start_camera

        Description:
            Inicializa la camara. Hay 2 casos para prod y dev.
            - Picam en la raspberry.
            - Camara principal en windows.
        '''

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
    
    def distance_measure_slot(self, dist):
        self.distance = dist
        self.ui.out_distance_measure.setPlainText(str(dist))

    def start_distance_measure_thread(self):

        if config_data["environment"] == "prod":
            self.distance_measure_thread = MeasureDistanceThread()
            self.distance_measure_thread.finished.connect(self.distance_measure_slot)
            self.distance_measure_thread.start()

    
    def detection_slot(self, diameter, sticks, image_detect_path, image_path, message):

        QApplication.restoreOverrideCursor()

        self.sticks = sticks
        self.diameter = diameter
        self.image_detect_path = image_detect_path
        self.image_path

        if self.sticks == 0:
                self.show_warning_message_box(WarningMessage.NOT_STICKS_DETECTED)

        else:
            self.ui.out_sticks.setPlainText(str(self.sticks))
            self.ui.out_diameter.setPlainText(str(round(self.diameter, 3)) + " cm")

            img_stick = QPixmap(image_path)

            img_stick_500 = img_stick.scaled(self.ui.out_img.size().width(), self.ui.out_img.size().height())
            self.ui.out_img.setPixmap(img_stick_500)    

            img_detecction = QPixmap(self.image_detect_path)
            img_detecction_500 = img_detecction.scaled(self.ui.out_img.size().width(),
                                                        self.ui.out_img.size().height())
            
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

            if not self.distance_measure_thread.isRunning():
                self.distance_measure_thread.start()
    
    def setup_detection_thread(self) -> None:

        self.detection_thread = DetectionThread()
        self.detection_thread.finished.connect(self.detection_slot)
    
    def package_send_slot(self, api_response, package_data) -> None:

        local_storage_manager = LocalStorageManager(config_data, package_data=package_data)
        local_storage_result = local_storage_manager.store_data()

        if local_storage_result:
            logger.info(f"Information succesfully stored in local fs.")
        
        else:
            logger.error(f"Information could not be stored in local fs.")

        if not api_response["success"]:
            response_code = api_response["code"]
            logger.debug(f"Not able to store data in the server: {response_code}")
            QApplication.restoreOverrideCursor()

            message = ""

            if response_code == 409:
                message = f"{WarningMessage.INFORMATION_NOT_STORED_IN_SERVER.value} : El paquete con número {self.n_package} ya existe."
            else:
                message = WarningMessage.INFORMATION_NOT_STORED_IN_SERVER

            self.show_warning_message_box(message)

        else:
            response_from_server = api_response["response"]
            logger.debug(f"Information succesfully sent to the server: {response_from_server}")
            success_message = 'La información fue enviada correctamente.'
            QApplication.restoreOverrideCursor()
            self.show_success_message_box(success_message)
        
        if not self.distance_measure_thread.isRunning():
                self.distance_measure_thread.start()


    def setup_api_request_thread(self) -> None:

        self.api_request_thread = PackageDetectAPIRequests(config_server_data=config_data["server"])
        self.api_request_thread.finished.connect(self.package_send_slot)

        
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

