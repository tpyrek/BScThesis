# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autocontrol.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1272, 692)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.executeCommandPushButton = QtWidgets.QPushButton(Dialog)
        self.executeCommandPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.executeCommandPushButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.executeCommandPushButton.setObjectName("executeCommandPushButton")
        self.gridLayout.addWidget(self.executeCommandPushButton, 3, 1, 1, 2)
        self.foundFiguresGroupBox = QtWidgets.QGroupBox(Dialog)
        self.foundFiguresGroupBox.setMinimumSize(QtCore.QSize(300, 0))
        self.foundFiguresGroupBox.setObjectName("foundFiguresGroupBox")
        self.foundFiguresListWidget = QtWidgets.QListWidget(self.foundFiguresGroupBox)
        self.foundFiguresListWidget.setGeometry(QtCore.QRect(5, 31, 291, 371))
        self.foundFiguresListWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.foundFiguresListWidget.setObjectName("foundFiguresListWidget")
        self.gridLayout.addWidget(self.foundFiguresGroupBox, 0, 1, 2, 1)
        self.returnPushButton = QtWidgets.QPushButton(Dialog)
        self.returnPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.returnPushButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.returnPushButton.setObjectName("returnPushButton")
        self.gridLayout.addWidget(self.returnPushButton, 4, 0, 1, 3)
        self.openCVLabel = QtWidgets.QLabel(Dialog)
        self.openCVLabel.setMinimumSize(QtCore.QSize(640, 480))
        self.openCVLabel.setText("")
        self.openCVLabel.setObjectName("openCVLabel")
        self.gridLayout.addWidget(self.openCVLabel, 0, 0, 4, 1)
        self.highlightFiguresCheckBox = QtWidgets.QCheckBox(Dialog)
        self.highlightFiguresCheckBox.setObjectName("highlightFiguresCheckBox")
        self.gridLayout.addWidget(self.highlightFiguresCheckBox, 2, 1, 1, 1)
        self.permittedOperationsGroupBox = QtWidgets.QGroupBox(Dialog)
        self.permittedOperationsGroupBox.setMinimumSize(QtCore.QSize(300, 0))
        self.permittedOperationsGroupBox.setObjectName("permittedOperationsGroupBox")
        self.permittedOperationsListWidget = QtWidgets.QListWidget(self.permittedOperationsGroupBox)
        self.permittedOperationsListWidget.setGeometry(QtCore.QRect(5, 31, 291, 401))
        self.permittedOperationsListWidget.setObjectName("permittedOperationsListWidget")
        self.gridLayout.addWidget(self.permittedOperationsGroupBox, 0, 2, 3, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.commandsListWidget = QtWidgets.QListWidget(Dialog)
        self.commandsListWidget.setMinimumSize(QtCore.QSize(0, 150))
        self.commandsListWidget.setMaximumSize(QtCore.QSize(16777215, 150))
        self.commandsListWidget.setObjectName("commandsListWidget")
        self.gridLayout_2.addWidget(self.commandsListWidget, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kontrola automatyczna"))
        self.executeCommandPushButton.setText(_translate("Dialog", "Wykonaj"))
        self.foundFiguresGroupBox.setTitle(_translate("Dialog", "Lista  znalezionych figur"))
        self.returnPushButton.setText(_translate("Dialog", "Powrót"))
        self.highlightFiguresCheckBox.setText(_translate("Dialog", "Zanznacz figure na obrazie"))
        self.permittedOperationsGroupBox.setTitle(_translate("Dialog", "Lista możliwych operacji"))

