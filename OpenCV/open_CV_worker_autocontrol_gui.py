from PyQt5 import QtCore, QtGui
import cv2
import numpy
import figuresStorage
import figuresProcess
import wait_for_camera_to_be_set
from time import sleep
import threading
import configparser

class openCVWorker(QtCore.QObject):

    # SYGNAŁY
    sendFrame = QtCore.pyqtSignal(QtGui.QImage)

    # Sygnał emitowany w celu dodania figury do listy znalezionych figur w autocontrol
    sendFigureText = QtCore.pyqtSignal(str)
    sendFigureData = QtCore.pyqtSignal(str)
    sendFigureDataTextClear = QtCore.pyqtSignal()
    sendCameraSet = QtCore.pyqtSignal()


    def __init__(self, sendDataToServosController, parent=None):
        QtCore.QObject.__init__(self, parent)

        # Oryginalny pobrany obraz
        # numpy - equivalent of cv::Mat
        self.frameOriginal = numpy.zeros((480, 640, 1), dtype = "uint8")
        # Przerobiony pobrany obraz
        self.frameProcessed = numpy.zeros((480, 640, 1), dtype = "uint8")
        self.capture = cv2.VideoCapture()
        self.runThread = True
        self.highlightFigure = False
        self.redLowerBottom, self.redUpperBottom, self.redLowerTop, self.redUpperTop = self.getRedColorFromIniFile()

        # Po wykonaniu akcji przez servosController zostaje wyemitowany sygnał do odświeżenia figur znajdujacych
        # sie na polu
        self.sendDataToServosController = sendDataToServosController
        # Magazyn do przechowywania znalezionych figur
        self.figuresStore = figuresStorage.FiguresStore()
        # Numer figury aktualnie wybranej z listy w oknie autocontrol
        self.selectedFigureNumber = None
        # Czekanie aż kamera ustawi sobie jasnośc i ostrość
        self.cameraWaiter = wait_for_camera_to_be_set.waitForCameraToBeSet()

        # Zmiana wartości na true po odczekaniu aż kamera ustawi jasność i ostrość
        self.cameraSet = False

        #Połączenie sygnałów ze slotami
        self.sendDataToServosController.sendStatus.connect(self.getFigures)
        self.cameraWaiter.sendCameraSet.connect(self.receiveCameraSet)

    def getRedColorFromIniFile(self):

        configpar = configparser.ConfigParser()
        configpar.read('colorsRange.ini')

        # Sprawdzam czy jest sekcja 'RedBottom' w pliku konfiguracyjnym
        if 'RedBottom' in configpar:
            # Zakres koloru niebieskiego
            redLowerBottom = numpy.fromstring(configpar['RedBottom']['Lower'],
                                              dtype=numpy.uint8, sep=',')  # Dolny zakres koloru niebieskiego
            redUpperBottom = numpy.fromstring(configpar['RedBottom']['Upper'],
                                              dtype=numpy.uint8, sep=',')  # Górny zakres koloru niebieskiego
        # Jeśli nie ma takiej sekcji to defaultowy zakres
        else:
            redLowerBottom = numpy.array([0, 150, 150], numpy.uint8)  # Dolny zakres koloru czerwonego
            redUpperBottom = numpy.array([10, 255, 255], numpy.uint8)  # Górny zakres koloru czerwonego

        # Sprawdzam czy jest sekcja 'RedTop' w pliku konfiguracyjnym
        if 'RedTop' in configpar:
            # Zakres koloru niebieskiego
            redLowerTop= numpy.fromstring(configpar['RedTop']['Lower'],
                                              dtype=numpy.uint8, sep=',')  # Dolny zakres koloru niebieskiego
            redUpperTop = numpy.fromstring(configpar['RedTop']['Upper'],
                                              dtype=numpy.uint8, sep=',')  # Górny zakres koloru niebieskiego
        # Jeśli nie ma takiej sekcji to defaultowy zakres
        else:
            redLowerTop = numpy.array([160, 150, 150], numpy.uint8)  # Dolny zakres koloru czerwonego
            redUpperTop = numpy.array([180, 255, 255], numpy.uint8)  # Górny zakres koloru czerwonego

        return(redLowerBottom, redUpperBottom, redLowerTop, redUpperTop)

    def robotArmPointer(self):
        # Znajdywanie czerwonego znacznika na obrazie oraz wypisanie jego współrzędnych

        frameHSV = cv2.cvtColor(self.frameOriginal, cv2.COLOR_BGR2HSV)

        redBottom = cv2.inRange(frameHSV, self.redLowerBottom, self.redUpperBottom)  # Wyizolowanie koloru czerwonego
        redTop = cv2.inRange(frameHSV, self.redLowerTop, self.redUpperTop)  # Wyizolowanie koloru czerwonego

        red = redBottom | redTop

        # Oddzielenie obrazu wykrytyh figur w kolorze czerwonym od reszty obrazu (obraz binarny)
        threshframe = cv2.threshold(red, 45, 255, cv2.THRESH_BINARY)[1]

        # Oczyszczenie obrazu
        threshframe = cv2.erode(threshframe, None, iterations=1)
        threshframe = cv2.dilate(threshframe, None, iterations=1)
        threshframe = cv2.erode(threshframe, None, iterations=1)
        threshframe = cv2.dilate(threshframe, None, iterations=1)
        threshframe = cv2.erode(threshframe, None, iterations=1)
        threshframe = cv2.dilate(threshframe, None, iterations=1)

        (check_red, contours_red, hierarchy_red) = cv2.findContours(threshframe.copy(),
                                                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Jeśli została znaleziona jakaś czerwona barwa
        if len(contours_red) != 0:
            M = cv2.moments(contours_red[0])  # Momenty obrazka

            # Wyliczanie współrzędnych centroidu
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            center_point = [cx, cy]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.frameProcessed, str(center_point), (cx+5, cy), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.circle(self.frameProcessed, tuple(center_point), 4, (0, 0, 0), -1)

    # Funkcja odpowiedzialna za podkreślanie figur na obrazie i zaznaczanie czerwonego znacznika
    def processImage(self):

        if self.cameraSet:
            self.robotArmPointer()

        if self.highlightFigure:
            if self.selectedFigureNumber != None:
                if(len(self.figuresStore.figures) != 0):
                    # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)
                    cv2.drawContours(self.frameProcessed, self.figuresStore.figures[self.selectedFigureNumber].contours,
                                 -1, (0, 0, 0), 2)
                    cv2.circle(self.frameProcessed,
                               tuple(self.figuresStore.figures[self.selectedFigureNumber].coordinates),4, (0, 0, 0), -1)

    # cameraDeviceNumber - numer uchwytu kamery
    def receiveSetup(self, cameraDeviceNumber: int):
        self.capture.open(cameraDeviceNumber)

    def receiveHighLightEnable(self):
        self.highlightFigure = not self.highlightFigure

    def endGrabbing(self):
        if self.capture.isOpened():
            # Zwolnienie uchwytu kamery
            self.capture.release()

    def clenVariables(self):
        self.figuresStore.clean()
        self.selectedFigureNumber = None

    # Główna pętla
    def receiveGrabFrame(self):

        while not self.capture.isOpened():
            pass

        # Wątek który w tle odczeka pewną ilość czasu aby kamera zdazyła dostosować się do jassnosci otoczenia
        # i wyemituje sygnał
        cameraSetThread = threading.Thread(target=self.cameraWaiter.waitForCamera)
        # Daemon thread zostanie zabity automatycznie przy zamknięciu aplikacji
        cameraSetThread.daemon = True
        cameraSetThread.start()

        while self.runThread:

            grabbed, self.frameOriginal = self.capture.read()

            if grabbed:

                width = int(self.capture.get(3))  # float
                height = int(self.capture.get(4))  # float

                self.frameProcessed = cv2.cvtColor(self.frameOriginal, cv2.COLOR_BGR2RGB)

                # Przeróbka obrazu
                self.processImage()

                # Stworzenie QImage
                qImage = QtGui.QImage(self.frameProcessed, width, height, QtGui.QImage.Format_RGB888)

                self.sendFrame.emit(qImage)

                sleep(0.001)

        self.endGrabbing()
        self.clenVariables()
        self.cameraSet = False

    def receiveSelectedFigureNumber(self, rowNumber):
        if rowNumber != -1:
            self.selectedFigureNumber = rowNumber
            self.sendFigureData.emit("Numer : " + str(self.figuresStore.figures[self.selectedFigureNumber].figureNumber)
                                     + "\nKolor : "
                                     + str(self.figuresStore.figures[self.selectedFigureNumber].color)
                                     + "\nŚrodek : "
                                     + str(self.figuresStore.figures[self.selectedFigureNumber].coordinates)
                                     + "\nKąt : "
                                     + str(self.figuresStore.figures[self.selectedFigureNumber].angle))

    def getFigures(self):
        self.clenVariables()
        self.sendFigureDataTextClear.emit()
        figuresProcess.figuresProcess(self.figuresStore, self.frameOriginal)
        for fi in self.figuresStore.figures:
            self.sendFigureText.emit("Figura : " + str(fi.figureNumber) + ", Kolor : " + str(fi.color))

    def receiveCameraSet(self):
        self.cameraSet = True
        self.getFigures()


