from PyQt5 import QtCore, QtGui
import cv2
import numpy
import configparser
from time import sleep

class openCVWorker(QtCore.QObject):

    # SYGNAŁY
    sendFrame = QtCore.pyqtSignal(QtGui.QImage)
    sendText = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        # Oryginalna pobrana klatka z kamery
        # numpy - odpowienik cv::Mat
        self.frameOriginal = numpy.zeros((480, 640, 1), dtype = "uint8")
        # Obrobiona klatka z kamery
        self.frameProcessed = numpy.zeros((480, 640, 1), dtype = "uint8")
        self.capture = cv2.VideoCapture()
        self.runThread = True


    # Funkcja dodająca kropkę na środku obrazu - ułatwienie kalibracji kolorów
    def processImage(self):

        width = int(self.capture.get(3))  # float
        height = int(self.capture.get(4))  # float

        center_point = [int(width / 2), int(height / 2)]  # Wyznaczenie środka (x,y)

        cv2.circle(self.frameProcessed, tuple(center_point), 10, (0, 0, 0), -1)

    # cameraDeviceNumber - numer uchwytu używany przez VideoCapture
    def receiveSetup(self, cameraDeviceNumber: int):
        # Start pobierania ramek
        self.capture.open(cameraDeviceNumber)


    def endGrabbing(self):
        if self.capture.isOpened():
            # Zwolnienie uchwytu kamery
            self.capture.release()

    # Główny wątek do pobierania klatek z kamery
    def receiveGrabFrame(self):

        while not self.capture.isOpened():
            pass

        while self.runThread:

            grabbed, self.frameOriginal = self.capture.read()

            if grabbed:

                width = int(self.capture.get(3))  # float
                height = int(self.capture.get(4))  # float

                self.frameProcessed = cv2.cvtColor(self.frameOriginal, cv2.COLOR_BGR2RGB)

                # Obróbka obrazu
                self.processImage()

                # Stworzenie QImage aby wyświetlić w polu QLabel
                qImage = QtGui.QImage(self.frameProcessed, width, height, QtGui.QImage.Format_RGB888)

                self.sendFrame.emit(qImage)

                sleep(0.001)

        self.endGrabbing()

    # Funkcja zapisuje podany zakres koloru w pliku konfiguracyjnym z rozszerzeniem .ini
    # color - String mówiący jaki kolor zapisać
    # colorLower - dolny zakres koloru
    # colorUpper - górny zakres koloru
    def setColorsRangeInIniFile(self, color, colorLower, colorUpper):

        # Usunięcie nawiasów kwadratowych z tablicy
        colorLower = ",".join(str(i) for i in colorLower)
        colorUpper = ",".join(str(i) for i in colorUpper)

        # Utworznie obiektu configpar
        configpar = configparser.ConfigParser()

        # Odczytanie pliku configuracyjnego oraz pobranie sekcji i wartości
        configpar.read('colorsRange.ini')

        # Sprawdza, czy sekcja która ma być zmieniona jest w pliku jak nie to tworzy ją
        if color not in configpar:
            configpar.add_section(color)

        # Ustawienie wartości dla wybranej sekcji color
        configpar.set(color, 'lower', str(colorLower))
        configpar.set(color, 'upper', str(colorUpper))

        # Wpisanie wartości do pliku
        # Jeśli nie będzie pliku o podanej nazwie to zostanie on stworzony
        with open('colorsRange.ini', 'w') as configfile:
            configpar.write(configfile)

    # Slot - Funkcja wywoływana przy naciśnieciu przycisku koloru w configurationGUI - pobiera kolory z kilku punktów
    # wokół środka oraz wylicza średnią dla lepszego przyblizenia koloru
    def getColorFromFrame(self, color:str):

        # Tablica do przechowania kolorów punktów z obrazu do wyliczenia średniej
        pointsTable = []

        width = int(self.capture.get(3))  # float
        height = int(self.capture.get(4))  # float

        center_point = [int(width / 2), int(height / 2)]  # Wyznaczenie środka (x,y)
        framehsv = cv2.cvtColor(self.frameOriginal, cv2.COLOR_BGR2HSV)  # Konwersja prezentacji barw z RGB na HSV

        # -5. -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
        # Pobranie kolorów punktu z kwadratu o boku 11 o środku w śroku przetwarzanego obrazu
        for i in range(-5, 6):
            for j in range(-5, 6):
                # Pobranie koloru z punktu o podanych współrzędnych (tutaj ze środka obrazu):
                # pierwsza to linie czyli y druga to kolomny czyli x
                # oraz wpisanie ich do tabeli
                pointsTable.append(framehsv[center_point[1] + j, center_point[0] + i])

        # Wartosci H, S, V reprezentacji barw
        h = 0
        s = 0
        v = 0

        # Obliczenie średniej dla lepszego przybliżenia barwy

        for points in pointsTable:
            h = h + points[0]
            s = s + points[1]
            v = v + points[2]

        h = int(h/len(pointsTable))
        s = int(s/len(pointsTable))
        v = int(v/len(pointsTable))

        colorLower = numpy.array([h - 10, 60, 70], numpy.uint8)  # Dolny zakres koloru
        colorUpper = numpy.array([h + 10, 255, 255], numpy.uint8)  # Górny zakres koloru

        # Zapisanie wartości w pliku
        self.setColorsRangeInIniFile(color, colorLower, colorUpper)
        self.sendText.emit(color + " : H = " + str(h) + ", S = " + str(s) + ", V = " + str(v))
