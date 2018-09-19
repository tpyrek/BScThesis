# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
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
        self.chooseModeLabel = QtWidgets.QLabel(Dialog)
        self.chooseModeLabel.setMinimumSize(QtCore.QSize(100, 50))
        self.chooseModeLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.chooseModeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chooseModeLabel.setObjectName("chooseModeLabel")
        self.verticalLayout.addWidget(self.chooseModeLabel)
        self.manualControlPushButton = QtWidgets.QPushButton(Dialog)
        self.manualControlPushButton.setMinimumSize(QtCore.QSize(200, 30))
        self.manualControlPushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.manualControlPushButton.setObjectName("manualControlPushButton")
        self.verticalLayout.addWidget(self.manualControlPushButton, 0, QtCore.Qt.AlignHCenter)
        self.autoControlPushButton = QtWidgets.QPushButton(Dialog)
        self.autoControlPushButton.setMinimumSize(QtCore.QSize(200, 30))
        self.autoControlPushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.autoControlPushButton.setObjectName("autoControlPushButton")
        self.verticalLayout.addWidget(self.autoControlPushButton, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Wybór trybu"))
        self.chooseModeLabel.setText(_translate("Dialog", "Wybierz tryb"))
        self.manualControlPushButton.setText(_translate("Dialog", "Kontrola manualna"))
        self.autoControlPushButton.setText(_translate("Dialog", "Kontrola automatyczna"))

