import tkinter as tk
from PIL import ImageTk
from PIL import Image
from gui import GUI
from numpy import asarray
from functools import partial

print("Program rozpoczęty")
root = GUI()

#powyżej ustalane są wszystkie parametry czyli:
#wczytywane jest zdjęcie do obiektu root, ustalana
#jest ramka root.window do której przyciski itp są 
#przyczepione oraz tworzony jest canvas czyli pole
#na którym wyświetlany będzie obrazek (canvas ma 
#rozmiar jak oryginalna rozdzielczość obrazka
#plus trzydzieści pikseli)

root.canvas.pack()  #wywołanie canvas w tkinterowym gui
img = ImageTk.PhotoImage(root.image)    #zapisanie obrazu z klasy GUI do zmiennej 
image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)   #wywołanie zmiennej na canvas
cursor_mode = tk.IntVar()   #zmienna czytająca checkbox dotyczący trybu operacji
cursor_lock = False         #inicjalizacja flip flopa przy zmianie trybów operacji
x = 0                       #inicjializacja pozycji kursora 
y = 0
size_var = 4        #domyślna wartość szerokości okna filtru medianowego
param_255_var = 0     #domyślna wartość parametru 0-255
slider_var_R = 1      #domyślna wartość na sliderze
slider_var_G = 1      #domyślna wartość na sliderze
slider_var_B = 1      #domyślna wartość na sliderze

#funkcje poniżej są do przycisków zdefiniowanych na dole 

#funkcje zdefiniowałem poniżej bo 
#1. używają obiektu
#2. call funkcji która zmienia coś w obiekcie
#3. update globalnej zmiennej img do wyświetlenia w canvas
#4. nowe image_id by zastąpić stary obrazek nowym po jakiejś
#   tam przemianie która nastąpiła w punkcie 2.

def resize():       #przycisk woła funkcję zmieniającą rozmiar o 10%

    #PONIŻEJ OPIS OGÓLNEGO TRYBU PRACY FUNKCJI 
    #PODŁĄCZONYCH DO PRZYCISKÓW I INNYCH WIDGETÓW
    #W PROGRAMIE

    #globalizuje się zmienne bo używa się tylko
    #jednego obrazka o jednym id jednocześnie
    global image_id
    global img

    #usuwam stary obrazek z wyświetlacza
    root.canvas.delete(image_id)

    #operacja na obiekcie
    root.resize(1.1)

    #załadowanie obrazka do zmiennej którą 
    #zrozumie gui (przez to ImageTk)
    img = ImageTk.PhotoImage(root.image)

    #wyświetlenie zmiennej do gui
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def resize1():      #przycisk woła funkcję zmieniającą rozmiar o -10%
    global image_id
    global img
    root.canvas.delete(image_id)
    root.resize(0.9)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def rotate_right(): #przycisk woła funkcję obracającą w prawo

    global image_id
    global img
    root.canvas.delete(image_id)
    root.rotate("right")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def rotate_left(): #przycisk woła funkcję obracającą w lewo

    global image_id
    global img
    #root.canvas.delete(image_id)
    root.rotate("left")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)


def undo():  #przycisk woła funkcję do cofania ostatniej operacji
    
    global image_id
    global img
    root.undo()
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def filtr_med_func(): #przycisk woła funkcję filtru medianowego który czyta wartość
                      #boku okna filtru z pola tekstowego "med_window"

    global image_id
    global img
    global size_var
    try:
        size_var = int(size_varr.get())
    except:
        return None
    
    root.median_filter(size_var)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def rgb_slider():   #przycisk woła funckję do zmiany parametrów RGB na podstawie
                    #trzech sliderów po jednym dla każdej składowej koloru pikseli

    global image_id
    global img
    global slider_var_R
    global slider_var_G
    global slider_var_B
    try:
        slider_var_R = slide_RGB1.get()
        slider_var_G = slide_RGB2.get()
        slider_var_B = slide_RGB3.get()
        print(f"R = {slider_var_R}, G = {slider_var_G}, B = {slider_var_B} ")
    except:
        return None
    root.RGB_levels(slider_var_R,  slider_var_G,  slider_var_B)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def contrast_adjustment():  #przycisk woła funkcję do zmiany kontrastu na podstawie parametru
                            #w polu 0-255
    global image_id
    global img
    global param_255_var
    try:
        param_255_var = int(param_255.get())
    except:
        return None
    root.contrast(param_255_var)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def brightness_adjustment():  #przycisk woła funkcję do zmiany jasności na podstawie parametru
                              #w polu 0-255
    global image_id
    global img
    global param_255_var
    try:
        param_255_var = int(param_255.get())
    except:
        return None
    root.brightness(param_255_var)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def sharpening():  #przycisk woła funkcję do zmiany ostrości na podstawie parametru
                   #w polu 0-255 który jest skalowany do 0-1 na potrzeby funkcji root.sharpening_filter
    global image_id
    global img
    global param_255_var
    try:
        param_255_var = int(param_255.get())
    except:
        return None
    scaled_param = float(param_255_var / 255)
    root.sharpening_filter(scaled_param)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)


#poniżej znajduje się kilka funkcji wołających funkcję kelner_filters z klasy GUI
#na podstawie przycisków 

def gaussian_blur_5x5():

    global image_id
    global img
    root.kernel_filters("gaussian_blur_5x5")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def gaussian_blur_3x3():

    global image_id
    global img
    root.kernel_filters("gaussian_blur_3x3")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def box_blur():

    global image_id
    global img
    root.kernel_filters("box_blur")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def edge_detection_1():

    global image_id
    global img
    root.kernel_filters("edge_detection_1")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def edge_detection_2():

    global image_id
    global img
    root.kernel_filters("edge_detection_2")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def edge_detection_3():

    global image_id
    global img
    root.kernel_filters("edge_detection_3")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)


def motion_get(event):
    global cursor_mode
    test = cursor_mode.get()
    root.cursor_mode = test
    root.canvas_position_x = root.canvas.winfo_x()
    root.canvas_position_y = root.canvas.winfo_y()

def motion_save_start(event):   #zapis początkowej pozycji kursora w trybie zaznaczania prostokąta
    global cursor_lock
    global x
    global y
    if root.cursor_mode == 1 and cursor_lock == False:
        x, y = event.x, event.y
        root.set_cursor_position(x, y, 0)
        cursor_lock = True

def motion_save_end(event):   #zapis końcowej pozycji kursora w trybie zaznaczania prostokąta
    global cursor_lock
    global x
    global y
    if root.cursor_mode == 1 and cursor_lock == True:
        x, y = event.x, event.y
        root.set_cursor_position(x, y, 1)
        cursor_lock = False

#przyciski
#tu można definiować nowe przyciski tak jak widać poniżej

#command = oznacza funkcję którą się odpala po kliknięciu 
#przycisku (mogą to być funkcje wewnątrz obiektu root.cośtam
#albo funkcje definiowane powyżej tak jak resize)

#frame'y czyli wiersze dla przycisków i pół tekstowych itp

upperframe = tk.Frame(root.window)
upperframe.pack(before = root.canvas)

functionframe = tk.Frame(root.window)
functionframe.pack(before = root.canvas)

functionframe1 = tk.Frame(root.window)
functionframe1.pack(before = root.canvas)

functionframe2 = tk.Frame(root.window)
functionframe2.pack(before = root.canvas)

fieldframe = tk.Frame(root.window)
fieldframe.pack(before = root.canvas)
fieldframe1 = tk.Frame(root.window)
fieldframe1.pack(before = root.canvas)

slideframe = tk.Frame(root.window)
slideframe.pack(before = root.canvas)

#pola tekstowe i ich opisy

size_varr=tk.StringVar(value=str(size_var))
med_window1 = tk.Label(fieldframe , text = 'Długość okna filtru medianowego', font=('calibre',10, 'bold'))
med_window = tk.Entry(fieldframe ,textvariable = size_varr, font=('calibre',10,'normal'))
med_window1.pack(side = tk.LEFT)
med_window.pack(side = tk.LEFT)

param_255=tk.StringVar(value=str(param_255_var))
param_1 = tk.Label(fieldframe1 , text = 'Parametr 0-255', font=('calibre',10, 'bold'))
param = tk.Entry(fieldframe1 ,textvariable = param_255, font=('calibre',10,'normal'))
param_1.pack(side = tk.LEFT)
param.pack(side = tk.LEFT)

#slidery RGB i ich etykiety

slide_RGB_label1 = tk.Label(slideframe , text = 'R', font=('calibre',10, 'bold'))
slide_RGB_label1.pack(side = tk.LEFT)
slide_RGB1 = tk.Scale(slideframe, from_=0, to=2 , resolution = 0.1, orient=tk.HORIZONTAL)
slide_RGB1.pack(side = tk.LEFT)
slide_RGB_label2 = tk.Label(slideframe , text = 'G', font=('calibre',10, 'bold'))
slide_RGB_label2.pack(side = tk.LEFT)
slide_RGB2 = tk.Scale(slideframe, from_=0, to=2 , resolution = 0.1, orient=tk.HORIZONTAL)
slide_RGB2.pack(side = tk.LEFT)
slide_RGB_label3 = tk.Label(slideframe , text = 'B', font=('calibre',10, 'bold'))
slide_RGB_label3.pack(side = tk.LEFT)
slide_RGB3 = tk.Scale(slideframe, from_=0, to=2 , resolution = 0.1, orient=tk.HORIZONTAL)
slide_RGB3.pack(side = tk.LEFT)

#poszególne przyciski 

exit_button = tk.Button(upperframe, text="Exit", command=root.window.destroy)
exit_button.pack(side = tk.LEFT)
restart_button = tk.Button(upperframe, text="Restart", command=root.reset)
restart_button.pack(side = tk.LEFT)
save_button = tk.Button(upperframe, text="Save", command=root.save)
save_button.pack(side = tk.LEFT)
plus_size_button = tk.Button(functionframe, text="+", command=resize)
plus_size_button.pack(side = tk.LEFT)
minus_size_button = tk.Button(functionframe, text="-", command=resize1)
minus_size_button.pack(side = tk.LEFT)
undo_button = tk.Button(functionframe, text="undo", command=undo)
undo_button.pack(side = tk.LEFT)


rotate_right_button = tk.Button(functionframe, text="rotate right", command=rotate_right)
rotate_right_button.pack(side = tk.LEFT)

rotate_left_button = tk.Button(functionframe, text="rotate left", command=rotate_left)
rotate_left_button.pack(side = tk.LEFT)

gaussian_blur = tk.Button(functionframe2, text="Gaussian Blur 5x5", command=gaussian_blur_5x5)
gaussian_blur.pack(side = tk.LEFT)

gaussian_blur3 = tk.Button(functionframe2, text="Gaussian Blur 3x3", command=gaussian_blur_3x3)
gaussian_blur3.pack(side = tk.LEFT)

box_blurr = tk.Button(functionframe2, text="Box Blur", command=box_blur)
box_blurr.pack(side = tk.LEFT)

edgy_1 = tk.Button(functionframe2, text="Edge Detection 1", command=edge_detection_1)
edgy_1.pack(side = tk.LEFT)

edgy_2 = tk.Button(functionframe2, text="Edge Detection 2", command=edge_detection_2)
edgy_2.pack(side = tk.LEFT)

edgy_3 = tk.Button(functionframe2, text="Edge Detection 3", command=edge_detection_3)
edgy_3.pack(side = tk.LEFT)

filtr_med = tk.Button(functionframe1, text="Filtr Medianowy", command=filtr_med_func)
filtr_med.pack(side = tk.LEFT)

RGB_button = tk.Button(functionframe1, text="Korekta RGB", command=rgb_slider)
RGB_button.pack(side = tk.LEFT)

contrast = tk.Button(functionframe1, text="Korektra kontrastu", command=contrast_adjustment)
contrast.pack(side = tk.LEFT)

brightness = tk.Button(functionframe1, text="Korektra jasności", command=brightness_adjustment)
brightness.pack(side = tk.LEFT)

sharpness = tk.Button(functionframe1, text="Wyostrzanie", command=sharpening)
sharpness.pack(side = tk.LEFT)

#checkbox trybu kursor/cały_obraz

mode_selector = tk.Checkbutton(functionframe, text="Cursor ON", variable=cursor_mode)
mode_selector.pack(side = tk.LEFT)

#eventy i ich pasujące funkcje

root.window.bind('<Motion>', motion_get)
root.window.bind('<KeyPress-Control_L>', motion_save_start)
root.window.bind('<KeyRelease-Control_L>', motion_save_end)

#loop gui

root.window.mainloop()