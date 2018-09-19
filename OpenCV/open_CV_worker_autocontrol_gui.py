from PyQt5 import QtCore, QtGui
import cv2
import numpy
import figuresStorage
import figuresProcess
from time import sleep

class openCVWorker(QtCore.QObject):

    # SYGNAŁY
    sendFrame = QtCore.pyqtSignal(QtGui.QImage)

    # Sygnał emitowany w celu dodania figury do listy znalezionych figur w autocontrol
    sendFigureText = QtCore.pyqtSignal(str)


    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        # Orginal grabbed frame
        # numpy - equivalent of cv::Mat
        self.frameOriginal = numpy.zeros((480, 640, 1), dtype = "uint8")
        # Processed grabbed frame
        self.frameProcessed = numpy.zeros((480, 640, 1), dtype = "uint8")
        self.capture = cv2.VideoCapture()
        self.runThread = True
        self.highlightFigure = False

        # Magazyn do przechowywania znalezionych figur
        self.figuresStore = figuresStorage.FiguresStore()
        # Numer figury aktualnie wybranej z listy w oknie autocontrol
        self.selectedFigureNumber = None


    # Funkcja odpowiedzialna za podkreślanie figur na obrazie
    def processImage(self):

        if self.highlightFigure:
            if self.selectedFigureNumber != None:
                if(len(self.figuresStore.figures) != 0):
                    # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)
                    cv2.drawContours(self.frameProcessed, self.figuresStore.figures[self.selectedFigureNumber].contours,
                                 -1, (0, 0, 0), 2)

    # cameraDeviceNumber - numer uchwytu kamery
    def receiveSetup(self, cameraDeviceNumber: int):
        try:
            self.capture.open(cameraDeviceNumber)
        except:

            pass

    def receiveHighLightEnable(self):
        self.highlightFigure = not self.highlightFigure

    def endGrabbing(self):
        if self.capture.isOpened():
            # Zwolnienie uchwytu kamery
            self.capture.release()

    def clenVariables(self):
        self.figuresStore.clean()
        self.selectedFigureNumber = None

    def receiveGrabFrame(self):

        # Pobranie pierwszej klatki w celu znalezienia figur
        self.frameOriginal = cv2.imread('test4.png')
        figuresProcess.figuresProcess(self.figuresStore, self.frameOriginal)
        for fi in self.figuresStore.figures:
            self.sendFigureText.emit("Figura : " + str(fi.figureNumber) + ", Kolor : " + str(fi.color))

        while not self.capture.isOpened():
            pass

        while self.runThread:
            #grabbed, self.frameOriginal = self.capture.read()

            self.frameOriginal = cv2.imread('test4.png')  # Wczytanie obrazka

        #if True:#grabbed:

            width = int(self.capture.get(3))  # float
            height = int(self.capture.get(4))  # float


            self.frameProcessed = cv2.cvtColor(self.frameOriginal, cv2.COLOR_BGR2RGB)

            # Convert image
            self.processImage()

            # Create to QImage
            qImage = QtGui.QImage(self.frameProcessed, width, height, QtGui.QImage.Format_RGB888)

            self.sendFrame.emit(qImage)

            sleep(0.001)

        self.endGrabbing()
        self.clenVariables()

    def receiveSelectedFigureNumber(self, rowNumber):
        self.selectedFigureNumber = rowNumber