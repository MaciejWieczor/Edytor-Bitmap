import tkinter
from tkinter import filedialog
import PIL
from PIL import ImageTk
from PIL import Image
import sys
import os

class GUI:
    def __init__(self):
        self.window = self.window_init()
        self.obrazek_name = self.browseFiles()
        self.image = self.image()
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30
        self.canvas = self.canvas_init()
        
    def window_init(self):
        return tkinter.Tk()

    def image(self):
        image = PIL.Image.open(self.obrazek_name)
        return image

    def canvas_init(self):
        canvas = tkinter.Canvas(self.window, width = self.width, height = self.height, highlightthickness=1, highlightbackground="black")
        return canvas

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
        return filename

    @staticmethod
    def reset():
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def save(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.image.save(filename)

    def resize(self, mod):
        self.image = self.image.resize((int(self.width*mod), int(self.height*mod)))
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30
    
        