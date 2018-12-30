from PyQt5 import QtCore
import struct


# Do manualnej kontroli ramienia
class SendDataToServosControllerManualControlGUI(QtCore.QObject):

    # Signals
    send_status = QtCore.pyqtSignal()
    send_commands_text = QtCore.pyqtSignal(str)

    def send_data(self, serial, min, max, speed, servo1_value, servo2_value, servo3_value, servo4_value,
                  servo5_value, servo6_value, first_servo, second_servo, third_servo, fourth_servo, fifth_servo,
                  sixth_servo):

        if not serial.is_open:
            self.send_commands_text.emit("Port szeregowy jest zamknięty")
            self.send_status.emit()
            return

        message_to_send = struct.pack('<iiiiiiiiiBBBBBB', min, max, speed, servo1_value, servo2_value, servo3_value,
                                      servo4_value, servo5_value, servo6_value, first_servo, second_servo, third_servo,
                                      fourth_servo, fifth_servo, sixth_servo)

        serial.write(message_to_send)
        self.send_commands_text.emit("Rpi   : " + str(message_to_send))

        received_message = serial.readline()
        self.send_commands_text.emit("Robot : " + str(received_message))

        # Wysłanie sygnału o zakończonej pracy w celu oblokowania wigdetów
        self.send_status.emit()
