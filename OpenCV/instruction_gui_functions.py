from PyQt5 import QtWidgets
from instruction_gui import Ui_Dialog


class InstructionGUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.close_push_button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()
