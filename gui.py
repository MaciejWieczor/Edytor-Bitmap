import tkinter
from tkinter import filedialog
import PIL
from PIL import ImageTk
from PIL import Image
import sys
import os
import math
import statistics
import multiprocessing

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

        self.size = self.image.size             #tu już takie logiczne parametry
        self.width = self.size[0]+30            
        self.height = self.size[1]+30
        self.canvas = self.canvas_init()        #na końcu canvas na którym wyświetla
                                                #się obrazki

        self.undo_queue = []
        self.undo_queue.append(self.image)
        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor_x1 = 0
        self.cursor_y1 = 0
        self.cursor_mode = 0
        self.canvas_position_x = 0
        self.canvas_position_y = 0
        
    def window_init(self):      #inicjalizacja obiektu tkinter gui
        return tkinter.Tk()

    def image(self):    #ładuje image przez PIL z browseFiles
        image = PIL.Image.open(self.obrazek_name)
        return image        

    def canvas_init(self):  #inicjalizuje canvas na bazie rozmiaru zdjęcia
        sizee = max(self.size)+30
        canvas = tkinter.Canvas(self.window, width = sizee, height = sizee, highlightthickness=1, highlightbackground="black")
        return canvas   

    @staticmethod       #otwiera na windowsie okno dialogowe do znalezienia pliku jpg/jpeg/png/bmp i zwraca ten plik
    def browseFiles():
        filename = filedialog.askopenfilename(initialdir = "C:/Users/macie/Source/Repos/Edytor_bitmap",
                                              title = "Select a File",
                                              filetypes = (("JPGs",
                                                            "*.jpg*"),
                                                           ("JPEGs",
                                                            "*.jpeg*"),
                                                           ("PNGs",
                                                            "*.png*"),
                                                            ("BMPs",
                                                            "*.bmp*"),
                                                           ("all files",
                                                            "*.*")))
        print(filename)
        return filename       

    @staticmethod
    def reset():            # funkcja pozwala na wczytanie nowego zdjęcia 
        python = sys.executable
        os.execl(python, python, * sys.argv)            

    def save(self):     # funkcja pozwala na zapisania obecnego stanu zdjęcia do pliku jpg
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.image.save(filename)

    def resize(self, mod):      #funkcja do zmiany rozmiaru obrazu
        self.image = self.image.resize((int(self.size[0]*mod), int(self.size[1]*mod)))
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30

        self.undo_queue.append(self.image)

    def rotate(self, direction):    #wbudowana pythonowa funkcja do rotacji o 90 stopni 

        tmp = PIL.Image.new("RGB", (self.size[1], self.size[0]), 0)
        tmp_px = tmp.load()
        original_px = self.image.load()

        if(direction == "right"):
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):
                    tmp_px[self.size[1] - 1 - j, i] = original_px[i, j]

        elif(direction == "left"):
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):
                    tmp_px[j, self.size[0] - 1 - i] = original_px[i, j]

        self.image = tmp
        self.size = self.image.size
        self.width, self.height = self.height, self.width

        self.undo_queue.append(self.image)

    def undo(self):     #funkcja obsługująca listę ostatnich akcji na obrazie i pozwalająca cofać się  
                        #do poprzedniej wersji
        if(len(self.undo_queue) > 1):
            self.image = self.undo_queue[len(self.undo_queue) - 2]
            self.undo_queue.pop()
            self.size = self.image.size
            self.width = self.size[0]+30
            self.height = self.size[1]+30
        if(len(self.undo_queue) > 10):  # pamieta tylko 10 ostanich obrazow
            self.undo_queue.pop(0)

    def RGB_levels(self, R, G, B):      #zmienia składowe RGB pikseli (działa w skali od 0-2 (0 to czarne, 2 to pełny kolor))

        # kawałek kodu który dla włączonego trybu kursora zmniejsza range wykonania operacji z 
        #całego obrazu do tego wyznaczonego przez myszkę + LCtrl
        if (self.cursor_mode == 1):
            range_i = range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x)
            range_j = range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y)
        else:
            range_i = range(0, self.size[0])
            range_j = range(0, self.size[1])
        
        if(R <= 2 and G <= 2 and B <= 2):

            tmp = self.image.copy()
            px = tmp.load()        ##zwraca tablice krotek rgb, jak sie zmieni krotke, automatycznie sie zmieni pixel na self.image 
            for i in range_i:
                for j in range_j:
                    px[i,j] = (int(px[i,j][0] * R), int(px[i,j][1] * G), int(px[i,j][2] * B))
            self.undo_queue.append(tmp)
            self.image = tmp
         
    def median_filter(self, size):      #filtr medianowy - dość wolny - zmienia piksel na medianę wartości
                                        #pikseli dookoła w kwadracie o boku wielkość "size"

        tmp = self.image.copy()
        tmp_px = tmp.load()
        original_px = self.image.load()

        t = math.floor(size/2)
        R = []
        G = []
        B = []

        if (self.cursor_mode == 1):
            range_i = range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x)
            range_j = range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y)
        else:
            range_i = range(0, self.size[0])
            range_j = range(0, self.size[1])

        for i in range_i:
            for j in range_j:

                ##petle do ladowania wartosci z okna
                for x in range (0, size):
                    for y in range(0, size):
                        if(j + y <= self.size[1] and i + x <= self.size[0] and i - t + x >= 0 and j - t + y >= 0): ##warunki aby nie bralo wartosci z poza zdjecia
                            R.append(original_px[i - t + x, j - t + y][0])
                            G.append(original_px[i - t + x, j - t + y][1])
                            B.append(original_px[i - t + x, j - t + y][2])
                tmp_px[i, j] = (int(statistics.median(R)), int(statistics.median(G)), int(statistics.median(B)))
                R.clear()
                G.clear()
                B.clear()
        self.image = tmp
        self.undo_queue.append(self.image)
    
    def set_cursor_position(self, x, y, select):     #ustawia wartości self klasowe prostokąta który jest zaznaczany 
                                                     #przez myszkę + LCtrl w trybie kursora
        if(select == 0):
            self.cursor_x = x
            self.cursor_y = y
            print('Start = {} {}'.format(self.cursor_x, self.cursor_y))
        else:
            self.cursor_x1 = x
            self.cursor_y1 = y
            print('End = {} {}'.format(self.cursor_x1, self.cursor_y1))

    def contrast(self, desired_contrast):           #operacja zmieniająca kontrast zdjęcia w skali od -255 do 255

        if(desired_contrast <= 255 and desired_contrast >= -255):

            tmp = self.image.copy()
            px = tmp.load()

            if (self.cursor_mode == 1):
                range_i = range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x)
                range_j = range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y)
            else:
                range_i = range(0, self.size[0])
                range_j = range(0, self.size[1])

            F = 259*(desired_contrast + 255)/(255*(259 - desired_contrast))
            for i in range_i:
                for j in range_j:
                    px[i,j] = (int(F*(px[i,j][0]-128)+128), int(F*(px[i,j][1]-128)+128), int(F*(px[i,j][2]-128)+128))
        
            self.image = tmp
            self.undo_queue.append(self.image)
       
    def brightness(self, brightness):       #funkcja zmienia poziom jasności w skali od -255 do 255

        if(brightness <= 255 and brightness >= -255):

            tmp = self.image.copy()
            px = tmp.load()

            if (self.cursor_mode == 1):
                range_i = range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x)
                range_j = range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y)
            else:
                range_i = range(0, self.size[0])
                range_j = range(0, self.size[1])

        
            for i in range_i:
                for j in range_j:
                    px[i,j] = (int(px[i,j][0] + brightness), int(px[i,j][1] + brightness), int(px[i,j][2] + brightness))

            self.image = tmp
            self.undo_queue.append(self.image)

    def sharpening_filter(self, sharpening_force):      #macierzowa operacja wyostrzająca obraz z daną "siłą" wyostrzenia

        tmp = self.image.copy()
        px = tmp.load()
        original_px = self.image.load()

        if (self.cursor_mode == 1):
            range_i = range(self.cursor_x-20-self.canvas_position_x + 1, self.cursor_x1-20-self.canvas_position_x - 1)
            range_j = range(self.cursor_y-20-self.canvas_position_y + 1, self.cursor_y1-20-self.canvas_position_y - 1)
        else:
            range_i = range(1, self.size[0] - 1)
            range_j = range(1, self.size[1] - 1)

        kernel = [[0, -1 * sharpening_force, 0],[-1 * sharpening_force, 4 * sharpening_force + 1, -1 * sharpening_force],[0, -1 * sharpening_force, 0]]
        ##na dobra sprawe, ten kernel to jest identity kernel + kernel od szukania krawedzi, czyli znalezione krawedzie nakleja na obraz i jest 
        ##na swoj sposob wyostrzony w ten sposob

        ##liczenie splotu jadra ze zdjeciem
        for i in range_i:
            for j in range_j:
                tmp_R = 0
                tmp_G = 0
                tmp_B = 0
                for ik in range(-1, 2):
                    for jk in range(-1, 2):
                        tmp_R += kernel[ik + 1][jk + 1] * original_px[i + ik, j + jk][0]
                        tmp_G += kernel[ik + 1][jk + 1] * original_px[i + ik, j + jk][1]
                        tmp_B += kernel[ik + 1][jk + 1] * original_px[i + ik, j + jk][2]
                px[i,j] = (int(tmp_R), int(tmp_G), int(tmp_B))

        self.image = tmp
        self.undo_queue.append(self.image)

    def kernel_filters(self, type):     #grupa filtrów na bazie macierzy 3x3 (lub 5x5 dla jednego gaussian blura)
                                        #typ filtru przekazuje się jako argument funkcji 

        tmp = self.image.copy()
        px = tmp.load()
        original_px = self.image.load()

        ##wybor jadra
        if(type == "edge_detection_1"):
            kernel = [[1, 0, -1],[0, 0, 0],[-1, 0, 1]]
            ik_range = range(-1, 2)
            jk_range = range(-1, 2)
            t = 1

        elif(type == "edge_detection_2"):
            kernel = [[0, -1, 0],[-1, 4, -1],[0, -1, 0]]
            ik_range = range(-1, 2)
            jk_range = range(-1, 2)
            t = 1

        elif(type == "edge_detection_3"):
            kernel = [[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]]
            ik_range = range(-1, 2)
            jk_range = range(-1, 2)
            t = 1

        elif(type == "box_blur"):
            kernel = [[1/9, 1/9, 1/9],[1/9, 1/9, 1/9],[1/9, 1/9, 1/9]]
            ik_range = range(-1, 2)
            jk_range = range(-1, 2)
            t = 1

        elif(type == "gaussian_blur_3x3"):
            kernel = [[1/16, 2/16, 1/16],[2/16, 4/16, 2/16],[1/16, 2/16, 1/16]]
            ik_range = range(-1, 2)
            jk_range = range(-1, 2)
            t = 1

        elif(type == "gaussian_blur_5x5"):
            kernel = [[1/256, 4/256, 6/256, 4/256, 1/256],[4/256, 16/256, 24/256, 26/256, 4/256], [6/256, 24/256, 36/256, 24/256, 6/256], [4/256, 16/256, 24/256, 26/256, 4/256], [1/256, 4/256, 6/256, 4/256, 1/256]]
            ik_range = range(-2, 3)
            jk_range = range(-2, 3)
            t = 2

        ##tu mozna wiecej tych filtrow dodac, ale nie wiem czy jest sens, tez mi sie nie chcialo robic gaussowskiego filtru dla rozmiaru n


        if (self.cursor_mode == 1):
            range_i = range(self.cursor_x-20-self.canvas_position_x + t, self.cursor_x1-20-self.canvas_position_x - t)
            range_j = range(self.cursor_y-20-self.canvas_position_y + t, self.cursor_y1-20-self.canvas_position_y - t)
        else:
            range_i = range(t, self.size[0] - t)
            range_j = range(t, self.size[1] - t)


        ##liczenie splotu jadra ze zdjeciem
        for i in range_i:
            for j in range_j:
                tmp_R = 0
                tmp_G = 0
                tmp_B = 0
                for ik in ik_range:
                    for jk in jk_range:
                        tmp_R += kernel[ik + t][jk + t] * original_px[i + ik, j + jk][0]
                        tmp_G += kernel[ik + t][jk + t] * original_px[i + ik, j + jk][1]
                        tmp_B += kernel[ik + t][jk + t] * original_px[i + ik, j + jk][2]
                px[i,j] = (int(tmp_R), int(tmp_G), int(tmp_B))

        self.image = tmp
        self.undo_queue.append(self.image)
