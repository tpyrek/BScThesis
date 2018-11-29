# Klasa przechowuje dane jednej figury
class Figure(object):
    def __init__(self, figure_number=None, cx_cy=None, angle=None, color=None, contours=None,
                 cross_point=None, extreme_points=None):
        self.figure_number = figure_number        # Ustawienie unikalnego numeru obiektu
        self.coordinates = cx_cy                 # Ustawienie współrzędnych centroidu
        self.angle = angle                      # Ustawienie wartości kąta figury
        self.color = color                      # Ustawienie koloru figury
        self.contours = contours                # Ustawienie tablicy z punktami konturu
        self.cross_point = cross_point            # Ustawienie punktu przecięcia konturu i prostej przechodzącej
        # przez centroid
        self.extreme_points = extreme_points      # Ustawienie skrajnych punktów [lewy, prawy, góra, dół]


# Klasa przechowująca obiekty klasy figure
class FiguresStore(object):

    def __init__(self):
        self.quantity = 0                       # Licznik figur
        self.figures = []                       # Tablica przechowująca obiekty klasy figure

    # Funkcja dodająca obiekt do magazynu
    def add_figure(self, figure):
        self.quantity += 1                        # Zwiększenie ilości figur o jeden
        self.figures.append(figure)             # Wpisanie do tabeli obiektu

    # Funkcja usuwająca obiekt z magazynu
    def delete_figure(self, index):
        self.quantity -= 1                        # Zmniejszenie ilości figur o jeden
        self.figures.pop(index)                 # Usunięcie obiektu z tabeli

    def clean(self):
        self.quantity = 0
        self.figures.clear()
