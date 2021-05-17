import tkinter
from tkinter import filedialog
import PIL
from PIL import ImageTk
from PIL import Image
import sys
import os

class GUI:
    def __init__(self):
        self.window = self.window_init()        #ramka do gui na której wszystko jest

        self.obrazek_name = self.browseFiles()  #path do zdjęcia

        self.image = self.image()               #obrazek w module PILLOW czyli można
                                                #choćby go zamieniać na array poprzez
                                                #numpy (funkcja asarray(self.image))
                                                #ten array ma wtedy wymiary
                                                #[linijka][piksel][rgb] z tego co 
                                                #rozumiem

        self.original_image = self.image        #oryginalny obrazek bez zmian

        self.size = self.image.size             #tu już takie logiczne parametry
        self.width = self.size[0]+30            
        self.height = self.size[1]+30
        self.canvas = self.canvas_init()        #na końcu canvas na którym wyświetla
                                                #się obrazki

        self.mod = 1.0                          #zmienna do skalowania, trzyma obecny rozmiar
        self.orientation = 0                     #obecna orientacja 0 = 0stopni, 1 = 90stopni, 2 = 180stopni 3 = 270stopni
        
        self.undo_list = [[self.mod, self.orientation]]

    def window_init(self):
        return tkinter.Tk()

    def image(self):
        image = PIL.Image.open(self.obrazek_name)
        return image         #ładuje image przez PIL z browseFiles

    def canvas_init(self):
        sizee = max(self.size)+30
        canvas = tkinter.Canvas(self.window, width = sizee, height = sizee, highlightthickness=1, highlightbackground="black")
        return canvas   #inicjalizuje canvas na bazie rozmiaru zdjęcia

    @staticmethod
    def browseFiles():
        filename = filedialog.askopenfilename(initialdir = "C:/Users/macie/Source/Repos/Edytor_bitmap",
                                              title = "Select a File",
                                              filetypes = (("JPGs",
                                                            "*.jpg*"),
                                                           ("all files",
                                                            "*.*")))
      
        # Change label contents
        print(filename)
        return filename       #handler przycisku wczytania pierwszego obrazka

    @staticmethod
    def reset():
        python = sys.executable
        os.execl(python, python, * sys.argv)             #handler przycisku wczytania nowego obrazka

    def save(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.image.save(filename)          #handler przycisku zapisania


    #ogolnie to zamysl jest taki, ze jezeli chcemy miec bezstratne transformacje, wykonywane na podstawie oryginalu
    #to wszystkie operacje trzeba wykonac od 0 po kolei, i w tym celu bedzie jakis wektor (albo pare zmiennych) stanu i jedna wielka funkcja ktora to wszystko wykona  
    #bo jak na przyklad zrobisz resize jak tutaj na oryginale to obroty stracisz, a poniewaz tylko kilka transformacji mamy miec, to moze takie cos da rade
    #jednak nwm jak to bedzie jak sie doda to wybieranie obszaru itp, najwyzej sie to zleje i zrobi lopatologicznie
    #na razie zrobie tak, ze funkcje wejsciowe zmieniaja parametry, i wywoluja jedna duza funkcje co wykona te transformacje


    def resize(self, mod):      #funkcja do zmiany rozmiaru - trochę do 
                                    #poprawy bo kiepsko skaluje
        self.mod = self.mod + mod
        self.__transformacja()

    def rotate(self, direction):
        if(direction == "right"):
            self.orientation -= 1
        elif(direction == "left"):
            self.orientation += 1
        if(self.orientation == -1):
            self.orientation = 3
        elif(self.orientation == 4):
            self.orientation = 0
        self.__transformacja()

    def undo(self):
        if(len(self.undo_list) > 1):

            self.mod = self.undo_list[len(self.undo_list) - 2][0]
            self.orientation = self.undo_list[len(self.undo_list) - 2][1]

            self.undo_list.pop()
            self.__transformacja()
            self.undo_list.pop()

    def __transformacja(self):
        
        wektor_zmian = []

        #skalowanie
        self.image = self.original_image.resize((int(self.original_image.size[0]*self.mod), int(self.original_image.size[1]*self.mod)))
        self.size = self.image.size
        
        wektor_zmian.append(self.mod)

        #obrot
        if(self.orientation == 1):
            self.image = self.image.transpose(Image.ROTATE_90)
        elif(self.orientation == 2):
            self.image = self.image.transpose(Image.ROTATE_180)
        elif(self.orientation == 3):
            self.image = self.image.transpose(Image.ROTATE_270)
        
        wektor_zmian.append(self.orientation)

        self.width = self.size[0]+30
        self.height = self.size[1]+30

        #zapisanie obrazka do pamieci
        self.undo_list.append(wektor_zmian)
        if(len(self.undo_list) > 5):     #na razie dam aby 5 ostatnich zmian pamietal
            self.undo_list.pop(0)

        print(len(self.undo_list))
