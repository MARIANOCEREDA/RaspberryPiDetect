import sys
import cv2
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from yoloV5.custom_detect import main as run_detect
from detect_sticks import Ui_MainWindow

#variables globales
sticks=0
total_sticks=0
sitck_correct=0
conf=0
n_package=""
diameter=0

from PyQt5.QtWidgets import QApplication, QMessageBox

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


#cuando se clickea detectar saca la foto, corre el programa detect_custom, detecta los palos y nos muestra el resultado
def on_detect_click():
    global sitck_correct, total_sticks, sticks,conf, diameter,n_package
    sticks=0
    diameter=0
    ui.out_sticks.setPlainText(str(sticks))
    ui.out_diameter.setPlainText(str(round(diameter, 3))+" cm")
 
    if conf==0 :
        
        diameter, sticks, image_detect_path, image_path = run_detect()

        ui.out_sticks.setPlainText(str(sticks))
        ui.out_diameter.setPlainText(str(round(diameter, 3)) + " cm")

        img_stick = QPixmap(image_path)
        img_stick_500 = img_stick.scaled(500, 500)

        ui.out_img.setPixmap(img_stick_500)    

        img_detecction = QPixmap(image_detect_path)
        img_detecction_500 = img_detecction.scaled(500, 500)
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
        "font: 16pt \"Consolas\";\n"
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
        "font: 16pt \"Consolas\";\n"
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
        ui.in_npackge.setEnabled(False)

        n_package=ui.in_npackge.text()
        style_conf(conf)
        conf=1
    else:
        ui.in_npackge.setEnabled(True)
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

       
if __name__ == "__main__":

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

    sys.exit(app.exec_())