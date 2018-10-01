# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
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
        self.setBluePushButton = QtWidgets.QPushButton(Dialog)
        self.setBluePushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.setBluePushButton.setObjectName("setBluePushButton")
        self.gridLayout.addWidget(self.setBluePushButton, 1, 1, 1, 1)
        self.setGreenPushButton = QtWidgets.QPushButton(Dialog)
        self.setGreenPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.setGreenPushButton.setObjectName("setGreenPushButton")
        self.gridLayout.addWidget(self.setGreenPushButton, 3, 1, 1, 1)
        self.instructionPushButton = QtWidgets.QPushButton(Dialog)
        self.instructionPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.instructionPushButton.setObjectName("instructionPushButton")
        self.gridLayout.addWidget(self.instructionPushButton, 0, 1, 1, 1)
        self.setRedPushButton = QtWidgets.QPushButton(Dialog)
        self.setRedPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.setRedPushButton.setObjectName("setRedPushButton")
        self.gridLayout.addWidget(self.setRedPushButton, 4, 1, 1, 1)
        self.okPushButton = QtWidgets.QPushButton(Dialog)
        self.okPushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.okPushButton.setObjectName("okPushButton")
        self.gridLayout.addWidget(self.okPushButton, 6, 1, 1, 1)
        self.setYellowPushButton = QtWidgets.QPushButton(Dialog)
        self.setYellowPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.setYellowPushButton.setObjectName("setYellowPushButton")
        self.gridLayout.addWidget(self.setYellowPushButton, 2, 1, 1, 1)
        self.openCVLabel = QtWidgets.QLabel(Dialog)
        self.openCVLabel.setMinimumSize(QtCore.QSize(640, 480))
        self.openCVLabel.setText("")
        self.openCVLabel.setObjectName("openCVLabel")
        self.gridLayout.addWidget(self.openCVLabel, 0, 0, 7, 1)
        self.skipCalibrationPushButton = QtWidgets.QPushButton(Dialog)
        self.skipCalibrationPushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.skipCalibrationPushButton.setObjectName("skipCalibrationPushButton")
        self.gridLayout.addWidget(self.skipCalibrationPushButton, 5, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.commandsListWidget = QtWidgets.QListWidget(Dialog)
        self.commandsListWidget.setMinimumSize(QtCore.QSize(850, 150))
        self.commandsListWidget.setObjectName("commandsListWidget")
        self.gridLayout_2.addWidget(self.commandsListWidget, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Konfiguracja"))
        self.setBluePushButton.setText(_translate("Dialog", "Niebieski"))
        self.setGreenPushButton.setText(_translate("Dialog", "Zielony"))
        self.instructionPushButton.setText(_translate("Dialog", "Instrukcja"))
        self.setRedPushButton.setText(_translate("Dialog", "Czerwony"))
        self.okPushButton.setText(_translate("Dialog", "Ok"))
        self.setYellowPushButton.setText(_translate("Dialog", "Żółty"))
        self.skipCalibrationPushButton.setText(_translate("Dialog", "Pomiń kalibracje"))

