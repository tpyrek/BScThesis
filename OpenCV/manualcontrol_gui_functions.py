from PyQt5 import QtWidgets
from manualcontrol_gui import Ui_Dialog
import sendDataToServosControllerManualControlGUI
import threading

class ManualcontrolGUI(QtWidgets.QDialog):

    def __init__(self, controlgui, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initialize()
        self.controlgui = controlgui
        self.sendDataToServosController = \
            sendDataToServosControllerManualControlGUI.sendDataToServosControllerManualControlGUI()

        self.ui.returnPushButton.clicked.connect(self.returnToControlGui)
        self.ui.neutralPositionPushButton.clicked.connect(self.setNeutralPosition)

        self.ui.servo1HorizontalSlider.sliderReleased.connect(self.servo1SetValue)
        self.ui.servo1HorizontalSlider.valueChanged.connect(self.servo1SliderValueChanged)
        self.ui.servo2HorizontalSlider.sliderReleased.connect(self.servo2SetValue)
        self.ui.servo2HorizontalSlider.valueChanged.connect(self.servo2SliderValueChanged)
        self.ui.servo3HorizontalSlider.sliderReleased.connect(self.servo3SetValue)
        self.ui.servo3HorizontalSlider.valueChanged.connect(self.servo3SliderValueChanged)
        self.ui.servo4HorizontalSlider.sliderReleased.connect(self.servo4SetValue)
        self.ui.servo4HorizontalSlider.valueChanged.connect(self.servo4SliderValueChanged)
        self.ui.servo5HorizontalSlider.sliderReleased.connect(self.servo5SetValue)
        self.ui.servo5HorizontalSlider.valueChanged.connect(self.servo5SliderValueChanged)
        self.ui.servo6HorizontalSlider.sliderReleased.connect(self.servo6SetValue)
        self.ui.servo6HorizontalSlider.valueChanged.connect(self.servo6SliderValueChanged)

        self.sendDataToServosController.sendStatus.connect(self.enableAllWidgets)
        self.sendDataToServosController.sendCommandsText.connect(self.receiveCommandsText)

    def initialize(self):
        self.ui.servo1HorizontalSlider.setMaximum(1000)
        self.ui.servo2HorizontalSlider.setMaximum(1000)
        self.ui.servo3HorizontalSlider.setMaximum(1000)
        self.ui.servo4HorizontalSlider.setMaximum(1000)
        self.ui.servo5HorizontalSlider.setMaximum(1000)
        self.ui.servo6HorizontalSlider.setMaximum(1000)

        self.ui.servo1HorizontalSlider.setMinimum(0)
        self.ui.servo2HorizontalSlider.setMinimum(0)
        self.ui.servo3HorizontalSlider.setMinimum(0)
        self.ui.servo4HorizontalSlider.setMinimum(0)
        self.ui.servo5HorizontalSlider.setMinimum(0)
        self.ui.servo6HorizontalSlider.setMinimum(0)

        self.ui.servo1HorizontalSlider.setValue(500)
        self.ui.servo2HorizontalSlider.setValue(500)
        self.ui.servo3HorizontalSlider.setValue(500)
        self.ui.servo4HorizontalSlider.setValue(500)
        self.ui.servo5HorizontalSlider.setValue(500)
        self.ui.servo6HorizontalSlider.setValue(500)

        self.ui.servo1LocationLabel.setText(
            str(self.ui.servo1HorizontalSlider.value()) + "/" + str(self.ui.servo1HorizontalSlider.maximum()))
        self.ui.servo2LocationLabel.setText(
            str(self.ui.servo2HorizontalSlider.value()) + "/" + str(self.ui.servo2HorizontalSlider.maximum()))
        self.ui.servo3LocationLabel.setText(
            str(self.ui.servo3HorizontalSlider.value()) + "/" + str(self.ui.servo3HorizontalSlider.maximum()))
        self.ui.servo4LocationLabel.setText(
            str(self.ui.servo4HorizontalSlider.value()) + "/" + str(self.ui.servo4HorizontalSlider.maximum()))
        self.ui.servo5LocationLabel.setText(
            str(self.ui.servo5HorizontalSlider.value()) + "/" + str(self.ui.servo5HorizontalSlider.maximum()))
        self.ui.servo6LocationLabel.setText(
            str(self.ui.servo6HorizontalSlider.value()) + "/" + str(self.ui.servo6HorizontalSlider.maximum()))

        self.ui.speedSpinBox.setValue(30)
        self.ui.commandsListWidget.addItem("Manualna kontrola ramienia")

    def receiveCommandsText(self, text):
        self.ui.commandsListWidget.addItem(text)

    def returnToControlGui(self):
        self.controlgui.show()
        self.close()

    def servo1SliderValueChanged(self):
        self.ui.servo1LocationLabel.setText(
            str(self.ui.servo1HorizontalSlider.value()) + "/" + str(self.ui.servo1HorizontalSlider.maximum()))

    def servo1SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4],dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()


    def servo2SliderValueChanged(self):
        self.ui.servo2LocationLabel.setText(
            str(self.ui.servo2HorizontalSlider.value()) + "/" + str(self.ui.servo2HorizontalSlider.maximum()))

    def servo2SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

    def servo3SliderValueChanged(self):
        self.ui.servo3LocationLabel.setText(
            str(self.ui.servo3HorizontalSlider.value()) + "/" + str(self.ui.servo3HorizontalSlider.maximum()))

    def servo3SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

    def servo4SliderValueChanged(self):
        self.ui.servo4LocationLabel.setText(
            str(self.ui.servo4HorizontalSlider.value()) + "/" + str(self.ui.servo4HorizontalSlider.maximum()))

    def servo4SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

    def servo5SliderValueChanged(self):
        self.ui.servo5LocationLabel.setText(
            str(self.ui.servo5HorizontalSlider.value()) + "/" + str(self.ui.servo5HorizontalSlider.maximum()))

    def servo5SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

    def servo6SliderValueChanged(self):
        self.ui.servo6LocationLabel.setText(
            str(self.ui.servo6HorizontalSlider.value()) + "/" + str(self.ui.servo6HorizontalSlider.maximum()))

    def servo6SetValue(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(self.ui.servo1HorizontalSlider.value())
        dataTab.append(self.ui.servo2HorizontalSlider.value())
        dataTab.append(self.ui.servo3HorizontalSlider.value())
        dataTab.append(self.ui.servo4HorizontalSlider.value())
        dataTab.append(self.ui.servo5HorizontalSlider.value())
        dataTab.append(self.ui.servo6HorizontalSlider.value())
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

    def setNeutralPosition(self):

        self.disableAllWidgets()

        dataTab = []
        dataTab.append(self.ui.servo1HorizontalSlider.minimum())
        dataTab.append(self.ui.servo1HorizontalSlider.maximum())
        dataTab.append(self.ui.speedSpinBox.value())
        dataTab.append(500)
        dataTab.append(500)
        dataTab.append(500)
        dataTab.append(500)
        dataTab.append(500)
        dataTab.append(500)
        dataTab.append(1)
        dataTab.append(2)
        dataTab.append(3)
        dataTab.append(4)
        dataTab.append(5)
        dataTab.append(6)

        thread = threading.Thread(target=self.sendDataToServosController.sendData,
                                  args=(self.controlgui.serial, dataTab[0], dataTab[1], dataTab[2],
                                        dataTab[3], dataTab[4], dataTab[5], dataTab[6], dataTab[7], dataTab[8],
                                        dataTab[9], dataTab[10], dataTab[11], dataTab[12], dataTab[13],
                                        dataTab[14]))
        thread.start()

        self.ui.servo1HorizontalSlider.setValue(500)
        self.ui.servo2HorizontalSlider.setValue(500)
        self.ui.servo3HorizontalSlider.setValue(500)
        self.ui.servo4HorizontalSlider.setValue(500)
        self.ui.servo5HorizontalSlider.setValue(500)
        self.ui.servo6HorizontalSlider.setValue(500)

    def enableAllWidgets(self):
        self.ui.servo1HorizontalSlider.setEnabled(True)
        self.ui.servo2HorizontalSlider.setEnabled(True)
        self.ui.servo3HorizontalSlider.setEnabled(True)
        self.ui.servo4HorizontalSlider.setEnabled(True)
        self.ui.servo5HorizontalSlider.setEnabled(True)
        self.ui.servo6HorizontalSlider.setEnabled(True)

        self.ui.neutralPositionPushButton.setEnabled(True)
        self.ui.returnPushButton.setEnabled(True)

    def disableAllWidgets(self):
        self.ui.servo1HorizontalSlider.setEnabled(False)
        self.ui.servo2HorizontalSlider.setEnabled(False)
        self.ui.servo3HorizontalSlider.setEnabled(False)
        self.ui.servo4HorizontalSlider.setEnabled(False)
        self.ui.servo5HorizontalSlider.setEnabled(False)
        self.ui.servo6HorizontalSlider.setEnabled(False)

        self.ui.neutralPositionPushButton.setEnabled(False)
        self.ui.returnPushButton.setEnabled(False)
