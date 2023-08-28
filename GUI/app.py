import sys
import cv2
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QMessageBox, QLineEdit
from yoloV5.custom_detect import main
from detect_sticks import Ui_MainWindow

sticks=0
total_sticks=0
sitck_correct=0
conf=0

def error_send():
    textbox = QLineEdit()
    textbox.move(0, 0)
    textbox.resize(280, 40)
    textboxValue = textbox.text()
    QMessageBox.critical(None, 'Error', "Confimar antes de Enviar " + textboxValue, QMessageBox.Ok)
    textbox.clear()

def error_confirm():
    textbox = QLineEdit()
    textbox.move(20, 20)
    textbox.resize(280, 40)
    textboxValue = textbox.text()
    QMessageBox.critical(None, 'Error', "No puede modificar el programa luego de confirmar " + textboxValue, QMessageBox.Ok)
    textbox.clear()



def on_detect_click():
    global sitck_correct, total_sticks, sticks,conf
    if conf==0 :
        diameter,sticks,image_detect_path,image_path=main()
        ui.out_sticks.setPlainText(str(sticks))
        ui.out_diameter.setPlainText(str(round(diameter, 2))+" cm")
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

def on_plas_click():
    global sitck_correct, total_sticks, sticks, conf
    if conf==0 :
        sitck_correct=sitck_correct+1
        ui.out_correction.setPlainText(str(sitck_correct))
        total_sticks=sticks+sitck_correct
        ui.out_total.setPlainText(str(total_sticks))
    else :
        error_confirm()

def on_less_click():
    global sitck_correct, total_sticks, sticks, conf
    if conf==0 :
        sitck_correct=sitck_correct-1
        ui.out_correction.setPlainText(str(sitck_correct))
        total_sticks=sticks+sitck_correct
        ui.out_total.setPlainText(str(total_sticks))
    else :
        error_confirm()

def on_conf_click():
    global conf
    if conf==0 :
        conf=1
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
        conf=0
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
def on_send_click():
    global conf
    if conf==0:
        error_send()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.button_detect.clicked.connect(on_detect_click)
    ui.button_plas.clicked.connect(on_plas_click)
    ui.button_less.clicked.connect(on_less_click)
    ui.button_send.clicked.connect(on_send_click)
    ui.button_conf.clicked.connect(on_conf_click)

    MainWindow.show()
    sys.exit(app.exec_())