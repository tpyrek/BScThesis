import cv2
import numpy as np
import math
import configparser
import figuresStorage


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
        blueLower = np.array([90, 95, 100], np.uint8)        # Dolny zakres koloru niebieskiego
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
        greenLower = np.array([44, 54, 63], np.uint8)     # Dolny zakres koloru zielonego
        greenUpper = np.array([71, 255, 255], np.uint8)     # Górny zakres koloru zielonego

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

    if p3[0] == p1[0]:
        p3 = tuple([p3[0]-1, p3[1]])

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


# Main function
def figuresProcess(figuresStore, frame):

    #cv2.medianBlur(frame, frame, 3)

    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)              # Konwersja prezentacji barw z RGB na HSV

    #Pobranie zakresów kolorów z pliku konfiguracyjnego
    blueLower, blueUpper, greenLower, greenUpper, yellowLower, yellowUpper = getColorsRangeFromIniFile()

    blue = cv2.inRange(frameHSV, blueLower, blueUpper)         # Wyizolowanie koloru niebieskiego
    green = cv2.inRange(frameHSV, greenLower, greenUpper)      # Wyizolowanie koloru zielonego
    yellow = cv2.inRange(frameHSV, yellowLower, yellowUpper)   # Wyizolowanie koloru żółtego

    # Oddzielenie obrazu wykrytyh figur w kolorze niebieskim od reszty obrazu (obraz binarny)
    threshFrameBlue = cv2.threshold(blue, 45, 255, cv2.THRESH_BINARY)[1]

    # Oddzielenie obrazu wykrytyh figur w kolorze zielonym od reszty obrazu (obraz binarny)
    threshFrameGreen = cv2.threshold(green, 45, 255, cv2.THRESH_BINARY)[1]

    # Oddzielenie obrazu wykrytyh figur w kolorze żółtym od reszty obrazu (obraz binarny)
    threshFrameYellow = cv2.threshold(yellow, 45, 255, cv2.THRESH_BINARY)[1]

    threshFrameBlue = deleteNoise(threshFrameBlue)          # Usunięcie szumów z obrazka
    threshFrameGreen = deleteNoise(threshFrameGreen)        # Usunięcie szumów z obrazka
    threshFrameYellow = deleteNoise(threshFrameYellow)      # Usunięcie szumów z obrazka


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
        f = figuresStorage.Figure(figuresStore.quantity, 0, 0, "blue", contours_blue[i], 0, None)
        figuresStore.addFigure(f)


    for i in range(0,len(contours_green)):
        f = figuresStorage.Figure(figuresStore.quantity, 0, 0, "green", contours_green[i], 0, None)
        figuresStore.addFigure(f)

    for i in range(0, len(contours_yellow)):
        f = figuresStorage.Figure(figuresStore.quantity, 0, 0, "yellow", contours_yellow[i], 0, None)
        figuresStore.addFigure(f)


    for i in range(0,figuresStore.quantity):
        calculateAndSetFigureValues(figuresStore.figures[i])
