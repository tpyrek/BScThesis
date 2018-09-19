__author__ = "Tomasz Pyrek"

from PyQt5 import QtWidgets
import sys
from configuration_gui_functions import ConfigurationGUI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = ConfigurationGUI()
    myapp.show()
    sys.exit(app.exec_())

