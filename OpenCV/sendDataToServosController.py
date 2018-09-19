from PyQt5 import QtCore
import struct

class sendDataToServosController(QtCore.QObject):

    # Signals
    sendStatus = QtCore.pyqtSignal()
    sendText = QtCore.pyqtSignal(str)

    def sendData(self, serial, min, max, speed, servo1Value, servo2Value, servo3Value, servo4Value,
                                   servo5Value, servo6Value, firstServo, secondServo, thirdServo, fourthServo, fifthServo,
                                   sixthServo):

        messageToSend = struct.pack('<iiiiiiiiiBBBBBB', min, max, speed, servo1Value, servo2Value, servo3Value,
                                    servo4Value, servo5Value, servo6Value, firstServo, secondServo, thirdServo,
                                    fourthServo, fifthServo, sixthServo)

        if not serial.is_open:
            self.sendText.emit("Seiral port jest zamknięty")
            self.sendStatus.emit()
            return

        serial.write(messageToSend)
        self.sendText.emit("Rpi   : " + str(messageToSend))


        receivedMessage = serial.readline()
        self.sendText.emit("Robot : " + str(receivedMessage))

        self.sendStatus.emit()






