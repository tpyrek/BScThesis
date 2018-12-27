from PyQt5 import QtCore
import struct


# Do ustawienia ramienia po zakończeniu działania aplikacji
class SendDataToServosControllerAtAppClosing(QtCore.QObject):

    def send_data(self, serial):

        print('ok')
        if not serial.is_open:
            self.send_commands_text.emit("Serial port jest zamknięty")
            self.send_status.emit()
            return

        message_to_send = struct.pack('<iiiiiiiiiBBBBBB', 0, 1000, 30, 473, 132, 73, 86, 70, 230, 5, 6, 2, 4, 3, 1)

        serial.write(message_to_send)

        serial.readline()

