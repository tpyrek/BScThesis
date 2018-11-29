# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 250)
        Dialog.setMinimumSize(QtCore.QSize(250, 250))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.choose_mode_label = QtWidgets.QLabel(Dialog)
        self.choose_mode_label.setMinimumSize(QtCore.QSize(100, 50))
        self.choose_mode_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.choose_mode_label.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_mode_label.setObjectName("choose_mode_label")
        self.verticalLayout.addWidget(self.choose_mode_label)
        self.manual_control_push_button = QtWidgets.QPushButton(Dialog)
        self.manual_control_push_button.setMinimumSize(QtCore.QSize(200, 30))
        self.manual_control_push_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.manual_control_push_button.setObjectName("manual_control_push_button")
        self.verticalLayout.addWidget(self.manual_control_push_button, 0, QtCore.Qt.AlignHCenter)
        self.auto_control_push_button = QtWidgets.QPushButton(Dialog)
        self.auto_control_push_button.setMinimumSize(QtCore.QSize(200, 30))
        self.auto_control_push_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.auto_control_push_button.setObjectName("auto_control_push_button")
        self.verticalLayout.addWidget(self.auto_control_push_button, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Wybór trybu"))
        self.choose_mode_label.setText(_translate("Dialog", "Wybierz tryb"))
        self.manual_control_push_button.setText(_translate("Dialog", "Kontrola manualna"))
        self.auto_control_push_button.setText(_translate("Dialog", "Kontrola automatyczna"))

