from PyQt5 import QtCore
from time import sleep


class waitForCameraToBeSet(QtCore.QObject):

    sendCameraSet = QtCore.pyqtSignal()

    def waitForCamera(self):
        # Poczekać aż ustawi sie kamera (jasność,ostrość)

        sleep(10)
        self.sendCameraSet.emit()
        return
