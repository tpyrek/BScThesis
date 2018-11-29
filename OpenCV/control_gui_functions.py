from PyQt5 import QtWidgets
from control_gui import Ui_Dialog
from auto_control_gui_functions import AutoControlGUI
from manual_control_gui_functions import ManualControlGUI
import serial


class ControlGUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.auto_control_gui = AutoControlGUI(self)
        self.manual_control_gui = ManualControlGUI(self)
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.port = '/dev/ttyUSB0'

        self.ui.auto_control_push_button.clicked.connect(self.open_auto_control_window)
        self.ui.manual_control_push_button.clicked.connect(self.open_manual_control_window)

    def __del__(self):
        if not self.serial.is_open:
            self.serial.close()

    def open_serial_port(self):
        try:
            self.serial.open()
        except serial.SerialException as e:
            print(e)
            pass

    def open_auto_control_window(self):
        self.close()
        self.auto_control_gui.show()
        self.auto_control_gui.start_open_cv_worker()

    def open_manual_control_window(self):
        self.close()
        self.manual_control_gui.show()
