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

        self.size = self.image.size             #tu już takie logiczne parametry
        self.width = self.size[0]+30            
        self.height = self.size[1]+30
        self.canvas = self.canvas_init()        #na końcu canvas na którym wyświetla
                                                #się obrazki

        self.undo_queue = []
        self.undo_queue.append(self.image)
        
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
        self.image = self.image.resize((int(self.width*mod), int(self.height*mod)))
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30

        self.undo_queue.append(self.image)

    def rotate(self, direction):
        if(direction == "right"):
            self.image = self.image.transpose(Image.ROTATE_270)
        elif(direction == "left"):
            self.image = self.image.transpose(Image.ROTATE_90)
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
        
        if(R <= 2 and G <= 2 and B <= 2):
            px = self.image.load()        ##zwaraca tablice krotek rgb, jak sie zmieni krotke, automatycznie sie zmieni pixel na self.image 

            print(R, G, B)

            for i in range(0, self.image.size[0]):
                for j in range(0, self.image.size[1]):
                    px[i,j] = (int(px[i,j][0] * R), int(px[i,j][1] * G), int(px[i,j][2] * B))