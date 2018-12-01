from PyQt5 import QtCore, QtGui
import cv2
import numpy
import glob
from figures.figures_storage import FiguresStore
from figures.figures_process import figures_process
from auto_control.wait_for_camera_to_be_set import WaitForCameraToBeSet
from time import sleep
import threading
import configparser


class OpenCVWorker(QtCore.QObject):

    # SYGNAŁY
    send_frame = QtCore.pyqtSignal(QtGui.QImage)

    # Sygnał emitowany w celu dodania figury do listy znalezionych figur w autocontrol
    send_figure_text = QtCore.pyqtSignal(str)
    send_figure_data = QtCore.pyqtSignal(str)
    send_figure_data_text_clear = QtCore.pyqtSignal()
    send_camera_set = QtCore.pyqtSignal()

    def __init__(self, send_data_to_servos_controller, parent=None):
        QtCore.QObject.__init__(self, parent)

        # Oryginalny pobrany obraz
        # numpy - equivalent of cv::Mat
        self.frame_original = numpy.zeros((480, 640, 1), dtype = "uint8")
        # Przerobiony pobrany obraz
        self.frame_processed = numpy.zeros((480, 640, 1), dtype = "uint8")
        self.capture = cv2.VideoCapture()
        self.run_thread = True
        self.highlight_figure = False
        self.red_lower_bottom, self.red_upper_bottom, self.red_lower_top, self.red_upper_top =\
            self.get_red_color_from_ini_file()

        # Po wykonaniu akcji przez servosController zostaje wyemitowany sygnał do odświeżenia figur znajdujacych
        # sie na polu
        self.send_data_to_servos_controller = send_data_to_servos_controller
        # Magazyn do przechowywania znalezionych figur
        self.figure_store = FiguresStore()
        # Numer figury aktualnie wybranej z listy w oknie autocontrol
        self.selected_figure_number = None
        # Czekanie aż kamera ustawi sobie jasnośc i ostrość
        self.camera_waiter = WaitForCameraToBeSet()

        # Zmiana wartości na true po odczekaniu aż kamera ustawi jasność i ostrość
        self.camera_set = False

        #Połączenie sygnałów ze slotami
        self.send_data_to_servos_controller.send_status.connect(self.get_figures)
        self.camera_waiter.send_camera_set.connect(self.receive_camera_set)

    def get_red_color_from_ini_file(self):

        config_parser = configparser.ConfigParser()
        config_parser.read('colorsRange.ini')

        # Sprawdzam czy jest sekcja 'RedBottom' w pliku konfiguracyjnym
        if 'RedBottom' in config_parser:
            # Zakres koloru niebieskiego
            red_lower_bottom = numpy.fromstring(config_parser['RedBottom']['Lower'],
                                              dtype=numpy.uint8, sep=',')  # Dolny zakres koloru niebieskiego
            red_upper_bottom = numpy.fromstring(config_parser['RedBottom']['Upper'],
                                              dtype=numpy.uint8, sep=',')  # Górny zakres koloru niebieskiego
        # Jeśli nie ma takiej sekcji to defaultowy zakres
        else:
            red_lower_bottom = numpy.array([0, 150, 150], numpy.uint8)  # Dolny zakres koloru czerwonego
            red_upper_bottom = numpy.array([10, 255, 255], numpy.uint8)  # Górny zakres koloru czerwonego

        # Sprawdzam czy jest sekcja 'RedTop' w pliku konfiguracyjnym
        if 'RedTop' in config_parser:
            # Zakres koloru niebieskiego
            red_lower_top= numpy.fromstring(config_parser['RedTop']['Lower'],
                                              dtype=numpy.uint8, sep=',')  # Dolny zakres koloru niebieskiego
            red_upper_top = numpy.fromstring(config_parser['RedTop']['Upper'],
                                              dtype=numpy.uint8, sep=',')  # Górny zakres koloru niebieskiego
        # Jeśli nie ma takiej sekcji to defaultowy zakres
        else:
            red_lower_top = numpy.array([160, 150, 150], numpy.uint8)  # Dolny zakres koloru czerwonego
            red_upper_top = numpy.array([180, 255, 255], numpy.uint8)  # Górny zakres koloru czerwonego

        return red_lower_bottom, red_upper_bottom, red_lower_top, red_upper_top

    def robot_arm_pointer(self):
        # Znajdywanie czerwonego znacznika na obrazie oraz wypisanie jego współrzędnych

        frame_hsv = cv2.cvtColor(self.frame_original, cv2.COLOR_BGR2HSV)

        red_bottom = cv2.inRange(frame_hsv, self.red_lower_bottom, self.red_upper_bottom)  # Wyizolowanie koloru czerwonego
        red_top = cv2.inRange(frame_hsv, self.red_lower_top, self.red_upper_top)  # Wyizolowanie koloru czerwonego

        red = red_bottom | red_top

        # Oddzielenie obrazu wykrytyh figur w kolorze czerwonym od reszty obrazu (obraz binarny)
        thresh_frame = cv2.threshold(red, 45, 255, cv2.THRESH_BINARY)[1]

        # Oczyszczenie obrazu
        thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)
        thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)
        thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

        (check_red, contours_red, hierarchy_red) = cv2.findContours(thresh_frame.copy(),
                                                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Jeśli została znaleziona jakaś czerwona barwa
        if len(contours_red) != 0:
            M = cv2.moments(contours_red[0])  # Momenty obrazka

            # Wyliczanie współrzędnych centroidu
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            center_point = [cx, cy]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.frame_processed, str(center_point), (cx+5, cy), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.circle(self.frame_processed, tuple(center_point), 4, (0, 0, 0), -1)

    # Funkcja odpowiedzialna za podkreślanie figur na obrazie i zaznaczanie czerwonego znacznika
    def process_image(self):

        if self.camera_set:
            self.robot_arm_pointer()

        if self.highlight_figure:
            if self.selected_figure_number != None:
                if len(self.figure_store.figures) != 0:
                    # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)
                    cv2.drawContours(self.frame_processed,
                                     self.figure_store.figures[self.selected_figure_number].contours, -1, (0, 0, 0), 2)
                    cv2.circle(self.frame_processed,
                               tuple(self.figure_store.figures[self.selected_figure_number].coordinates)
                               , 4, (0, 0, 0), -1)

    def find_video_index_and_open_capture(self):
        available_video = glob.glob('/dev/video*')
        if len(available_video):
            video_index = int(available_video[0][-1])
            self.capture.open(video_index)

    def receive_high_light_enable(self):
        self.highlight_figure = not self.highlight_figure

    def end_grabbing(self):
        if self.capture.isOpened():
            # Zwolnienie uchwytu kamery
            self.capture.release()

    def clear_variables(self):
        self.figure_store.clear()
        self.selected_figure_number = None

    # Główna pętla
    def receive_grab_frame(self):

        while not self.capture.isOpened():
            pass

        # Wątek który w tle odczeka pewną ilość czasu aby kamera zdazyła dostosować się do jassnosci otoczenia
        # i wyemituje sygnał
        camera_set_thread = threading.Thread(target=self.camera_waiter.wait_for_camera)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        camera_set_thread.daemon = True
        camera_set_thread.start()

        while self.run_thread:

            grabbed, self.frame_original = self.capture.read()

            if grabbed:

                width = int(self.capture.get(3))  # float
                height = int(self.capture.get(4))  # float

                self.frame_processed = cv2.cvtColor(self.frame_original, cv2.COLOR_BGR2RGB)

                # Przeróbka obrazu
                self.process_image()

                # Stworzenie QImage
                q_image = QtGui.QImage(self.frame_processed, width, height, QtGui.QImage.Format_RGB888)

                self.send_frame.emit(q_image)

                sleep(0.001)

        self.end_grabbing()
        self.clear_variables()
        self.camera_set = False

    def receive_selected_figure_number(self, row_number):
        if row_number != -1:
            self.selected_figure_number = row_number
            self.send_figure_data.emit("Numer : "
                                       + str(self.figure_store.figures[self.selected_figure_number].figure_number)
                                       + "\nKolor : "
                                       + str(self.figure_store.figures[self.selected_figure_number].color)
                                       + "\nŚrodek : "
                                       + str(self.figure_store.figures[self.selected_figure_number].coordinates)
                                       + "\nKąt : "
                                       + str(self.figure_store.figures[self.selected_figure_number].angle))

    def get_figures(self):
        self.clear_variables()
        self.send_figure_data_text_clear.emit()
        figures_process(self.figure_store, self.frame_original)
        for fi in self.figure_store.figures:
            self.send_figure_text.emit("Figura : " + str(fi.figure_number) + ", Kolor : " + str(fi.color))

    def receive_camera_set(self):
        self.camera_set = True
        self.get_figures()

    def get_figure_field(self, figure_number):
        figure_x_coordinate, figure_y_coordinate = self.figure_store.figures[figure_number].coordinates

        if figure_x_coordinate < 320 and figure_y_coordinate < 240:
            return "field_1"
        elif figure_x_coordinate >= 320 and figure_y_coordinate < 240:
            return "field_2"
        elif figure_x_coordinate < 320 and figure_y_coordinate >= 240:
            return "field_3"
        elif figure_x_coordinate >= 320 and figure_y_coordinate >= 240:
            return "field_4"


