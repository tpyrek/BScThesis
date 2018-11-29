import cv2
import numpy as np
import math
import configparser
from figures.figures_storage import Figure


# Definicje funkcji


# Funkcja pobiera zakres kolorów z pliku konfiguracyjnego z rozszerzeniem .ini i zwraca je w postaci tablic
# Jeśli nie ma danego zakresu w pliku (lub jeśli nie ma pliku) przypisywane są wartości defaultowe
def get_colors_range_from_ini_file():

    config_parser = configparser.ConfigParser()
    config_parser.read('colorsRange.ini')

    # Sprawdzam czy jest sekcja 'Blue' w pliku konfiguracyjnym
    if 'Blue' in config_parser:
        # Zakres koloru niebieskiego
        blue_lower = np.fromstring(config_parser['Blue']['Lower'],
                                   dtype=np.uint8, sep=',')  # Dolny zakres koloru niebieskiego
        blue_upper = np.fromstring(config_parser['Blue']['Upper'],
                                   dtype=np.uint8, sep=',')  # Górny zakres koloru niebieskiego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        blue_lower = np.array([90, 95, 100], np.uint8)        # Dolny zakres koloru niebieskiego
        blue_upper = np.array([125, 255, 255], np.uint8)     # Górny zakres koloru niebieskiego

    # Sprawdzam czy jest sekcja 'Green' w pliku konfiguracyjnym
    if 'Green' in config_parser:
        # Zakres koloru zielonego
        green_lower = np.fromstring(config_parser['Green']['Lower'],
                                    dtype=np.uint8, sep=',')   # Dolny zakres koloru zielonego
        green_upper = np.fromstring(config_parser['Green']['Upper'],
                                    dtype=np.uint8, sep=',')   # Górny zakres koloru zielonego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        green_lower = np.array([44, 54, 63], np.uint8)     # Dolny zakres koloru zielonego
        green_upper = np.array([71, 255, 255], np.uint8)     # Górny zakres koloru zielonego

    # Sprawdzam czy jest sekcja 'Yellow' w pliku konfiguracyjnym
    if 'Yellow' in config_parser:
        # Zakres koloru żółtego
        yellow_lower = np.fromstring(config_parser['Yellow']['Lower'],
                                     dtype=np.uint8, sep=',') # Dolny zakres koloru żółtego
        yellow_upper = np.fromstring(config_parser['Yellow']['Upper'],
                                     dtype=np.uint8, sep=',') # Górny zakres koloru żółtego
    # Jeśli nie ma takiej sekcji to defaultowy zakres
    else:
        yellow_lower = np.array([15, 50, 60], np.uint8)      # Dolny zakres koloru żółtego
        yellow_upper = np.array([35, 255, 255], np.uint8)    # Górny zakres koloru żółtego

    return blue_lower, blue_upper, green_lower, green_upper, yellow_lower, yellow_upper


# Funckja do wyszukiwania minimalnej wartości w tablicy
def find_min_in_list(tab: list):

    index = 0                           # Indeks najmniejszego elementu
    for i in range(0, len(tab)):         # Sprwadzam wszytskie elementy tablicy - zakładam, że pierwszy jest najmniejszy
        if tab[index] > tab[i]:         # Jeśli któryś kolejny mniejszy to jego indeks wstawiam do zmiennej index
            index = i

    return tab[index]                               # Zwracam najmniejszy element


# Funkcja, która szuka punktu o najbliższej współrzędnej y do punktu przecięcia osi biegnącej przez centroid z obwiednią
def find_close_point(cross_point, corner_points_tab):

    corner_points_tab_size = len(corner_points_tab)     # Wymiary tablicy - pierwszy wymiar to ilość wierszy

    difference_tab = []                   # Tablica różnic współrzędnych y
    index = 0                           # Indeks elementu w tablicy corner_points_tab który jest najbliżej cross-point

    for i in range(0, corner_points_tab_size):
        difference_tab.append(abs(cross_point[1]-corner_points_tab[i][1]))   # Dodanie elementu do tablicy

    difference_tab_min = find_min_in_list(difference_tab)

    for j in range(0, corner_points_tab_size):
        if difference_tab[j] == difference_tab_min:
            index = j

    return index            # Zwraca indeks elementu o najmniejszej różnicy współrzędnych


# Funkcja do szukania punktu przecięcia obwiedni figury z prostą biegnącą przez centroid
def find_cross_point(cx, c):
    c_size = c.shape                # c_size - wymaiarowość tablicy w tym przypadku będą 3 wartości
    cross_co_ordinates = []            # Tablica przechowująca współrzędne punktów przecięcia linii
    # biegnącaj przez centroid z konturami

    for i in range(0, c_size[0]):                        # Pierwszy element c_size bo to będzie ilość wierszy
        # [i][0][0] ponieważ [i] bo to numer wiersza a sprawdzam je po kolei,
        # [0] bo jest tylko jeden wymiar w tym przypadku, [0] bo badam współrzędną x
        if abs(cx - c[i][0][0]) < 1:
            cross_co_ordinates.append(tuple(c[i][0]))    # Dodanie współrzędnych do tablicy

    return min(cross_co_ordinates)                       # Zwraca współrzędne punktu o mniejszej wartości y


# Funkcja obliczająca kąt na podstawie współrzędnych 3 punktów
def calculate_angle(p1, p2, p3):
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
def delete_noise(thresh_frame):

    thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)
    thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)
    thresh_frame = cv2.erode(thresh_frame, None, iterations=1)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

    return thresh_frame


# Funkcja ta z wykorzystaniem innych znajduje skrajne punkty, szuka centroidu figury o danym kolorze,
# szuka punktu przecięcia się prostej biegnącej przez centroid z obwiednią,
# wyllicza kąt i ustawia odpowienie pola obiektu figure klasy figure
# figure - obiekt klasy figure któremu ustawiam pola
def calculate_and_set_figure_values(figure):


    # Cześć do szukania najbardziej wysuniętych punktów

    c = figure.contours     # Pobranie punktów konturu figury

    # Znalezienie najbardziej wysunietych punktów
    # Tutaj jest c[numer][0], nie dodaje numeru 3 wymiaru i
    # dzięki temu weźmie zarówno x jak i y a funkcja tuple przekształci to w następujacą postać : (x,y)
    ext_left = tuple(c[c[:, 0, 0].argmin()][0])
    ext_right = tuple(c[c[:, 0, 0].argmax()][0])
    ext_top = tuple(c[c[:, 0, 1].argmin()][0])
    ext_bot = tuple(c[c[:, 0, 1].argmax()][0])

    ex_points_tab=[]             # Tablica przechowująca skrajne punkty

    # Dodawanie punktów
    ex_points_tab.append(ext_left)
    ex_points_tab.append(ext_right)
    ex_points_tab.append(ext_top)
    ex_points_tab.append(ext_bot)

    # Dla zrozumienia c ma 3 wymiary [d1]:[d2]:[d3] :
    # d3 odpowiada za to czy mamy współrzędną x(to zero) czy współrzędną y(to jeden)
    # d2 to ilość kolumn tutaj, jest tylko jedna
    # d1 to ilośc wierszy i tutaj jest ich tyle ile punktów konturu znalazło

    figure.extremePoints = ex_points_tab      # Ustawienie skrajnych punktów figury

    # Koniec części szukania skrajnych punktów

    m = cv2.moments(c)            # Momenty obrazka

    # Wyliczanie współrzędnych centroidu
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    cx_cy = [cx, cy]                      # Współrzedne środka figury w postaci [x,y]
    figure.coordinates = cx_cy           # Ustawienie współrzędnych centroidu

    cross_point = find_cross_point(cx, c)  # Znalezienie punktu przeciecia prostej przechodzącej przez centroid z konturem
    figure.crossPoint = cross_point     # Ustawienie pola crossPoint w obiekcie klasy figure
    if cross_point:                     # Jeśli jest to licz kąt
        figure.angle = calculate_angle(cross_point, tuple([cx, cy]), ex_points_tab[find_close_point(cross_point, ex_points_tab)])


# Main function
def figures_process(figures_store, frame):

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)              # Konwersja prezentacji barw z RGB na HSV

    #Pobranie zakresów kolorów z pliku konfiguracyjnego
    blue_lower, blue_upper, green_lower, green_upper, yellow_lower, yellow_upper = get_colors_range_from_ini_file()

    blue = cv2.inRange(frame_hsv, blue_lower, blue_upper)         # Wyizolowanie koloru niebieskiego
    green = cv2.inRange(frame_hsv, green_lower, green_upper)      # Wyizolowanie koloru zielonego
    yellow = cv2.inRange(frame_hsv, yellow_lower, yellow_upper)   # Wyizolowanie koloru żółtego

    # Oddzielenie obrazu wykrytyh figur w kolorze niebieskim od reszty obrazu (obraz binarny)
    thresh_frame_blue = cv2.threshold(blue, 45, 255, cv2.THRESH_BINARY)[1]

    # Oddzielenie obrazu wykrytyh figur w kolorze zielonym od reszty obrazu (obraz binarny)
    thresh_frame_green = cv2.threshold(green, 45, 255, cv2.THRESH_BINARY)[1]

    # Oddzielenie obrazu wykrytyh figur w kolorze żółtym od reszty obrazu (obraz binarny)
    thresh_frame_yellow = cv2.threshold(yellow, 45, 255, cv2.THRESH_BINARY)[1]

    thresh_frame_blue = delete_noise(thresh_frame_blue)          # Usunięcie szumów z obrazka
    thresh_frame_green = delete_noise(thresh_frame_green)        # Usunięcie szumów z obrazka
    thresh_frame_yellow = delete_noise(thresh_frame_yellow)      # Usunięcie szumów z obrazka

    # Znalezienie konturów
    (check_blue, contours_blue, hierarchy_blue) = cv2.findContours(thresh_frame_blue.copy(),
                                                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (check_green, contours_green, hierarchy_green) = cv2.findContours(thresh_frame_green.copy(),
                                                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (check_yellow, contours_yellow, hierarchy_yellow) = cv2.findContours(thresh_frame_yellow.copy(),
                                                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Dodanie figur do magazynu
    # Numer figury ustawiam zgodnie z ilością figur, aby każda miała unikalny
    for i in range(0, len(contours_blue)):
        f = Figure(figures_store.quantity, 0, 0, "Blue", contours_blue[i], 0, None)
        figures_store.add_figure(f)

    for i in range(0, len(contours_green)):
        f = Figure(figures_store.quantity, 0, 0, "Green", contours_green[i], 0, None)
        figures_store.add_figure(f)

    for i in range(0, len(contours_yellow)):
        f = Figure(figures_store.quantity, 0, 0, "Yellow", contours_yellow[i], 0, None)
        figures_store.add_figure(f)

    for i in range(0, figures_store.quantity):
        calculate_and_set_figure_values(figures_store.figures[i])
