# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detect_sticks_app.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from picamera2.previews.qt import QGlPicamera2
from picamera2.picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
import yaml
import os

from config.logger_config import get_logger

# Setup global variables
logger = get_logger("DetectSticksUI")

qpicamera2 = None
config_data = None
RETRY_PICAM_ERROR = 2

def setup_config_file(env="prod"):
    CONFIG_FILE = os.path.dirname(__file__) + f"/../config/config.{env}.yaml"
    with open(CONFIG_FILE) as f:
        config_data = yaml.safe_load(f)
    return config_data


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        config_data = setup_config_file()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("QLabel{\n"
"color:rgb(255, 255,255);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_superior = QtWidgets.QFrame(self.frame)
        self.frame_superior.setMaximumSize(QtCore.QSize(16777215, 35))
        self.frame_superior.setStyleSheet("QFrame{\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton{\n"
"background-color: rgb(0, 0, 0);\n"
"border-radius:17px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(255, 255, 255);\n"
"}\n"
"QLabel{\n"
"font: 16pt \"Consolas\";\n"
"}\n"
"")
        self.frame_superior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_superior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_superior.setObjectName("frame_superior")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_superior)
        self.horizontalLayout.setContentsMargins(15, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame_superior)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(477, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_min = QtWidgets.QPushButton(self.frame_superior)
        self.button_min.setMinimumSize(QtCore.QSize(34, 34))
        self.button_min.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/gui/menos (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_min.setIcon(icon)
        self.button_min.setIconSize(QtCore.QSize(28, 28))
        self.button_min.setObjectName("button_min")
        self.horizontalLayout.addWidget(self.button_min)
        self.button_max = QtWidgets.QPushButton(self.frame_superior)
        self.button_max.setMinimumSize(QtCore.QSize(34, 34))
        self.button_max.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/gui/expandir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_max.setIcon(icon1)
        self.button_max.setIconSize(QtCore.QSize(28, 28))
        self.button_max.setObjectName("button_max")
        self.horizontalLayout.addWidget(self.button_max)
        self.button_close = QtWidgets.QPushButton(self.frame_superior)
        self.button_close.setMinimumSize(QtCore.QSize(34, 34))
        self.button_close.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/gui/cerrar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon2)
        self.button_close.setIconSize(QtCore.QSize(28, 28))
        self.button_close.setObjectName("button_close")
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout_2.addWidget(self.frame_superior)
        self.frame_inferior = QtWidgets.QFrame(self.frame)
        self.frame_inferior.setStyleSheet("")
        self.frame_inferior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_inferior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inferior.setObjectName("frame_inferior")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_inferior)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_datos = QtWidgets.QFrame(self.frame_inferior)
        self.frame_datos.setMinimumSize(QtCore.QSize(285, 0))
        self.frame_datos.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame_datos.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"")
        self.frame_datos.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_datos.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_datos.setObjectName("frame_datos")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_datos)
        self.verticalLayout_4.setContentsMargins(15, 0, 5, 15)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_botones = QtWidgets.QFrame(self.frame_datos)
        self.frame_botones.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frame_botones.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"\n"
"QPushButton{\n"
"font: 14pt \"Consolas\";\n"
"color:rgb(255, 255,255);\n"
"border:1px solid #93C6FF;\n"
"background-color: rgb(70, 70, 70);\n"
"border-radius:5px;\n"
"margin: 5px;\n"
"}\n"
"")
        # Frame Botones general ---------------------------------
        self.frame_botones.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_botones.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_botones.setObjectName("frame_botones")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_botones)
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        # Frame Botones general ---------------------------------

        # Button detectar --------------------------------
        self.button_detect = QtWidgets.QPushButton(self.frame_botones)
        self.button_detect.setMinimumSize(QtCore.QSize(0, 35))
        self.button_detect.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.button_detect.setIconSize(QtCore.QSize(35, 35))
        self.button_detect.setObjectName("button_detect")
        self.button_detect.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"\n"
"QPushButton{\n"
"font: 14pt \"Consolas\";\n"
"color:rgb(255, 255,255);\n"
"border:1px solid #93C6FF;\n"
"background-color: rgb(70, 70, 70);\n"
"border-radius:5px;\n"
"margin: 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(0, 0, 0);\n"
"border:1px solid #93C6FF;\n"
"}\n")
        self.verticalLayout_5.addWidget(self.button_detect)
        # Button detectar --------------------------------

        # Button confirm ---------------------------------
        self.button_conf = QtWidgets.QPushButton(self.frame_botones)
        self.button_conf.setMinimumSize(QtCore.QSize(0, 35))
        self.button_conf.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_conf.setIconSize(QtCore.QSize(35, 35))
        self.button_conf.setObjectName("button_conf")
        self.verticalLayout_5.addWidget(self.button_conf)
        # Button confirm ---------------------------------

        # Button send --------------------------------------------
        self.button_send = QtWidgets.QPushButton(self.frame_botones)
        self.button_send.setMinimumSize(QtCore.QSize(0,35))
        self.button_send.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.button_send.setIconSize(QtCore.QSize(30, 30))
        self.button_send.setObjectName("button_send")
        self.verticalLayout_5.addWidget(self.button_send)
        self.verticalLayout_4.addWidget(self.frame_botones)
        self.button_send.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"\n"
"QPushButton{\n"
"font: 14pt \"Consolas\";\n"
"color:rgb(255, 255,255);\n"
"border:1px solid #93C6FF;\n"
"background-color: rgb(70, 70, 70);\n"
"border-radius:5px;\n"
"margin: 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(0, 0, 0);\n"
"border:1px solid #93C6FF;\n"
"}\n")
        # Button send --------------------------------------------

        self.frame_2 = QtWidgets.QFrame(self.frame_datos)
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"QPushButton{\n"
"background-color: rgb(69, 74, 88);\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QLabel{\n"
"font: 12pt \"Consolas\";\n"
"color: rgb(255, 255,255);\n"
"}\n"
"\n"
"QLineEdit{\n"
"border:1px solid #93C6FF;\n"
"border-radius:5px;\n"
"background-color: rgb(70, 70, 70);\n"
"font: 12pt \"Consolas\";\n"
"color: rgb(255, 255,255);\n"
"}\n"
"\n"
"QTextBrowser{\n"
"border-radius:5px;\n"
"border:1px solid #93C6FF;\n"
"background-color: rgb(70, 70, 70);\n"
"font: 12pt \"Consolas\";\n"
"color: rgb(255, 255,255);\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_8.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_8.setSpacing(13)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        # Frame input numero paquete ----------------------------------
        self.frame_package_number = QtWidgets.QFrame(self.frame_2)
        self.frame_package_number.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_package_number.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_package_number.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_package_number.setObjectName("frame_package_number")
        self.label_package_number = QtWidgets.QLabel(self.frame_package_number)
        self.label_package_number.setGeometry(QtCore.QRect(5, -12, 171, 71))
        self.label_package_number.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_package_number.setObjectName("label_package_number")
        self.in_npackage = QtWidgets.QLineEdit(self.frame_package_number)
        self.in_npackage.setGeometry(QtCore.QRect(120, 7, 131, 33))
        self.in_npackage.setMinimumSize(QtCore.QSize(0, 33))
        self.in_npackage.setInputMask("")
        self.in_npackage.setObjectName("in_npackage")
        self.verticalLayout_8.addWidget(self.frame_package_number)
        # Frame input numero paquete ----------------------------------

        # Frame cantidad palos ------------------------------------
        self.frame_n_sticks = QtWidgets.QFrame(self.frame_2)
        self.frame_n_sticks.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_n_sticks.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_n_sticks.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_n_sticks.setObjectName("frame_n_sticks")
        self.label_n_sticks = QtWidgets.QLabel(self.frame_n_sticks)
        self.label_n_sticks.setGeometry(QtCore.QRect(5, -14, 231, 71))
        self.label_n_sticks.setMinimumSize(QtCore.QSize(0, 33))
        self.label_n_sticks.setObjectName("label_n_sticks")
        self.out_sticks = QtWidgets.QTextBrowser(self.frame_n_sticks)
        self.out_sticks.setGeometry(QtCore.QRect(120, 5, 131, 33))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.out_sticks.sizePolicy().hasHeightForWidth())
        self.out_sticks.setSizePolicy(sizePolicy)
        self.out_sticks.setMinimumSize(QtCore.QSize(0, 33))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.out_sticks.setFont(font)
        self.out_sticks.setObjectName("out_sticks")
        # Frame cantidad palos ------------------------------------

        # Frame diametro promedio --------------------------------
        self.verticalLayout_8.addWidget(self.frame_n_sticks)
        self.frame_avg_diameter = QtWidgets.QFrame(self.frame_2)
        self.frame_avg_diameter.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_avg_diameter.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_avg_diameter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_avg_diameter.setObjectName("frame_avg_diameter")
        self.label_avg_diameter = QtWidgets.QLabel(self.frame_avg_diameter)
        self.label_avg_diameter.setGeometry(QtCore.QRect(5, -14, 221, 71))
        self.label_avg_diameter.setMinimumSize(QtCore.QSize(0, 33))
        self.label_avg_diameter.setObjectName("label_avg_diameter")
        self.out_diameter = QtWidgets.QTextBrowser(self.frame_avg_diameter)
        self.out_diameter.setGeometry(QtCore.QRect(120, 5, 131, 33))
        self.out_diameter.setMinimumSize(QtCore.QSize(0, 33))
        self.out_diameter.setObjectName("out_diameter")
        self.verticalLayout_8.addWidget(self.frame_avg_diameter)
        # Frame diametro promedio --------------------------------

        # Frame botones de mas ---------------------------------------
        self.frame_14 = QtWidgets.QFrame(self.frame_2)
        self.frame_14.setMinimumSize(QtCore.QSize(0, 44))
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.button_plas = QtWidgets.QPushButton(self.frame_14)
        self.button_plas.setGeometry(QtCore.QRect(170, 0, 43, 43))
        self.button_plas.setStyleSheet("")
        self.button_plas.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/gui/mas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_plas.setIcon(icon3)
        self.button_plas.setIconSize(QtCore.QSize(53, 53))
        self.button_plas.setObjectName("button_plas")
        self.verticalLayout_8.addWidget(self.frame_14)
        # Frame botones de mas ---------------------------------------

        # Frame Corrección -------------------------------------
        self.frame_15 = QtWidgets.QFrame(self.frame_2)
        self.frame_15.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.label_12 = QtWidgets.QLabel(self.frame_15)
        self.label_12.setGeometry(QtCore.QRect(5, -12, 191, 71))
        self.label_12.setObjectName("label_12")
        self.out_correction = QtWidgets.QTextBrowser(self.frame_15)
        self.out_correction.setGeometry(QtCore.QRect(120, 5, 131, 33))
        self.out_correction.setMinimumSize(QtCore.QSize(0, 33))
        self.out_correction.setObjectName("out_correction")
        self.verticalLayout_8.addWidget(self.frame_15)
        # Frame Corrección -------------------------------------

        # Frame botones de menos ---------------------------------------
        self.frame_16 = QtWidgets.QFrame(self.frame_2)
        self.frame_16.setMinimumSize(QtCore.QSize(0, 44))
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.button_less = QtWidgets.QPushButton(self.frame_16)
        self.button_less.setGeometry(QtCore.QRect(170, 0, 43, 43))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_less.sizePolicy().hasHeightForWidth())
        self.button_less.setSizePolicy(sizePolicy)
        self.button_less.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_less.setStyleSheet("")
        self.button_less.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/gui/menos.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_less.setIcon(icon4)
        self.button_less.setIconSize(QtCore.QSize(53, 53))
        self.button_less.setObjectName("button_less")
        self.verticalLayout_8.addWidget(self.frame_16)
        # Frame botones de + y - ---------------------------------------

        # Palos totales frame ----------------------------------
        self.frame_17 = QtWidgets.QFrame(self.frame_2)
        self.frame_17.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.label_11 = QtWidgets.QLabel(self.frame_17)
        self.label_11.setGeometry(QtCore.QRect(5, -12, 181, 71))
        self.label_11.setObjectName("label_11")
        self.out_total = QtWidgets.QTextBrowser(self.frame_17)
        self.out_total.setGeometry(QtCore.QRect(120, 7, 131, 33))
        self.out_total.setMinimumSize(QtCore.QSize(0, 33))
        self.out_total.setObjectName("out_total")
        self.verticalLayout_8.addWidget(self.frame_17)
        # Palos totales frame ----------------------------------

        # Distance measure frame -------------------------
        self.frame_distance_measure = QtWidgets.QFrame(self.frame_2)
        self.frame_distance_measure.setMinimumSize(QtCore.QSize(0, 25))
        self.frame_distance_measure.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_distance_measure.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_distance_measure.setObjectName("frame_distance_measure")
        self.label_distance_measure = QtWidgets.QLabel(self.frame_distance_measure)
        self.label_distance_measure.setGeometry(QtCore.QRect(5, -10, 181, 65))
        self.label_distance_measure.setObjectName("label_distance_measure")
        self.out_distance_measure = QtWidgets.QTextBrowser(self.frame_distance_measure)
        self.out_distance_measure.setGeometry(QtCore.QRect(120, 5, 131, 30))
        self.out_distance_measure.setMinimumSize(QtCore.QSize(0, 25))
        self.out_distance_measure.setObjectName("out_distance_measure")
        self.verticalLayout_8.addWidget(self.frame_distance_measure)
        # Distance measure frame -------------------------------------

        self.verticalLayout_4.addWidget(self.frame_2)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 7)
        self.horizontalLayout_2.addWidget(self.frame_datos)
        self.frame_imagen = QtWidgets.QFrame(self.frame_inferior)
        self.frame_imagen.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_imagen.setMaximumSize(QtCore.QSize(100000, 16777215))
        self.frame_imagen.setStyleSheet("QFrame{\n"
"background-color: rgb(69, 74, 88);\n"
"}\n"
"")
        self.frame_imagen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_imagen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_imagen.setObjectName("frame_imagen")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_imagen)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_imagen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(682, 455))
        self.tabWidget.setMaximumSize(QtCore.QSize(710, 513))
        self.tabWidget.setStyleSheet(" QTabBar::tab {\n"
"font: 13pt \"Consolas\";\n"
"color:rgb(255, 255,255);\n"
"border:2px solid #93C6FF;\n"
"background-color: rgb(70, 70, 70);\n"
"                min-width:130px; /* Cambia el ancho mínimo de los botones */\n"
"                padding: 5px; /* Cambia el espacio interno de los botones */         \n"
"\n"
"            }\n"
"\n"
"QTabBar::tab:selected {\n"
"font: 13pt \"Consolas\";\n"
"color:rgb(255, 255,255);\n"
"background-color: rgb(0, 0, 0);    \n"
"            }\n"
"QTabWidget::pane {\n"
" border:3px solid #93C6FF;    \n"
"background-color: rgb(70, 70, 70);    \n"
"            }")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        '''self.out_cam = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.out_cam.sizePolicy().hasHeightForWidth())
        self.out_cam.setSizePolicy(sizePolicy)
        self.out_cam.setMinimumSize(QtCore.QSize(682, 455))
        self.out_cam.setMaximumSize(QtCore.QSize(682, 455))
        self.out_cam.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.out_cam.setText("")
        self.out_cam.setScaledContents(False)
        self.out_cam.setAlignment(QtCore.Qt.AlignCenter)
        self.out_cam.setObjectName("out_cam")
        self.horizontalLayout_4.addWidget(self.out_cam)

        self.tabWidget.addTab(self.tab_3, "")'''

        if config_data["environment"] == "prod":

                self.picam = Picamera2()
                size = (config_data["camera"]["res_x"], config_data["camera"]["res_y"])

                picam_error_counter = 0

                while picam_error_counter < RETRY_PICAM_ERROR:
                        try:
                                config = self.picam.create_preview_configuration(main={"size": size},
                                                                        lores={"size": (640, 480)},
                                                                        display="lores")
                                self.picam.configure(config)
                                break
                        
                        except Exception as e:
                                picam_error_counter += 1
                                logger.error(f"Error: {e}")
                        

                self.qpicamera2 = QGlPicamera2(picam2=self.picam,
                                               parent=self.tab_3,
                                               width=800, height=600,
                                               bg_colour=(255,255,255), 
                                               keep_ar=True)
                
                self.qpicamera2.done_signal.connect(self.capture_done)

                self.horizontalLayout_4.addWidget(self.qpicamera2)
                self.tabWidget.addTab(self.tab_3, "")
        
        else:
                self.out_cam = QtWidgets.QLabel(self.tab_3)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.out_cam.sizePolicy().hasHeightForWidth())
                self.out_cam.setSizePolicy(sizePolicy)
                self.out_cam.setMinimumSize(QtCore.QSize(682, 455))
                self.out_cam.setMaximumSize(QtCore.QSize(682, 455))
                self.out_cam.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.out_cam.setText("")
                self.out_cam.setScaledContents(False)
                self.out_cam.setAlignment(QtCore.Qt.AlignCenter)
                self.out_cam.setObjectName("out_cam")
                self.horizontalLayout_4.addWidget(self.out_cam)
                self.tabWidget.addTab(self.tab_3, "")
             

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.out_img = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.out_img.sizePolicy().hasHeightForWidth())
        self.out_img.setSizePolicy(sizePolicy)
        self.out_img.setMinimumSize(QtCore.QSize(682, 455))
        self.out_img.setMaximumSize(QtCore.QSize(682, 455))
        self.out_img.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.out_img.setText("")
        self.out_img.setAlignment(QtCore.Qt.AlignCenter)
        self.out_img.setObjectName("out_img")
        self.verticalLayout_3.addWidget(self.out_img)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.out_detect = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.out_detect.sizePolicy().hasHeightForWidth())
        self.out_detect.setSizePolicy(sizePolicy)
        self.out_detect.setMinimumSize(QtCore.QSize(682, 455))
        self.out_detect.setMaximumSize(QtCore.QSize(682, 455))
        self.out_detect.setText("")
        self.out_detect.setAlignment(QtCore.Qt.AlignCenter)
        self.out_detect.setObjectName("out_detect")
        self.verticalLayout_7.addWidget(self.out_detect)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout_2.addWidget(self.frame_imagen)
        self.verticalLayout_2.addWidget(self.frame_inferior)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def capture_done(self, job):
        self.picam.wait(job)
        print("Photo job image done !")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Detección de Palos "))
        self.button_detect.setText(_translate("MainWindow", "Detectar  "))
        self.button_conf.setText(_translate("MainWindow", "Confirmar "))
        self.button_send.setText(_translate("MainWindow", "Enviar    "))
        self.label_package_number.setText(_translate("MainWindow", "<html><head/><body><p>N° de <br/>Paquete</p></body></html>"))
        self.in_npackage.setPlaceholderText(_translate("MainWindow", "Ingrese N°"))
        self.label_n_sticks.setText(_translate("MainWindow", "<html><head/><body><p>Palos <br/>Detectados</p></body></html>"))
        self.label_avg_diameter.setText(_translate("MainWindow", "<html><head/><body><p>Diametro <br/>Promedio</p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p>Correción <br/>Detección</p></body></html>"))
        self.label_distance_measure.setText(_translate("MainWindow", "<html><head/><body><p>Distancia </p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "Palos<br> Totales"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Camara"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Fotografia"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Detección"))

    def style_confirm_button(self, conf: bool):

        if not conf:
                self.button_conf.setStyleSheet("QPushButton{\n"
                "font: 14pt \"Consolas\";\n"
                "color:rgb(255, 255,255);\n"
                "border:1px solid #93C6FF;\n"
                "background-color: rgb(0, 0, 0);\n"
                "border-radius:5px;\n"
                "\n"
                "}\n"
                "")
        else: 
                self.button_conf.setStyleSheet("QPushButton{\n"
                "font: 14pt \"Consolas\";\n"
                "color:rgb(255, 255,255);\n"
                "border:1px solid #93C6FF;\n"
                "background-color: rgb(70, 70, 70);\n"
                "border-radius:5px;\n"
                "\n"
                "}\n"
                "")
    
    def style_button_pressed(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
