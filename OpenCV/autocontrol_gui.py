# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autocontrol.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
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
        self.execute_command_push_button = QtWidgets.QPushButton(Dialog)
        self.execute_command_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.execute_command_push_button.setMaximumSize(QtCore.QSize(16777215, 30))
        self.execute_command_push_button.setObjectName("execute_command_push_button")
        self.gridLayout.addWidget(self.execute_command_push_button, 3, 1, 1, 2)
        self.return_push_button = QtWidgets.QPushButton(Dialog)
        self.return_push_button.setMinimumSize(QtCore.QSize(0, 30))
        self.return_push_button.setMaximumSize(QtCore.QSize(16777215, 30))
        self.return_push_button.setObjectName("return_push_button")
        self.gridLayout.addWidget(self.return_push_button, 4, 0, 1, 3)
        self.open_cv_label = QtWidgets.QLabel(Dialog)
        self.open_cv_label.setMinimumSize(QtCore.QSize(640, 480))
        self.open_cv_label.setText("")
        self.open_cv_label.setObjectName("open_cv_label")
        self.gridLayout.addWidget(self.open_cv_label, 0, 0, 4, 1)
        self.highlight_figures_check_box = QtWidgets.QCheckBox(Dialog)
        self.highlight_figures_check_box.setObjectName("highlight_figures_check_box")
        self.gridLayout.addWidget(self.highlight_figures_check_box, 2, 1, 1, 1)
        self.permitted_operations_group_box = QtWidgets.QGroupBox(Dialog)
        self.permitted_operations_group_box.setMinimumSize(QtCore.QSize(300, 0))
        self.permitted_operations_group_box.setObjectName("permitted_operations_group_box")
        self.permitted_operations_list_widget = QtWidgets.QListWidget(self.permitted_operations_group_box)
        self.permitted_operations_list_widget.setGeometry(QtCore.QRect(5, 31, 291, 401))
        self.permitted_operations_list_widget.setObjectName("permitted_operations_list_widget")
        self.gridLayout.addWidget(self.permitted_operations_group_box, 0, 2, 3, 1)
        self.found_figures_group_box = QtWidgets.QGroupBox(Dialog)
        self.found_figures_group_box.setMinimumSize(QtCore.QSize(300, 290))
        self.found_figures_group_box.setObjectName("found_figures_group_box")
        self.found_figures_list_widget = QtWidgets.QListWidget(self.found_figures_group_box)
        self.found_figures_list_widget.setGeometry(QtCore.QRect(5, 31, 291, 251))
        self.found_figures_list_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.found_figures_list_widget.setObjectName("found_figures_list_widget")
        self.gridLayout.addWidget(self.found_figures_group_box, 0, 1, 1, 1)
        self.figure_data_group_box = QtWidgets.QGroupBox(Dialog)
        self.figure_data_group_box.setObjectName("figure_data_group_box")
        self.figure_data_text_edit = QtWidgets.QTextEdit(self.figure_data_group_box)
        self.figure_data_text_edit.setGeometry(QtCore.QRect(10, 30, 281, 81))
        self.figure_data_text_edit.setObjectName("figure_data_text_edit")
        self.gridLayout.addWidget(self.figure_data_group_box, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.commands_list_widget = QtWidgets.QListWidget(Dialog)
        self.commands_list_widget.setMinimumSize(QtCore.QSize(0, 150))
        self.commands_list_widget.setMaximumSize(QtCore.QSize(16777215, 150))
        self.commands_list_widget.setObjectName("commands_list_widget")
        self.gridLayout_2.addWidget(self.commands_list_widget, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kontrola automatyczna"))
        self.execute_command_push_button.setText(_translate("Dialog", "Wykonaj"))
        self.return_push_button.setText(_translate("Dialog", "Powrót"))
        self.highlight_figures_check_box.setText(_translate("Dialog", "Zanznacz figure na obrazie"))
        self.permitted_operations_group_box.setTitle(_translate("Dialog", "Lista możliwych operacji"))
        self.found_figures_group_box.setTitle(_translate("Dialog", "Lista  znalezionych figur"))
        self.figure_data_group_box.setTitle(_translate("Dialog", "Dane figury"))
        self.figure_data_text_edit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Numer : </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Kolor :    </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Środek : </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Kąt : </p></body></html>"))

