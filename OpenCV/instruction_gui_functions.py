from PyQt5 import QtWidgets
from instruction_gui import Ui_Dialog

class InstructionGUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.closePushButton.clicked.connect(self.closeWindow)


    def closeWindow(self):
        self.close()
