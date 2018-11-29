from PyQt5 import QtWidgets, QtCore, QtGui
from configuration_gui import Ui_Dialog
from instruction_gui_functions import InstructionGUI
from control_gui_functions import ControlGUI
from open_cv_worker_configuration_gui import OpenCVWorker
import threading

class ConfigurationGUI(QtWidgets.QDialog):

    send_signal_to_set_color = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.instruction_gui = InstructionGUI()
        self.control_gui = ControlGUI()

        self.open_cv_worker = OpenCVWorker()
        self.open_cv_worker_thread = threading.Thread(target=self.open_cv_worker.receive_grab_frame)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        self.open_cv_worker_thread.daemon = True

        self.disable_configuration_buttons()
        self.ui.ok_push_button.setDisabled(True)
        # Licznik enable_ok_button - Zostaje zwiekszony przy pobraniu każdego koloru i kiedy wszystkie kolory zostaną pobrane,
        # zostaje odblokowany przycisk ok_push_button
        self.enable_ok_button = 0
        self.first_frame = True

        self.ui.commands_list_widget.addItem("Kalibracja kolorów")
        self.ui.skip_calibration_push_button.setStyleSheet("background-color: red")

        # Połączenie sygnałów ze slotami
        self.ui.instruction_push_button.clicked.connect(self.open_instruction_window)
        self.ui.set_blue_push_button.clicked.connect(self.set_blue_color)
        self.ui.set_yellow_push_button.clicked.connect(self.set_yellow_color)
        self.ui.set_green_push_button.clicked.connect(self.set_green_color)
        self.ui.set_red_push_button.clicked.connect(self.set_red_color)
        self.ui.ok_push_button.clicked.connect(self.open_control_window)
        self.ui.skip_calibration_push_button.clicked.connect(self.skip_calibration)

        self.send_signal_to_set_color.connect(self.open_cv_worker.getColorFromFrame)

        self.open_cv_worker.send_text.connect(self.receive_text)
        self.open_cv_worker.send_frame.connect(self.receive_frame)
        self.open_cv_worker.receive_setup(0)
        self.open_cv_worker_thread.start()

    # SLOTY

    # Ustawienie otrzymanego od open_cv_worker tekstu
    def receive_text(self, text):
        self.ui.commands_list_widget.addItem(text)

    # Wyświetlenie otrzymanego od open_cv_worker obrazka
    def receive_frame(self, q_image):
        if self.first_frame:
            self.enable_configuration_buttons()
            self.first_frame = False
        self.ui.open_cv_label.setPixmap(QtGui.QPixmap.fromImage(q_image))

    # Otwarcie okna instrukcji po naciśnięciu przycisku
    def open_instruction_window(self):
        self.instruction_gui.show()

    def set_blue_color(self):
        self.ui.set_blue_push_button.setDisabled(True)
        self.ui.skip_calibration_push_button.setDisabled(True)
        self.enable_ok_button = self.enable_ok_button + 1
        if self.enable_ok_button == 4:
            self.ui.ok_push_button.setEnabled(True)
        self.send_signal_to_set_color.emit("Blue")

    def set_yellow_color(self):
        self.ui.set_yellow_push_button.setDisabled(True)
        self.ui.skip_calibration_push_button.setDisabled(True)
        self.enable_ok_button = self.enable_ok_button + 1
        if self.enable_ok_button == 4:
            self.ui.ok_push_button.setEnabled(True)
        self.send_signal_to_set_color.emit("Yellow")

    def set_green_color(self):
        self.ui.set_green_push_button.setDisabled(True)
        self.ui.skip_calibration_push_button.setDisabled(True)
        self.enable_ok_button = self.enable_ok_button + 1
        if self.enable_ok_button == 4:
            self.ui.ok_push_button.setEnabled(True)
        self.send_signal_to_set_color.emit("Green")

    def set_red_color(self):
        self.ui.set_red_push_button.setDisabled(True)
        self.ui.skip_calibration_push_button.setDisabled(True)
        self.enable_ok_button = self.enable_ok_button + 1
        if self.enable_ok_button == 4:
            self.ui.ok_push_button.setEnabled(True)
        self.send_signal_to_set_color.emit("Red")

    def open_control_window(self):
        self.open_cv_worker.run_thread = False
        self.open_cv_worker_thread.join()
        del self.open_cv_worker_thread
        self.close()
        self.control_gui.show()
        self.control_gui.openSerialPort()

    def skip_calibration(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setWindowTitle("Uwaga !")
        message_box.setText("Jeśli pominiesz ten krok, aplikacja może nie działać poprawnie!")
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        message_box_button_yes = message_box.button(QtWidgets.QMessageBox.Yes)
        message_box_button_yes.setText("Ok, pomiń")
        message_box_button_no = message_box.button(QtWidgets.QMessageBox.No)
        message_box_button_no.setText("Wróć")
        message_box.exec()

        if message_box.clickedButton() == message_box_button_yes:
            self.open_cv_worker.run_thread = False
            self.open_cv_worker_thread.join()
            del self.open_cv_worker_thread
            self.close()
            self.control_gui.show()
            self.control_gui.openSerialPort()

        elif message_box.clickedButton() == message_box_button_no:
            return

    # FUNKCJE
    def disable_configuration_buttons(self):
        self.ui.set_blue_push_button.setDisabled(True)
        self.ui.set_yellow_push_button.setDisabled(True)
        self.ui.set_green_push_button.setDisabled(True)
        self.ui.set_red_push_button.setDisabled(True)

    def enable_configuration_buttons(self):
        self.ui.set_blue_push_button.setEnabled(True)
        self.ui.set_yellow_push_button.setEnabled(True)
        self.ui.set_green_push_button.setEnabled(True)
        self.ui.set_red_push_button.setEnabled(True)
