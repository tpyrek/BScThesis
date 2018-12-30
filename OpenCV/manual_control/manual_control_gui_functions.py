from PyQt5 import QtWidgets
from manual_control.manual_control_gui import Ui_Dialog
from send_data_to_servos.send_data_to_servos_controller_manual_control_gui \
    import SendDataToServosControllerManualControlGUI
from send_data_to_servos.send_data_to_servos_controller_at_app_closing import SendDataToServosControllerAtAppClosing
import threading


class ManualControlGUI(QtWidgets.QDialog):

    def __init__(self, control_gui, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.robot_arm_ready = True
        self.initialize()
        self.control_gui = control_gui
        self.send_data_to_servos_controller = SendDataToServosControllerManualControlGUI()

        self.ui.return_push_button.clicked.connect(self.return_to_control_gui)
        self.ui.neutral_position_push_button.clicked.connect(self.set_neutral_position)

        self.ui.servo1_horizontal_slider.sliderReleased.connect(self.servo1_set_value)
        self.ui.servo1_horizontal_slider.valueChanged.connect(self.servo1_slider_value_changed)
        self.ui.servo2_horizontal_slider.sliderReleased.connect(self.servo2_set_value)
        self.ui.servo2_horizontal_slider.valueChanged.connect(self.servo2_slider_value_changed)
        self.ui.servo3_horizontal_slider.sliderReleased.connect(self.servo3_set_value)
        self.ui.servo3_horizontal_slider.valueChanged.connect(self.servo3_slider_value_changed)
        self.ui.servo4_horizontal_slider.sliderReleased.connect(self.servo4_set_value)
        self.ui.servo4_horizontal_slider.valueChanged.connect(self.servo4_slider_value_changed)
        self.ui.servo5_horizontal_slider.sliderReleased.connect(self.servo5_set_value)
        self.ui.servo5_horizontal_slider.valueChanged.connect(self.servo5_slider_value_changed)
        self.ui.servo6_horizontal_slider.sliderReleased.connect(self.servo6_set_value)
        self.ui.servo6_horizontal_slider.valueChanged.connect(self.servo6_slider_value_changed)

        self.send_data_to_servos_controller.send_status.connect(self.enable_all_widgets)
        self.send_data_to_servos_controller.send_commands_text.connect(self.receive_commands_text)

    def closeEvent(self, event):

        if not self.robot_arm_ready:
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Warning)
            message_box.setWindowTitle("Uwaga")
            message_box.setText('Robot nie zakończył pracy. Operacja możliwa dopiero po jej ukończeniu')
            message_box.exec()

            event.ignore()

        elif self.robot_arm_ready:

            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            message_box.setWindowTitle("Informacja")
            message_box.setText('Po kliknięciu "Ok" nastąpi ustawienie robota w pozycji spoczynku')
            message_box.exec()

            send_data_to_servos_controller_at_app_closing = SendDataToServosControllerAtAppClosing()
            send_data_to_servos_controller_at_app_closing.send_data(self.control_gui.serial)

            event.accept()

    def initialize(self):
        self.ui.servo1_horizontal_slider.setMaximum(1000)
        self.ui.servo2_horizontal_slider.setMaximum(1000)
        self.ui.servo3_horizontal_slider.setMaximum(1000)
        self.ui.servo4_horizontal_slider.setMaximum(1000)
        self.ui.servo5_horizontal_slider.setMaximum(1000)
        self.ui.servo6_horizontal_slider.setMaximum(1000)

        self.ui.servo1_horizontal_slider.setMinimum(0)
        self.ui.servo2_horizontal_slider.setMinimum(0)
        self.ui.servo3_horizontal_slider.setMinimum(0)
        self.ui.servo4_horizontal_slider.setMinimum(0)
        self.ui.servo5_horizontal_slider.setMinimum(0)
        self.ui.servo6_horizontal_slider.setMinimum(0)

        self.ui.servo1_horizontal_slider.setValue(500)
        self.ui.servo2_horizontal_slider.setValue(500)
        self.ui.servo3_horizontal_slider.setValue(500)
        self.ui.servo4_horizontal_slider.setValue(500)
        self.ui.servo5_horizontal_slider.setValue(500)
        self.ui.servo6_horizontal_slider.setValue(500)

        self.ui.servo1_location_label.setText(
            str(self.ui.servo1_horizontal_slider.value()) + "/" + str(self.ui.servo1_horizontal_slider.maximum()))
        self.ui.servo2_location_label.setText(
            str(self.ui.servo2_horizontal_slider.value()) + "/" + str(self.ui.servo2_horizontal_slider.maximum()))
        self.ui.servo3_location_label.setText(
            str(self.ui.servo3_horizontal_slider.value()) + "/" + str(self.ui.servo3_horizontal_slider.maximum()))
        self.ui.servo4_location_label.setText(
            str(self.ui.servo4_horizontal_slider.value()) + "/" + str(self.ui.servo4_horizontal_slider.maximum()))
        self.ui.servo5_location_label.setText(
            str(self.ui.servo5_horizontal_slider.value()) + "/" + str(self.ui.servo5_horizontal_slider.maximum()))
        self.ui.servo6_location_label.setText(
            str(self.ui.servo6_horizontal_slider.value()) + "/" + str(self.ui.servo6_horizontal_slider.maximum()))

        self.ui.speed_spin_box.setValue(30)
        self.ui.commands_list_widget.addItem("Manualna kontrola ramienia")

    def receive_commands_text(self, text):
        self.ui.commands_list_widget.addItem(text)

    def return_to_control_gui(self):
        self.close()
        self.control_gui.show()

    def servo1_slider_value_changed(self):
        self.ui.servo1_location_label.setText(
            str(self.ui.servo1_horizontal_slider.value()) + "/" + str(self.ui.servo1_horizontal_slider.maximum()))

    def servo1_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def servo2_slider_value_changed(self):
        self.ui.servo2_location_label.setText(
            str(self.ui.servo2_horizontal_slider.value()) + "/" + str(self.ui.servo2_horizontal_slider.maximum()))

    def servo2_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def servo3_slider_value_changed(self):
        self.ui.servo3_location_label.setText(
            str(self.ui.servo3_horizontal_slider.value()) + "/" + str(self.ui.servo3_horizontal_slider.maximum()))

    def servo3_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def servo4_slider_value_changed(self):
        self.ui.servo4_location_label.setText(
            str(self.ui.servo4_horizontal_slider.value()) + "/" + str(self.ui.servo4_horizontal_slider.maximum()))

    def servo4_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def servo5_slider_value_changed(self):
        self.ui.servo5_location_label.setText(
            str(self.ui.servo5_horizontal_slider.value()) + "/" + str(self.ui.servo5_horizontal_slider.maximum()))

    def servo5_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def servo6_slider_value_changed(self):
        self.ui.servo6_location_label.setText(
            str(self.ui.servo6_horizontal_slider.value()) + "/" + str(self.ui.servo6_horizontal_slider.maximum()))

    def servo6_set_value(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(self.ui.servo1_horizontal_slider.value())
        data_tab.append(self.ui.servo2_horizontal_slider.value())
        data_tab.append(self.ui.servo3_horizontal_slider.value())
        data_tab.append(self.ui.servo4_horizontal_slider.value())
        data_tab.append(self.check_servo_value(self.ui.servo5_horizontal_slider.value()))
        data_tab.append(self.check_servo_value(self.ui.servo6_horizontal_slider.value()))
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

    def set_neutral_position(self):

        self.disable_all_widgets()

        data_tab = list()
        data_tab.append(self.ui.servo1_horizontal_slider.minimum())
        data_tab.append(self.ui.servo1_horizontal_slider.maximum())
        data_tab.append(self.ui.speed_spin_box.value())
        data_tab.append(500)
        data_tab.append(500)
        data_tab.append(500)
        data_tab.append(500)
        data_tab.append(500)
        data_tab.append(500)
        data_tab.append(1)
        data_tab.append(3)
        data_tab.append(4)
        data_tab.append(2)
        data_tab.append(5)
        data_tab.append(6)

        thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                  args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                        data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7], data_tab[8],
                                        data_tab[9], data_tab[10], data_tab[11], data_tab[12], data_tab[13],
                                        data_tab[14]))
        thread.start()

        self.ui.servo1_horizontal_slider.setValue(500)
        self.ui.servo2_horizontal_slider.setValue(500)
        self.ui.servo3_horizontal_slider.setValue(500)
        self.ui.servo4_horizontal_slider.setValue(500)
        self.ui.servo5_horizontal_slider.setValue(500)
        self.ui.servo6_horizontal_slider.setValue(500)

    def enable_all_widgets(self):
        self.ui.servo1_horizontal_slider.setEnabled(True)
        self.ui.servo2_horizontal_slider.setEnabled(True)
        self.ui.servo3_horizontal_slider.setEnabled(True)
        self.ui.servo4_horizontal_slider.setEnabled(True)
        self.ui.servo5_horizontal_slider.setEnabled(True)
        self.ui.servo6_horizontal_slider.setEnabled(True)

        self.ui.neutral_position_push_button.setEnabled(True)
        self.ui.return_push_button.setEnabled(True)

        self.robot_arm_ready = True

    def disable_all_widgets(self):
        self.ui.servo1_horizontal_slider.setEnabled(False)
        self.ui.servo2_horizontal_slider.setEnabled(False)
        self.ui.servo3_horizontal_slider.setEnabled(False)
        self.ui.servo4_horizontal_slider.setEnabled(False)
        self.ui.servo5_horizontal_slider.setEnabled(False)
        self.ui.servo6_horizontal_slider.setEnabled(False)

        self.ui.neutral_position_push_button.setEnabled(False)
        self.ui.return_push_button.setEnabled(False)

        self.robot_arm_ready = False

    def check_servo_value(self, value):
        if value < 70:
            return 70
        elif value > 930:
            return 930
        else:
            return value
