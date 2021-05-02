import tkinter
import PIL
from PIL import ImageTk

class GUI:
    def __init__(self, obrazek_name):
        self.window = self.window_init()
        self.obrazek = obrazek_name
        self.image = self.image_param()
        self.size = self.image.size
        self.width = self.size[0]+30
        self.height = self.size[1]+30
        
    def window_init(self):
        return tkinter.Tk()

    def image_param(self):
        image = PIL.Image.open(self.obrazek)
        return image

    def canvas_init(self):
        canvas = tkinter.Canvas(self.window, width = self.width, height = self.height)
        canvas.pack()
        return canvas


