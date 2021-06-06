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

    def resize(self, mod):      #funkcja do zmiany rozmiaru - trochę do 
                                #poprawy bo kiepsko skaluje
        self.image = self.image.resize((int(self.size[0]*mod), int(self.size[1]*mod)))
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30

        self.undo_queue.append(self.image)

    def rotate(self, direction):

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

    def undo(self):
        if(len(self.undo_queue) > 1):
            self.image = self.undo_queue[len(self.undo_queue) - 2]
            self.undo_queue.pop()
            self.size = self.image.size
            self.width = self.size[0]+30
            self.height = self.size[1]+30
        if(len(self.undo_queue) > 10): # pamieta tylko 10 ostanich obrazow
            self.undo_queue.pop(0)

    def RGB_levels(self, R, G, B):
        if (self.cursor_mode == 0): #caly ekran
            if(R <= 2 and G <= 2 and B <= 2):

                tmp = self.image.copy()
                px = tmp.load()        ##zwaraca tablice krotek rgb, jak sie zmieni krotke, automatycznie sie zmieni pixel na self.image 

                for i in range(0, tmp.size[0]):
                    for j in range(0, tmp.size[1]):
                        px[i,j] = (int(px[i,j][0] * R), int(px[i,j][1] * G), int(px[i,j][2] * B))
                self.undo_queue.append(tmp)
                self.image = tmp
        if (self.cursor_mode == 1): #cursor mode
            if(R <= 2 and G <= 2 and B <= 2):

                tmp = self.image.copy()
                px = tmp.load()        ##zwaraca tablice krotek rgb, jak sie zmieni krotke, automatycznie sie zmieni pixel na self.image 

                for i in range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x):
                    for j in range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y):
                        px[i,j] = (int(px[i,j][0] * R), int(px[i,j][1] * G), int(px[i,j][2] * B))
                self.undo_queue.append(tmp)
                self.image = tmp

                
    def median_filter(self, size):

        tmp = PIL.Image.new("RGB", (self.size[0], self.size[1]), 0)
        tmp_px = tmp.load()
        original_px = self.image.load()

        t = math.floor(size/2)
        R = []
        G = []
        B = []

        if (self.cursor_mode == 0): #caly ekran
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):

                    ##petle to ladowania wartosci z okna
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
        if (self.cursor_mode == 1): #tylko kursor
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):
                    tmp_px[i, j] = (original_px[i,j][0] ,original_px[i,j][1],original_px[i,j][2])

                    ##petle to ladowania wartosci z okna
            for i in range(self.cursor_x-20-self.canvas_position_x, self.cursor_x1-20-self.canvas_position_x):
                for j in range(self.cursor_y-20-self.canvas_position_y, self.cursor_y1-20-self.canvas_position_y):
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
    
    def set_cursor_position(self, x, y, select):
        if(select == 0):
            self.cursor_x = x
            self.cursor_y = y
            print('Start = {} {}'.format(self.cursor_x, self.cursor_y))
        else:
            self.cursor_x1 = x
            self.cursor_y1 = y
            print('End = {} {}'.format(self.cursor_x1, self.cursor_y1))