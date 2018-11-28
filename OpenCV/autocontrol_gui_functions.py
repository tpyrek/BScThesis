from PyQt5 import QtWidgets, QtGui
from autocontrol_gui import Ui_Dialog
import open_CV_worker_autocontrol_gui
import sendDataToServosControllerAutoControlGUI
import threading

from fields_coordinates import field_coordinates_table


class AutoControlGUI(QtWidgets.QDialog):

    def __init__(self, controlgui, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.controlgui = controlgui
        self.sendDataToServosController = \
            sendDataToServosControllerAutoControlGUI.sendDataToServosControllerAutoControlGUI()

        self.openCVWorker = open_CV_worker_autocontrol_gui.openCVWorker(self.sendDataToServosController)

        self.ui.permittedOperationsListWidget.addItem("Przenieś")

        # Połączenie sygnałów ze slotami
        self.ui.returnPushButton.clicked.connect(self.returnToControlGui)
        self.ui.executeCommandPushButton.clicked.connect(self.executeCommand)
        self.ui.highlightFiguresCheckBox.stateChanged.connect(self.openCVWorker.receiveHighLightEnable)
        self.ui.foundFiguresListWidget.currentRowChanged.connect(self.openCVWorker.receiveSelectedFigureNumber)

        self.openCVWorker.sendFrame.connect(self.receiveFrame)
        self.openCVWorker.sendFigureText.connect(self.receiveFigureText)
        self.openCVWorker.sendFigureData.connect(self.receiveFigureData)
        self.openCVWorker.sendFigureDataTextClear.connect(self.clearFiguresListAndInfo)

        self.sendDataToServosController.sendStatus.connect(self.enableAllWidgets)
        self.sendDataToServosController.sendCommandsText.connect(self.receiveCommandsText)

    def startOpenCVWorker(self):
        self.openCVWorker.runThread = True
        self.openCVWorker.receiveSetup(0)
        self.openCVWorkerThread = threading.Thread(target=self.openCVWorker.receiveGrabFrame)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        self.openCVWorkerThread.daemon = True
        self.openCVWorkerThread.start()

    # Slot do ustawiania otrzymanych od openCVWorker klatek
    def receiveFrame(self, qImage):
        self.ui.openCVLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))

    def receiveFigureText(self, text):
        self.ui.foundFiguresListWidget.addItem(text)

    def receiveFigureData(self, data):
        self.ui.figureDataTextEdit.setText(data)

    def receiveCommandsText(self, text):
        self.ui.commandsListWidget.addItem(text)

    def returnToControlGui(self):
        self.clearFiguresListAndInfo()
        self.openCVWorker.runThread = False
        self.openCVWorkerThread.join()
        del self.openCVWorkerThread
        self.controlgui.show()
        self.close()

    def executeCommand(self):

        # Sprawdzenie, czy są jakiekolwiek figury i dozwolone operacje
        if self.ui.foundFiguresListWidget.count() != 0 and self.ui.permittedOperationsListWidget.count() != 0:
            # Sprawdzenie, czy jest zaznaczona któraś figura i któraś z możliwych operacji
            if (self.ui.foundFiguresListWidget.currentRow() != -1 and
                    self.ui.permittedOperationsListWidget.currentRow() != -1):

                self.disableAllWidgets()

                figure_number = self.ui.foundFiguresListWidget.currentRow()
                figure_field = self.openCVWorker.getFigureField(figure_number)

                dataTab = []
                dataTab.append(0)  # Max value
                dataTab.append(1000)  # Min value
                dataTab.append(60)  # Speed

                for value in field_coordinates_table[figure_field]:
                    dataTab.append(value)

                dataTab.append(1)
                dataTab.append(2)
                dataTab.append(3)
                dataTab.append(4)
                dataTab.append(5)
                dataTab.append(6)

                thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                          args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                                dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                                dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                                dataTab[14]))
                thread.start()


    def enableAllWidgets(self):
        self.ui.executeCommandPushButton.setEnabled(True)
        self.ui.returnPushButton.setEnabled(True)

    def disableAllWidgets(self):
        self.ui.executeCommandPushButton.setEnabled(False)
        self.ui.returnPushButton.setEnabled(False)

    def clearFiguresListAndInfo(self):
        self.ui.foundFiguresListWidget.clear()
        self.ui.figureDataTextEdit.setText("Numer : \nKolor : \nŚrodek : \nKąt : ")
