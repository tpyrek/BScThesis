# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(868, 656)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.set_blue_push_button = QtWidgets.QPushButton(Dialog)
        self.set_blue_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.set_blue_push_button.setObjectName("set_blue_push_button")
        self.gridLayout.addWidget(self.set_blue_push_button, 1, 1, 1, 1)
        self.set_green_push_button = QtWidgets.QPushButton(Dialog)
        self.set_green_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.set_green_push_button.setObjectName("set_green_push_button")
        self.gridLayout.addWidget(self.set_green_push_button, 3, 1, 1, 1)
        self.instruction_push_button = QtWidgets.QPushButton(Dialog)
        self.instruction_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.instruction_push_button.setObjectName("instruction_push_button")
        self.gridLayout.addWidget(self.instruction_push_button, 0, 1, 1, 1)
        self.set_red_push_button = QtWidgets.QPushButton(Dialog)
        self.set_red_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.set_red_push_button.setObjectName("set_red_push_button")
        self.gridLayout.addWidget(self.set_red_push_button, 4, 1, 1, 1)
        self.ok_push_button = QtWidgets.QPushButton(Dialog)
        self.ok_push_button.setMinimumSize(QtCore.QSize(0, 50))
        self.ok_push_button.setObjectName("ok_push_button")
        self.gridLayout.addWidget(self.ok_push_button, 6, 1, 1, 1)
        self.set_yellow_push_button = QtWidgets.QPushButton(Dialog)
        self.set_yellow_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.set_yellow_push_button.setObjectName("set_yellow_push_button")
        self.gridLayout.addWidget(self.set_yellow_push_button, 2, 1, 1, 1)
        self.open_cv_label = QtWidgets.QLabel(Dialog)
        self.open_cv_label.setMinimumSize(QtCore.QSize(640, 480))
        self.open_cv_label.setText("")
        self.open_cv_label.setObjectName("open_cv_label")
        self.gridLayout.addWidget(self.open_cv_label, 0, 0, 7, 1)
        self.skip_calibration_push_button = QtWidgets.QPushButton(Dialog)
        self.skip_calibration_push_button.setMinimumSize(QtCore.QSize(0, 40))
        self.skip_calibration_push_button.setObjectName("skip_calibration_push_button")
        self.gridLayout.addWidget(self.skip_calibration_push_button, 5, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.commands_list_widget = QtWidgets.QListWidget(Dialog)
        self.commands_list_widget.setMinimumSize(QtCore.QSize(850, 150))
        self.commands_list_widget.setObjectName("commands_list_widget")
        self.gridLayout_2.addWidget(self.commands_list_widget, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Konfiguracja"))
        self.set_blue_push_button.setText(_translate("Dialog", "Niebieski"))
        self.set_green_push_button.setText(_translate("Dialog", "Zielony"))
        self.instruction_push_button.setText(_translate("Dialog", "Instrukcja"))
        self.set_red_push_button.setText(_translate("Dialog", "Czerwony"))
        self.ok_push_button.setText(_translate("Dialog", "Ok"))
        self.set_yellow_push_button.setText(_translate("Dialog", "Żółty"))
        self.skip_calibration_push_button.setText(_translate("Dialog", "Pomiń kalibracje"))

