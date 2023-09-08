import sys
import cv2
import threading
import os
import numpy as np
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from yoloV5.custom_detect import main as run_detect
from detect_sticks import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMessageBox

#variables globales
sticks=0
total_sticks=0
sitck_correct=0
conf=0
n_package=""
diameter=0
capture_video = True
current_frame = None

#Adventencia de enviar y confirmar, crea una ventana emergente con messagebox
def error_send(n):
    global sticks, diameter, total_sticks, n_package
    if n==1:
        error_message = "Confirmar antes de enviar"
        QMessageBox.warning(None, 'Advertencia', error_message, QMessageBox.Ok)
        
    if n==2:
        error_message = "Tienes que detectar antes de enviar"
        QMessageBox.warning(None, 'Advertencia', error_message, QMessageBox.Ok)

    if n==3:
        error_message = "Tienes que ingresar el número del paquete antes de enviar"
        QMessageBox.warning(None, 'Advertencia', error_message, QMessageBox.Ok)

    if n==4:
        error_message = "Palos detectados: "+ str(sticks)+"\n" + "Palos totales: "+str(total_sticks)+"\n" + "Diametro Promedio: "+str(round(diameter, 3))+"\n"+"Número de paquete: "+str(n_package)
        QMessageBox.information(None, 'Resultado', error_message, QMessageBox.Ok)

def error_confirm():
    error_message = "No puede modificar el programa luego de confirmar"
    QMessageBox.warning(None, 'Advertencia', error_message, QMessageBox.Ok)

def error_detect(message):
    error_message = message
    QMessageBox.warning(None, 'Advertencia', error_message, QMessageBox.Ok)


def linea_img():
    
    # Resolución de la imagen de la cámara Sony IMX219
    resolucion_horizontal = 3280  # Ancho de la imagen en píxeles

    # Escala en píxeles por metro
    escala_pixeles_por_metro = resolucion_horizontal / 1.0  # 1 metro en la imagen

    # Longitud real de la línea en metros
    longitud_real = 1.3

    # Profundidad deseada en metros
    profundidad_deseada = 1.0

    # Longitud en píxeles de la línea
    longitud_en_pixeles = int(longitud_real * escala_pixeles_por_metro)

    # Profundidad en píxeles desde el centro de la imagen
    profundidad_en_pixeles = int(profundidad_deseada * escala_pixeles_por_metro)

    # Crea una imagen en blanco con la resolución de la cámara
    imagen = np.zeros((2464, 3280, 3), dtype=np.uint8)

    # Coordenadas para dibujar la línea
    y = 1232  # Altura (vertical) del centro de la imagen
    start_x = (resolucion_horizontal // 2) - profundidad_en_pixeles
    end_x = start_x - longitud_en_pixeles
    print
    # Color de la línea (por ejemplo, verde en formato BGR)
    color = (0, 255, 0)

    # Grosor de la línea
    thickness = 2

    # Dibuja la línea en la imagen
    cv2.line(imagen, (start_x, y), (end_x, y), color, thickness)
    imagen_redimensionada = cv2.resize(imagen, (1000, 600))
    # Muestra la imagen resultante
    cv2.imshow('Imagen con línea', imagen_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#cuando se clickea detectar saca la foto, corre el programa detect_custom, detecta los palos y nos muestra el resultado
def on_detect_click():
    ui.tabWidget.setFixedSize(MainWindow.size().height()-58-30,MainWindow.size().height()-58)

    ui.out_img.setFixedSize(ui.tabWidget.size().width()-28, ui.tabWidget.size().width()-28)
    ui.out_detect.setFixedSize(ui.tabWidget.size().width()-28, ui.tabWidget.size().width()-28)

    global sitck_correct, total_sticks, sticks,conf, diameter,n_package, current_frame
    sticks=0
    diameter=0
    ui.out_sticks.setPlainText(str(sticks))
    ui.out_diameter.setPlainText(str(round(diameter, 3))+" cm")
 
    if conf==0 :
        if current_frame is not None:
            image_filename = "captura_.png"
            cam_path=os.path.join(os.path.dirname(__file__),"capturs", "captura_.png")
            current_frame.save(cam_path)

        diameter, sticks, image_detect_path, image_path, message = run_detect()

        if sticks==0:
            error_detect(message)
        else:
            ui.out_sticks.setPlainText(str(sticks))
            ui.out_diameter.setPlainText(str(round(diameter, 3)) + " cm")

            img_stick = QPixmap(image_path)

            img_stick_500 = img_stick.scaled(ui.tabWidget.size().width()-28, ui.tabWidget.size().width()-28)

            ui.out_img.setPixmap(img_stick_500)    

            img_detecction = QPixmap(image_detect_path)
            img_detecction_500 = img_detecction.scaled(ui.tabWidget.size().width()-28, ui.tabWidget.size().width()-28)
            ui.out_detect.setPixmap(img_detecction_500)
            sitck_correct=0
            ui.out_correction.setPlainText(str(sitck_correct))
            total_sticks=sticks+sitck_correct
            ui.out_total.setPlainText(str(total_sticks))
    else :
        error_confirm()

# cuando se cliequea el boton + agrega 1 stick a la correción y a los palos totales
def on_plus_click():
    global sitck_correct, total_sticks, sticks, conf
    if conf==0 :
        sitck_correct=sitck_correct+1
        ui.out_correction.setPlainText(str(sitck_correct))
        total_sticks=sticks+sitck_correct
        ui.out_total.setPlainText(str(total_sticks))
    else :
        error_confirm()

# cuando se cliequea el boton - quita 1 stick a la correción y a los palos totales
def on_less_click():
    global sitck_correct, total_sticks, sticks, conf

    if conf==0 :
        sitck_correct= sitck_correct-1
        ui.out_correction.setPlainText(str(sitck_correct))
        total_sticks=sticks+sitck_correct
        ui.out_total.setPlainText(str(total_sticks))
    else :
        error_confirm()

def style_conf(conf):
    if conf==0:
        ui.button_conf.setStyleSheet("QPushButton{\n"
        "font: 14pt \"Consolas\";\n"
        "color:rgb(255, 255,255);\n"
        "border:1px solid #93C6FF;\n"
        "background-color: rgb(0, 0, 0);\n"
        "border-radius:5px;\n"
        "\n"
        "}\n"
        "QPushButton:hover{\n"
        "background-color: rgb(70, 70, 70);\n"
        "border:1px solid #93C6FF;\n"
        "}\n"
        "")
    else: 
        ui.button_conf.setStyleSheet("QPushButton{\n"
        "font: 14pt \"Consolas\";\n"
        "color:rgb(255, 255,255);\n"
        "border:1px solid #93C6FF;\n"
        "background-color: rgb(70, 70, 70);\n"
        "border-radius:5px;\n"
        "\n"
        "}\n"
        "QPushButton:hover{\n"
        "background-color: rgb(0, 0, 0);\n"
        "border:1px solid #93C6FF;\n"
        "}\n"
        "")

#Boton confirmar, se le da el estilo para que cuando este cliqueado quede en  negro
def on_conf_click():
    global conf,n_package
    if conf==0 :
        ui.in_npackage.setEnabled(False)
        n_package=ui.in_npackage.text()
        style_conf(conf)
        conf=1
    else:
        ui.in_npackage.setEnabled(True)
        style_conf(conf)
        conf=0
        
#Boton enviar, si no esta confimar error.
def on_send_click():
    global conf, sticks, diameter,n_package
    if conf==0:
        error_send(1)
    elif sticks==0:
        error_send(2)
    elif n_package=="":
        error_send(3)
    else:
        error_send(4)

def VideoCam():
    global capture_video, current_frame
    cap = cv2.VideoCapture(0)
    while capture_video:
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)

            current_frame = pixmap #image actual
            ui.out_cam.setPixmap(pixmap)
            QApplication.processEvents()  # Actualiza la interfaz de usuario

def on_app_quit():
    global capture_video
    capture_video = False
    video_thread.join()  # Esperamos a que el hilo termine antes de salir por completo
    sys.exit()  # Salir después de asegurarse de que el hilo haya terminado

if __name__ == "__main__":
    #linea_img()
    #creamos la ventana principal
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # Click botones
    ui.button_detect.clicked.connect(on_detect_click)
    ui.button_plas.clicked.connect(on_plus_click)
    ui.button_less.clicked.connect(on_less_click)
    ui.button_send.clicked.connect(on_send_click)
    ui.button_conf.clicked.connect(on_conf_click)
    MainWindow.show()

    # Iniciar el hilo de captura de webcam
    video_thread = threading.Thread(target=VideoCam)
    video_thread.start()

     # Capturar el evento de cierre de la aplicación
    app.aboutToQuit.connect(on_app_quit)

    sys.exit(app.exec_())
