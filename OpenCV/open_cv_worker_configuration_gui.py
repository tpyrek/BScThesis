from PyQt5 import QtCore, QtGui
import cv2
import numpy
import configparser
from time import sleep


class OpenCVWorker(QtCore.QObject):

    # SYGNAŁY
    send_frame = QtCore.pyqtSignal(QtGui.QImage)
    send_text = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        # Oryginalna pobrana klatka z kamery
        # numpy - odpowienik cv::Mat
        self.frame_original = numpy.zeros((480, 640, 1), dtype = "uint8")
        # Obrobiona klatka z kamery
        self.frame_processed = numpy.zeros((480, 640, 1), dtype = "uint8")
        self.capture = cv2.VideoCapture()
        self.run_thread = True


    # Funkcja dodająca kropkę na środku obrazu - ułatwienie kalibracji kolorów
    def process_image(self):

        width = int(self.capture.get(3))  # float
        height = int(self.capture.get(4))  # float

        center_point = [int(width / 2), int(height / 2)]  # Wyznaczenie środka (x,y)

        cv2.circle(self.frame_processed, tuple(center_point), 10, (0, 0, 0), -1)

    # camera_device_number - numer uchwytu używany przez VideoCapture
    def receive_setup(self, camera_device_number: int):
        # Start pobierania ramek
        self.capture.open(camera_device_number)

    def end_grabbing(self):
        if self.capture.isOpened():
            # Zwolnienie uchwytu kamery
            self.capture.release()

    # Główny wątek do pobierania klatek z kamery
    def receive_grab_frame(self):

        while not self.capture.isOpened():
            pass

        while self.run_thread:

            grabbed, self.frame_original = self.capture.read()

            if grabbed:

                width = int(self.capture.get(3))  # float
                height = int(self.capture.get(4))  # float

                self.frame_processed = cv2.cvtColor(self.frame_original, cv2.COLOR_BGR2RGB)

                # Obróbka obrazu
                self.process_image()

                # Stworzenie q_image aby wyświetlić w polu QLabel
                q_image = QtGui.QImage(self.frame_processed, width, height, QtGui.QImage.Format_RGB888)

                self.send_frame.emit(q_image)

                sleep(0.001)

        self.end_grabbing()

    # Funkcja zapisuje podany zakres koloru w pliku konfiguracyjnym z rozszerzeniem .ini
    # color - String mówiący jaki kolor zapisać
    # color_lower - dolny zakres koloru
    # color_upper - górny zakres koloru
    def set_colors_range_in_ini_file(self, color, color_lower, color_upper):

        # Usunięcie nawiasów kwadratowych z tablicy
        color_lower = ",".join(str(i) for i in color_lower)
        color_upper = ",".join(str(i) for i in color_upper)

        # Utworznie obiektu config_parser
        config_parser = configparser.ConfigParser()

        # Odczytanie pliku configuracyjnego oraz pobranie sekcji i wartości
        config_parser.read('colorsRange.ini')

        # Sprawdza, czy sekcja która ma być zmieniona jest w pliku jak nie to tworzy ją
        if color not in config_parser:
            config_parser.add_section(color)

        # Ustawienie wartości dla wybranej sekcji color
        config_parser.set(color, 'lower', str(color_lower))
        config_parser.set(color, 'upper', str(color_upper))

        # Wpisanie wartości do pliku
        # Jeśli nie będzie pliku o podanej nazwie to zostanie on stworzony
        with open('colorsRange.ini', 'w') as configfile:
            config_parser.write(configfile)

    # Slot - Funkcja wywoływana przy naciśnieciu przycisku koloru w configurationGUI - pobiera kolory z kilku punktów
    # wokół środka oraz wylicza średnią dla lepszego przyblizenia koloru
    def get_color_from_frame(self, color: str):

        # Tablica do przechowania kolorów punktów z obrazu do wyliczenia średniej
        points_table = []

        width = int(self.capture.get(3))  # float
        height = int(self.capture.get(4))  # float

        center_point = [int(width / 2), int(height / 2)]  # Wyznaczenie środka (x,y)
        frame_hsv = cv2.cvtColor(self.frame_original, cv2.COLOR_BGR2HSV)  # Konwersja prezentacji barw z RGB na HSV

        # -5. -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
        # Pobranie kolorów punktu z kwadratu o boku 11 o środku w śroku przetwarzanego obrazu
        for i in range(-5, 6):
            for j in range(-5, 6):
                # Pobranie koloru z punktu o podanych współrzędnych (tutaj ze środka obrazu):
                # pierwsza to linie czyli y druga to kolomny czyli x
                # oraz wpisanie ich do tabeli
                points_table.append(frame_hsv[center_point[1] + j, center_point[0] + i])

        # Wartosci H, S, V reprezentacji barw
        h = 0
        s = 0
        v = 0

        # Obliczenie średniej dla lepszego przybliżenia barwy

        for points in points_table:
            h = h + points[0]
            s = s + points[1]
            v = v + points[2]

        h = int(h/len(points_table))
        s = int(s/len(points_table))
        v = int(v/len(points_table))

        # Dla czerwonego koloru
        # Czerwony kolor jest od dla h=0:10 oraz h=160:180
        if h > 155 or h < 15:
            self.send_text.emit(color + " : H = " + str(h) + ", S = " + str(s) + ", V = " + str(v))
            if h < 15:
                color_lower = numpy.array([0, s-20, v-85], numpy.uint8)  # Dolny zakres koloru
                color_upper = numpy.array([h + 10, 255, 255], numpy.uint8)  # Górny zakres koloru

                color = "RedBottom"
                self.set_colors_range_in_ini_file(color, color_lower, color_upper)

                color_lower = numpy.array([160, s - 20, v - 85], numpy.uint8)  # Dolny zakres koloru
                color_upper = numpy.array([180, 255, 255], numpy.uint8)  # Górny zakres koloru

                color = "RedTop"
                self.set_colors_range_in_ini_file(color, color_lower, color_upper)

            if h > 155:
                color_lower = numpy.array([h - 10, s-20, v-85], numpy.uint8)  # Dolny zakres koloru
                color_upper = numpy.array([180, 255, 255], numpy.uint8)  # Górny zakres koloru

                color = color+"Top"
                self.set_colors_range_in_ini_file(color, color_lower, color_upper)

                color_lower = numpy.array([0, s - 20, v - 85], numpy.uint8)  # Dolny zakres koloru
                color_upper = numpy.array([10, 255, 255], numpy.uint8)  # Górny zakres koloru

                color = color + "Bottom"
                self.set_colors_range_in_ini_file(color, color_lower, color_upper)

        # Dla reszty kolorów
        else:
            color_lower = numpy.array([h - 10, s-20, v-85], numpy.uint8)  # Dolny zakres koloru
            color_upper = numpy.array([h + 10, 255, 255], numpy.uint8)  # Górny zakres koloru

            # Zapisanie wartości w pliku
            self.set_colors_range_in_ini_file(color, color_lower, color_upper)
            self.send_text.emit(color + " : H = " + str(h) + ", S = " + str(s) + ", V = " + str(v))
