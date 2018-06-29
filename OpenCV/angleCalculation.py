import cv2
import numpy as np
import math
import configparser

# Definicje klas


# Klasa przechowuje dane jednej figury
class figure(object):
    def __init__(self, figureNumber, cxCy, angle, color, contours, crossPoint, extremePoints):
        self.figureNumber = figureNumber        # Ustawienie unikalnego numeru obiektu
        self.coordinates = cxCy                 # Ustawienie współrzędnych centroidu
        self.angle = angle                      # Ustawienie wartości kąta figury
        self.color = color                      # Ustawienie koloru figury
        self.contours = contours                # Ustawienie tablicy z punktami konturu
        self.crossPoint = crossPoint            # Ustawienie punktu przecięcia konturu i prostej przechodzącej
        # przez centroid
        self.extremePoints = extremePoints      # Ustawienie skrajnych punktów [lewy, prawy, góra, dół]


# Klasa przechowująca obiekty klasy figure
class figuresStore(object):

    def __init__(self):
        self.quantity = 0                       # Licznik figur
        self.figures = []                       # Tablica przechowująca obiekty klasy figure

    # Funkcja dodająca obiekt do magazynu
    def addFigure(self, figure):
        self.quantity+=1                        # Zwiększenie ilości figur o jeden
        self.figures.append(figure)             # Wpisanie do tabeli obiektu

    # Funkcja usuwająca obiekt z magazynu
    def deleteFigure(self, index):
        self.quantity-=1                        # Zmniejszenie ilości figur o jeden
        self.figures.pop(index)                 # Usunięcie obiektu z tabeli

# Definicje funkcji


# Funkcja pobiera zakres kolorów z pliku konfiguracyjnego z rozszerzeniem .ini i zwraca je w postaci tablic
# Jeśli nie ma danego zakresu w pliku (lub jeśli nie ma pliku) przypisywane są wartości defaultowe
def getColorsRangeFromIniFile():

    configpar = configparser.ConfigParser()
    configpar.read('colorsRange.ini')

    # Sprawdzam czy jest sekcja 'Blue' w pliku konfiguracyjnym
    if 'Blue' in configpar:
        # Zakres koloru niebieskiego
        blueLower = np.fromstring(configpar['Blue']['Lower'],
                                  dtype=np.uint8, sep=',') # Dolny zakres koloru niebieskiego
        blueUpper = np.fromstring(configpar['Blue']['Upper'],
                                  dtype=np.uint8, sep=',') # Górny zakres koloru niebieskiego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        blueLower = np.array([90, 30, 30], np.uint8)        # Dolny zakres koloru niebieskiego
        blueUpper = np.array([125, 255, 255], np.uint8)     # Górny zakres koloru niebieskiego

    # Sprawdzam czy jest sekcja 'Green' w pliku konfiguracyjnym
    if 'Green' in configpar:
        # Zakres koloru zielonego
        greenLower = np.fromstring(configpar['Green']['Lower'],
                                   dtype=np.uint8, sep=',')   # Dolny zakres koloru zielonego
        greenUpper = np.fromstring(configpar['Green']['Upper'],
                                   dtype=np.uint8, sep=',')   # Górny zakres koloru zielonego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        greenLower = np.array([50, 120, 140], np.uint8)     # Dolny zakres koloru zielonego
        greenUpper = np.array([65, 255, 255], np.uint8)     # Górny zakres koloru zielonego

    # Sprawdzam czy jest sekcja 'Yellow' w pliku konfiguracyjnym
    if 'Yellow' in configpar:
        # Zakres koloru żółtego
        yellowLower = np.fromstring(configpar['Yellow']['Lower'],
                                    dtype=np.uint8, sep=',') # Dolny zakres koloru żółtego
        yellowUpper = np.fromstring(configpar['Yellow']['Upper'],
                                    dtype=np.uint8, sep=',') # Górny zakres koloru żółtego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        yellowLower = np.array([15, 50, 60], np.uint8)      # Dolny zakres koloru żółtego
        yellowUpper = np.array([35, 255, 255], np.uint8)    # Górny zakres koloru żółtego


    return (blueLower, blueUpper, greenLower, greenUpper, yellowLower, yellowUpper)


# Funckja do wyszukiwania minimalnej wartości w tablicy
def findMin(tab):

    index = 0                           # Indeks najmniejszego elementu
    for i in range(0,len(tab)):         # Sprwadzam wszytskie elementy tablicy - zakładam, że pierwszy jest najmniejszy
        if tab[index] > tab[i]:         # Jeśli któryś kolejny mniejszy to jego indeks wstawiam do zmiennej index
            index = i

    return tab[index]                               # Zwracam najmniejszy element


# Funkcja, która szuka punktu o najbliższej współrzędnej y do punktu przecięcia osi biegnącej przez centroid z obwiednią
def findClosePoint(cross_point, cornerpointstab):

    cornerpointstab_size = len(cornerpointstab)     # Wymiary tablicy - pierwszy wymiar to ilość wierszy

    difference_tab=[]                   # Tablica różnic współrzędnych y
    index = 0                           # Indeks elementu w tablicy cornerpointstab który jest najbliżej cross-point

    for i in range(0,cornerpointstab_size):
        difference_tab.append(abs(cross_point[1]-cornerpointstab[i][1]))   # Dodanie elementu do tablicy

    difference_tab_min = findMin(difference_tab)

    for j in range(0,cornerpointstab_size):
        if difference_tab[j] == difference_tab_min:
            index = j

    return index            # Zwraca indeks elementu o najmniejszej różnicy współrzędnych


# Funkcja do szukania punktu przecięcia obwiedni figury z prostą biegnącą przez centroid
def findCrossPoint(cx,c):
    c_size = c.shape                # c_size - wymaiarowość tablicy w tym przypadku będą 3 wartości
    crossCo_ordinates=[]            # Tablica przechowująca współrzędne punktów przecięcia linii
    # biegnącaj przez centroid z konturami

    for i in range(0,c_size[0]):                        # Pierwszy element c_size bo to będzie ilość wierszy
        # [i][0][0] ponieważ [i] bo to numer wiersza a sprawdzam je po kolei,
        # [0] bo jest tylko jeden wymiar w tym przypadku, [0] bo badam współrzędną x
        if abs(cx - c[i][0][0]) < 1:
            crossCo_ordinates.append(tuple(c[i][0]))    # Dodanie współrzędnych do tablicy

    return min(crossCo_ordinates)                       # Zwraca współrzędne punktu o mniejszej wartości y


# Funkcja obliczająca kąt na podstawie współrzędnych 3 punktów
def calculateAngle(p1, p2, p3):
    # p1 to punkt wspólny - cross-point
    # p2 to centroid
    # p3 to jeden z wierzchołków

    delta_x_p2 = p2[0]-p1[0]
    delta_y_p2 = p2[1]-p1[1]

    # Sprawdzam czy współrzędna x wierzchołka jest większa czy mniejsza od współrzędnej x cross-pointa i
    # zależnie od tego czy większe czy mniejsze wyliczam kąty

    if p3[0] < p1[0]:
        fi1 = math.atan(delta_y_p2/delta_x_p2) * 57.29577951308     # Pierwszy kąt w stopniach
    if p3[0] > p1[0]:
        fi1 = math.atan(delta_x_p2 / delta_y_p2) * 57.29577951308   # Pierwszy kąt w stopniach

    delta_x_p3 = p3[0] - p1[0]
    delta_y_p3 = p3[1] - p1[1]

    if p3[0] < p1[0]:
        fi2 = math.atan(delta_y_p3 / delta_x_p3) * 57.29577951308   # Drugi kąt w stopniach
    if p3[0] > p1[0]:
        fi2 = math.atan(delta_x_p3 / delta_y_p3) * 57.29577951308   # Drugi kąt w stopniach

    return round(fi1-fi2, 1)


# Usuwanie szumu z obrazka (erozja, dylatacja)
def deleteNoise(threshframe):

    threshframe = cv2.erode(threshframe, None, iterations=1)
    threshframe = cv2.dilate(threshframe, None, iterations=1)
    threshframe = cv2.erode(threshframe, None, iterations=1)
    threshframe = cv2.dilate(threshframe, None, iterations=1)
    threshframe = cv2.erode(threshframe, None, iterations=1)
    threshframe = cv2.dilate(threshframe, None, iterations=1)

    return threshframe


# Funkcja ta z wykorzystaniem innych znajduje skrajne punkty, szuka centroidu figury o danym kolorze,
# szuka punktu przecięcia się prostej biegnącej przez centroid z obwiednią,
# wyllicza kąt i ustawia odpowienie pola obiektu figure klasy figure
# figure - obiekt klasy figure któremu ustawiam pola
def calculateAndSetFigureValues(figure):


    # Cześć do szukania najbardziej wysuniętych punktów

    c = figure.contours     # Pobranie punktów konturu figury

    # Znalezienie najbardziej wysunietych punktów
    # Tutaj jest c[numer][0], nie dodaje numeru 3 wymiaru i
    # dzięki temu weźmie zarówno x jak i y a funkcja tuple przekształci to w następujacą postać : (x,y)
    extLeft = tuple(c[c[:, 0, 0].argmin()][0])
    extRight = tuple(c[c[:, 0, 0].argmax()][0])
    extTop = tuple(c[c[:, 0, 1].argmin()][0])
    extBot = tuple(c[c[:, 0, 1].argmax()][0])

    expointstab=[]             # Tablica przechowująca skrajne punkty

    # Dodawanie punktów
    expointstab.append(extLeft)
    expointstab.append(extRight)
    expointstab.append(extTop)
    expointstab.append(extBot)

    # Dla zrozumienia c ma 3 wymiary [d1]:[d2]:[d3] :
    # d3 odpowiada za to czy mamy współrzędną x(to zero) czy współrzędną y(to jeden)
    # d2 to ilość kolumn tutaj, jest tylko jedna
    # d1 to ilośc wierszy i tutaj jest ich tyle ile punktów konturu znalazło

    figure.extremePoints = expointstab      # Ustawienie skrajnych punktów figury

    # Koniec części szukania skrajnych punktów


    M = cv2.moments(c)            # Momenty obrazka

    # Wyliczanie współrzędnych centroidu
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cxcy = [cx,cy]                      # Współrzedne środka figury w postaci [x,y]
    figure.coordinates = cxcy           # Ustawienie współrzędnych centroidu

    cross_point = findCrossPoint(cx,c)  # Znalezienie punktu przeciecia prostej przechodzącej przez centroid z konturem
    figure.crossPoint = cross_point     # Ustawienie pola crossPoint w obiekcie klasy figure
    if cross_point:                     # Jeśli jest to licz kąt
        figure.angle = calculateAngle(cross_point, tuple([cx, cy]), expointstab[findClosePoint(cross_point,expointstab)])


lineThickness = 2                                    # Grubość linii
figuresstore = figuresStore()                        # Instancja klasy figures store - magazyn dla znalezionych figur

#im = cv2.imread('zdjecie.jpg')                          # Wczytanie obrazka
im = cv2.imread('test3.png')                            # Wczytanie obrazka
height, width, channels = im.shape                      # Zczytanie danych takich jak wysokość i szerokosć z obrazka
imhsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)              # Konwersja prezentacji barw z RGB na HSV

#Pobranie zakresów kolorów z pliku konfiguracyjnego
blueLower, blueUpper, greenLower, greenUpper, yellowLower, yellowUpper = getColorsRangeFromIniFile()

blue = cv2.inRange(imhsv, blueLower, blueUpper)         # Wyizolowanie koloru niebieskiego
green = cv2.inRange(imhsv, greenLower, greenUpper)      # Wyizolowanie koloru zielonego
yellow = cv2.inRange(imhsv, yellowLower, yellowUpper)   # Wyizolowanie koloru żółtego

# Oddzielenie obrazu wykrytyh figur w kolorze niebieskim od reszty obrazu (obraz binarny)
threshFrameBlue = cv2.threshold(blue, 45, 255, cv2.THRESH_BINARY)[1]

# Oddzielenie obrazu wykrytyh figur w kolorze zielonym od reszty obrazu (obraz binarny)
threshFrameGreen = cv2.threshold(green, 45, 255, cv2.THRESH_BINARY)[1]

# Oddzielenie obrazu wykrytyh figur w kolorze żółtym od reszty obrazu (obraz binarny)
threshFrameYellow = cv2.threshold(yellow, 45, 255, cv2.THRESH_BINARY)[1]

threshFrameBlue = deleteNoise(threshFrameBlue)          # Usunięcie szumów zo obrazka
threshFrameGreen = deleteNoise(threshFrameGreen)        # Usunięcie szumów zo obrazka
threshFrameYellow = deleteNoise(threshFrameYellow)      # Usunięcie szumów zo obrazka

# Znalezienie konturów
(check_blue, contours_blue, hierarchy_blue) = cv2.findContours(threshFrameBlue.copy(),
                                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
(check_green, contours_green, hierarchy_green) = cv2.findContours(threshFrameGreen.copy(),
                                                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
(check_yellow, contours_yellow, hierarchy_yellow) = cv2.findContours(threshFrameYellow.copy(),
                                                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Dodanie figur do magazynu
# Numer figury ustawiam zgodnie z ilością figur, aby każda miała unikalny
for i in range(0,len(contours_blue)):
    f = figure(figuresstore.quantity, 0, 0, "blue", contours_blue[i], 0, None)
    figuresstore.addFigure(f)

for i in range(0,len(contours_green)):
    f = figure(figuresstore.quantity, 0, 0, "green", contours_green[i], 0, None)
    figuresstore.addFigure(f)

for i in range(0, len(contours_yellow)):
    f = figure(figuresstore.quantity, 0, 0, "yellow", contours_yellow[i], 0, None)
    figuresstore.addFigure(f)

cv2.drawContours(im, contours_blue, -1, (0, 0, 0), 2)    # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)
cv2.drawContours(im, contours_green, -1, (0, 0, 0), 2)   # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)
cv2.drawContours(im, contours_yellow, -1, (0, 0, 0), 2)  # Rysowanie konturów (argumrnt -1 : rysuje wszytskie kontury)

for i in range(0,figuresstore.quantity):
    calculateAndSetFigureValues(figuresstore.figures[i])

    # Rysowanie lini przechodzącej przez centroid
    cv2.line(im, (figuresstore.figures[i].coordinates[0], 0), (figuresstore.figures[i].coordinates[0], height),
             (0, 0, 0), lineThickness)

    # Rysowanie kropki na punkcie przecięcia obwiedni i linii przechodzącej przez centroid
    cv2.circle(im, figuresstore.figures[i].crossPoint, 7, (0, 0, 255), -1)

    # Umieszczenie kropki przedstawiającej środek figury
    cv2.circle(im, (figuresstore.figures[i].coordinates[0], figuresstore.figures[i].coordinates[1]),
               7, (255, 255, 255), -1)

# Blok odpowiedzialny za stworzenie czarnego obrazu i naniesienie na danych figury
blank_image = np.zeros((height,width,3), np.uint8)      # Stworzenie czarnego obrazu

for i in range(0,figuresstore.quantity):
    cv2.putText(blank_image, str(str(figuresstore.figures[i].figureNumber)+" " +figuresstore.figures[i].color +" : "
                                 + str(figuresstore.figures[i].angle)), # Umieszczenie napisu na obrazku
                    (figuresstore.figures[i].coordinates[0]+5,
                     figuresstore.figures[i].coordinates[1]),       # Współrzędne lewej dolnej częsci tekstu
                    cv2.FONT_HERSHEY_SIMPLEX,                       # Czcionka
                    1,                                              # Wielkość czcionki
                    (255, 255, 255),                                # Kolor tekstu
                    1)                                              # Grubość

    cv2.circle(blank_image,(figuresstore.figures[i].coordinates[0],figuresstore.figures[i].coordinates[1]),
               7, (255, 255, 255), -1)  # Umieszczenie kropki przedstawiającej środek figury
    # Rysowanie skrajnych punktów
    cv2.circle(blank_image, figuresstore.figures[i].extremePoints[0], 8, (130, 130, 130), -1)
    cv2.circle(blank_image, figuresstore.figures[i].extremePoints[1], 8, (130, 130, 130), -1)
    cv2.circle(blank_image, figuresstore.figures[i].extremePoints[2], 8, (130, 130, 130), -1)
    cv2.circle(blank_image, figuresstore.figures[i].extremePoints[3], 8, (130, 130, 130), -1)

# Koniec bloku

cv2.imshow("Punkty", blank_image)                       # Wyświetlenie obrazu
cv2.imshow("PNG", im)                                   # Otworzenie okna z obrazkiem


if cv2.waitKey(0) & 0xff == 27:                         # Zamkniecie krzyżykiem lub klawiszem ESC
    cv2.destroyAllWindows()

