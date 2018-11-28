from PyQt5 import QtCore
import struct
from time import sleep


# Do automatycznej kontroli ramienia
class sendDataToServosControllerAutoControlGUI(QtCore.QObject):

    # Signals
    sendStatus = QtCore.pyqtSignal()
    sendCommandsText = QtCore.pyqtSignal(str)

    def sendData(self, serial, min, max, speed, servo1Value, servo2Value, servo3Value, servo4Value,
                 servo5Value, servo6Value, firstServo, secondServo, thirdServo, fourthServo, fifthServo,
                 sixthServo):

        if not serial.is_open:
            self.sendCommandsText.emit("Serial port jest zamknięty")
            sleep(4)
            self.sendStatus.emit()
            return

        messageToSend = struct.pack('<iiiiiiiiiBBBBBB', min, max, speed, servo1Value, servo2Value, servo3Value,
                                    servo4Value, servo5Value, servo6Value, firstServo, secondServo, thirdServo,
                                    fourthServo, fifthServo, sixthServo)

        serial.write(messageToSend)
        self.sendCommandsText.emit("Rpi   : " + str(messageToSend))

        receivedMessage = serial.readline()
        self.sendCommandsText.emit("Robot : " + str(receivedMessage))

        # Przeniesienie klocka w wyznaczone miejsce
        messageToSend = struct.pack('<iiiiiiiiiBBBBBB', min, max, speed, servo1Value, servo2Value, servo3Value,
                                    servo4Value, servo5Value, servo6Value, firstServo, secondServo, thirdServo,
                                    fourthServo, fifthServo, sixthServo)

        serial.write(messageToSend)
        self.sendCommandsText.emit("Rpi   : " + str(messageToSend))

        receivedMessage = serial.readline()
        self.sendCommandsText.emit("Robot : " + str(receivedMessage))

        # Ustawienie robota w pozycji neutralnej
        messageToSend = struct.pack('<iiiiiiiiiBBBBBB', min, max, speed, servo1Value, servo2Value, servo3Value,
                                    servo4Value, servo5Value, servo6Value, firstServo, secondServo, thirdServo,
                                    fourthServo, fifthServo, sixthServo)

        serial.write(messageToSend)
        self.sendCommandsText.emit("Rpi   : " + str(messageToSend))

        receivedMessage = serial.readline()
        self.sendCommandsText.emit("Robot : " + str(receivedMessage))

        # Wysłanie sygnału o zakończonej pracy w celu oblokowania wigdetów i odświeżenie listy figur na planszy
        self.sendStatus.emit()





