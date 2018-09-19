from PyQt5 import QtWidgets, QtGui
from autocontrol_gui import Ui_Dialog
import open_CV_worker_autocontrol_gui
import threading


class AutocontrolGUI(QtWidgets.QDialog):

    def __init__(self, controlgui, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.controlgui = controlgui

        self.openCVWorker = open_CV_worker_autocontrol_gui.openCVWorker()

        # Połączenie sygnałów ze slotami
        self.ui.returnPushButton.clicked.connect(self.returnToControlGui)
        self.ui.executeCommandPushButton.clicked.connect(self.executeCommand)
        self.openCVWorker.sendFrame.connect(self.receiveFrame)
        self.ui.highlightFiguresCheckBox.stateChanged.connect(self.openCVWorker.receiveHighLightEnable)
        self.ui.foundFiguresListWidget.currentRowChanged.connect(self.openCVWorker.receiveSelectedFigureNumber)
        self.openCVWorker.sendFigureText.connect(self.receiveFigureText)

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

    def returnToControlGui(self):
        self.ui.foundFiguresListWidget.clear()
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
                print("ok")

    def enableAllWidgets(self):
        self.ui.executeCommandPushButton.setEnabled(True)
        self.ui.returnPushButton.setEnabled(True)

    def disableAllWidgets(self):
        self.ui.executeCommandPushButton.setEnabled(False)
        self.ui.returnPushButton.setEnabled(False)