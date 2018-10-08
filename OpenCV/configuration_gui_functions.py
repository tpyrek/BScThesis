from PyQt5 import QtWidgets, QtCore, QtGui
from configuration_gui import Ui_Dialog
from instruction_gui_functions import InstructionGUI
from control_gui_functions import ControlGUI
import open_CV_worker_configuration_gui
import threading

class ConfigurationGUI(QtWidgets.QDialog):

    sendSignalToSetColor = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.instructiongui = InstructionGUI()
        self.controlgui = ControlGUI()

        self.openCVWorker = open_CV_worker_configuration_gui.openCVWorker()
        self.openCVWorkerThread = threading.Thread(target=self.openCVWorker.receiveGrabFrame)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        self.openCVWorkerThread.daemon = True


        self.disableConfigurationButtons()
        self.ui.okPushButton.setDisabled(True)
        # Licznik enableOkButton - Zostaje zwiekszony przy pobraniu każdego koloru i kiedy wszystkie kolory zostaną pobrane,
        # zostaje odblokowany przycisk okPushButton
        self.enableOkButton = 0
        self.firstFrame = True

        self.ui.commandsListWidget.addItem("Kalibracja kolorów")
        self.ui.skipCalibrationPushButton.setStyleSheet("background-color: red")

        # Połączenie sygnałów ze slotami
        self.ui.instructionPushButton.clicked.connect(self.openInstructionWindow)
        self.ui.setBluePushButton.clicked.connect(self.setBlueColor)
        self.ui.setYellowPushButton.clicked.connect(self.setYellowColor)
        self.ui.setGreenPushButton.clicked.connect(self.setGreenColor)
        self.ui.setRedPushButton.clicked.connect(self.setRedColor)
        self.ui.okPushButton.clicked.connect(self.openControlWindow)
        self.ui.skipCalibrationPushButton.clicked.connect(self.skipCalibration)
        self.openCVWorker.sendFrame.connect(self.receiveFrame)
        self.sendSignalToSetColor.connect(self.openCVWorker.getColorFromFrame)
        self.openCVWorker.sendText.connect(self.receiveText)

        self.openCVWorker.receiveSetup(1)
        self.openCVWorkerThread.start()

    # SLOTY

    # Ustawienie otrzymanego od openCVWorker tekstu
    def receiveText(self, text):
        self.ui.commandsListWidget.addItem(text)

    # Wyświetlenie otrzymanego od openCVWorker obrazka
    def receiveFrame(self, qImage):
        if self.firstFrame:
            self.enableConfigurationButtons()
            self.firstFrame = False
        self.ui.openCVLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))

    # Otwarcie okna instrukcji po naciśnięciu przycisku
    def openInstructionWindow(self):
        self.instructiongui.show()


    def setBlueColor(self):
        self.ui.setBluePushButton.setDisabled(True)
        self.ui.skipCalibrationPushButton.setDisabled(True)
        self.enableOkButton = self.enableOkButton + 1
        if self.enableOkButton == 4:
            self.ui.okPushButton.setEnabled(True)
        self.sendSignalToSetColor.emit("Blue")


    def setYellowColor(self):
        self.ui.setYellowPushButton.setDisabled(True)
        self.ui.skipCalibrationPushButton.setDisabled(True)
        self.enableOkButton = self.enableOkButton + 1
        if self.enableOkButton == 4:
            self.ui.okPushButton.setEnabled(True)
        self.sendSignalToSetColor.emit("Yellow")


    def setGreenColor(self):
        self.ui.setGreenPushButton.setDisabled(True)
        self.ui.skipCalibrationPushButton.setDisabled(True)
        self.enableOkButton = self.enableOkButton + 1
        if self.enableOkButton == 4:
            self.ui.okPushButton.setEnabled(True)
        self.sendSignalToSetColor.emit("Green")


    def setRedColor(self):
        self.ui.setRedPushButton.setDisabled(True)
        self.ui.skipCalibrationPushButton.setDisabled(True)
        self.enableOkButton = self.enableOkButton + 1
        if self.enableOkButton == 4:
            self.ui.okPushButton.setEnabled(True)
        self.sendSignalToSetColor.emit("Red")

    def openControlWindow(self):
        self.openCVWorker.runThread = False
        self.openCVWorkerThread.join()
        del self.openCVWorkerThread
        self.close()
        self.controlgui.show()
        self.controlgui.openSerialPort()

    def skipCalibration(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        messageBox.setWindowTitle("Uwaga !")
        messageBox.setText("Jeśli pominiesz ten krok, aplikacja może nie działać poprawnie!")
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        messageBoxButtonYes = messageBox.button(QtWidgets.QMessageBox.Yes)
        messageBoxButtonYes.setText("Ok, pomiń")
        messageBoxButtonNo = messageBox.button(QtWidgets.QMessageBox.No)
        messageBoxButtonNo.setText("Wróć")
        messageBox.exec()

        if messageBox.clickedButton() == messageBoxButtonYes:
            self.openCVWorker.runThread = False
            self.openCVWorkerThread.join()
            del self.openCVWorkerThread
            self.close()
            self.controlgui.show()
            self.controlgui.openSerialPort()

        elif messageBox.clickedButton() == messageBoxButtonNo:
            return


    # FUNKCJE
    def disableConfigurationButtons(self):
        self.ui.setBluePushButton.setDisabled(True)
        self.ui.setYellowPushButton.setDisabled(True)
        self.ui.setGreenPushButton.setDisabled(True)
        self.ui.setRedPushButton.setDisabled(True)

    def enableConfigurationButtons(self):
        self.ui.setBluePushButton.setEnabled(True)
        self.ui.setYellowPushButton.setEnabled(True)
        self.ui.setGreenPushButton.setEnabled(True)
        self.ui.setRedPushButton.setEnabled(True)
