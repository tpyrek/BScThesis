from PyQt5 import QtWidgets
from control_gui import Ui_Dialog
from autocontrol_gui_functions import AutocontrolGUI
from manualcontrol_gui_functions import ManualcontrolGUI
import serial

class ControlGUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.autocontolgui = AutocontrolGUI(self)
        self.manualcontrolgui = ManualcontrolGUI(self)
        self.serial = serial.Serial()

        self.ui.autoControlPushButton.clicked.connect(self.openAutoControlWindow)
        self.ui.manualControlPushButton.clicked.connect(self.openManualControlWindow)

    def __del__(self):
        if not serial.is_open:
            self.serial.close()

    def openSerialPort(self):
        self.serial.baudrate = 9600
        self.serial.port = '/dev/ttyUSB0'
        try:
            self.serial.open()
        except:
            pass


    def openAutoControlWindow(self):
        self.close()
        self.autocontolgui.show()
        self.autocontolgui.startOpenCVWorker()


    def openManualControlWindow(self):
        self.close()
        self.manualcontrolgui.show()