from PyQt5 import QtCore
from time import sleep


class WaitForCameraToBeSet(QtCore.QObject):

    send_camera_set = QtCore.pyqtSignal()

    def wait_for_camera(self):
        # Poczekać aż ustawi sie kamera (jasność,ostrość)

        sleep(10)
        self.send_camera_set.emit()
        return
