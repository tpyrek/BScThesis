from PyQt5 import QtCore
import struct


# Do ustawienia ramienia po zakończeniu działania aplikacji
class SendDataToServosControllerAtAppClosing(QtCore.QObject):

    def send_data(self, serial):

        if not serial.is_open:
            return

        message_to_send = struct.pack('<iiiiiiiiiBBBBBB', 0, 1000, 30, 422, 117, 67, 78, 61, 205, 5, 6, 2, 4, 3, 1)
        serial.write(message_to_send)
        serial.readline()

