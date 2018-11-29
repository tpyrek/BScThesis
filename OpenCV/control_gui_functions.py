from PyQt5 import QtWidgets
from control_gui import Ui_Dialog
from auto_control_gui_functions import AutoControlGUI
from manualcontrol_gui_functions import ManualControlGUI
import serial

class ControlGUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.autocontolgui = AutoControlGUI(self)
        self.manualcontrolgui = ManualControlGUI(self)
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.port = '/dev/ttyUSB0'

        self.ui.autoControlPushButton.clicked.connect(self.openAutoControlWindow)
        self.ui.manualControlPushButton.clicked.connect(self.openManualControlWindow)

    def __del__(self):
        if not serial.is_open:
            self.serial.close()

    def openSerialPort(self):
        try:
            self.serial.open()
        except serial.SerialException as e:
            print(e)
            pass

    def openAutoControlWindow(self):
        self.close()
        self.autocontolgui.show()
        self.autocontolgui.startOpenCVWorker()

    def openManualControlWindow(self):
        self.close()
        self.manualcontrolgui.show()
