from PyQt5 import QtWidgets, QtGui
from auto_control.auto_control_gui import Ui_Dialog
from open_cv_workers.open_cv_worker_auto_control_gui import OpenCVWorker
from send_data_to_servos.send_data_to_servos_controller_auto_control_gui import SendDataToServosControllerAutoControlGUI
import threading

from auto_control.fields_coordinates import field_coordinates_table


class AutoControlGUI(QtWidgets.QDialog):

    def __init__(self, control_gui, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.control_gui = control_gui
        self.send_data_to_servos_controller = SendDataToServosControllerAutoControlGUI()

        self.open_cv_worker = OpenCVWorker(self.send_data_to_servos_controller)

        self.ui.permitted_operations_list_widget.addItem("Przenieś")

        # Połączenie sygnałów ze slotami
        self.ui.return_push_button.clicked.connect(self.return_to_control_gui)
        self.ui.execute_command_push_button.clicked.connect(self.execute_command)
        self.ui.highlight_figures_check_box.stateChanged.connect(self.open_cv_worker.receive_high_light_enable)
        self.ui.found_figures_list_widget.currentRowChanged.connect(self.open_cv_worker.receive_selected_figure_number)

        self.open_cv_worker.send_frame.connect(self.receive_frame)
        self.open_cv_worker.send_figure_text.connect(self.receive_figure_text)
        self.open_cv_worker.send_figure_data.connect(self.receive_figure_data)
        self.open_cv_worker.send_figure_data_text_clear.connect(self.clear_figures_list_and_info)

        self.send_data_to_servos_controller.send_status.connect(self.enable_all_widgets)
        self.send_data_to_servos_controller.send_commands_text.connect(self.receive_commands_text)

    def start_open_cv_worker(self):
        self.open_cv_worker.run_thread = True
        self.open_cv_worker.find_video_index_and_open_capture()
        self.open_cv_worker_thread = threading.Thread(target=self.open_cv_worker.receive_grab_frame)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        self.open_cv_worker_thread.daemon = True
        self.open_cv_worker_thread.start()

    # Slot do ustawiania otrzymanych od open_cv_worker klatek
    def receive_frame(self, qImage):
        self.ui.open_cv_label.setPixmap(QtGui.QPixmap.fromImage(qImage))

    def receive_figure_text(self, text):
        self.ui.found_figures_list_widget.addItem(text)

    def receive_figure_data(self, data):
        self.ui.figure_data_text_edit.setText(data)

    def receive_commands_text(self, text):
        self.ui.commands_list_widget.addItem(text)

    def return_to_control_gui(self):
        self.clear_figures_list_and_info()
        self.open_cv_worker.run_thread = False
        self.open_cv_worker_thread.join()
        del self.open_cv_worker_thread
        self.control_gui.show()
        self.close()

    def execute_command(self):

        # Sprawdzenie, czy są jakiekolwiek figury i dozwolone operacje
        if self.ui.found_figures_list_widget.count() != 0 and self.ui.permitted_operations_list_widget.count() != 0:
            # Sprawdzenie, czy jest zaznaczona któraś figura i któraś z możliwych operacji
            if (self.ui.found_figures_list_widget.currentRow() != -1 and
                    self.ui.permitted_operations_list_widget.currentRow() != -1):

                self.disable_all_widgets()

                figure_number = self.ui.found_figures_list_widget.currentRow()
                figure_field = self.open_cv_worker.get_figure_field(figure_number)

                data_tab = list()
                data_tab.append(0)  # Max value
                data_tab.append(1000)  # Min value
                data_tab.append(60)  # Speed

                for value in field_coordinates_table[figure_field]:
                    data_tab.append(value)

                data_tab.append(2)
                data_tab.append(3)
                data_tab.append(4)
                data_tab.append(5)
                data_tab.append(1)
                data_tab.append(6)

                thread = threading.Thread(target=self.send_data_to_servos_controller.send_data,
                                          args=(self.control_gui.serial, data_tab[0], data_tab[1], data_tab[2],
                                                data_tab[3], data_tab[4], data_tab[5], data_tab[6], data_tab[7],
                                                data_tab[8], data_tab[9], data_tab[10], data_tab[11], data_tab[12],
                                                data_tab[13], data_tab[14]))
                thread.start()


    def enable_all_widgets(self):
        self.ui.execute_command_push_button.setEnabled(True)
        self.ui.return_push_button.setEnabled(True)

    def disable_all_widgets(self):
        self.ui.execute_command_push_button.setEnabled(False)
        self.ui.return_push_button.setEnabled(False)

    def clear_figures_list_and_info(self):
        self.ui.found_figures_list_widget.clear()
        self.ui.figure_data_text_edit.setText("Numer : \nKolor : \nŚrodek : \nKąt : ")
