import tkinter as tk
from PIL import ImageTk
from PIL import Image
from gui import GUI
from numpy import asarray
from functools import partial

print("czeźdź")
root = GUI()

#powyżej ustalane są wszystkie parametry czyli:
#wczytywane jest zdjęcie do obiektu root, ustalana
#jest ramka root.window do której przyciski itp są 
#przyczepione oraz tworzony jest canvas czyli pole
#na którym wyświetlany będzie obrazek (canvas ma 
#rozmiar jak oryginalna rozdzielczość obrazka
#plus trzydzieści pikseli)

root.canvas.pack()
img = ImageTk.PhotoImage(root.image)
image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)
cursor_mode = tk.IntVar()
cursor_lock = False
x = 0
y = 0
size_var = 4        #domyślna wartość szerokości okna filtru medianowego
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

def resize():
    #globalizuje się zmienne bo używa się tylko
    #jednego obrazka o jednym id jednocześnie
    #(pewnie możnaby to zrobić lepiej ale teraz
    #nie mam ochoty xd)
    global image_id
    global img

    #usuwam stary obrazek z wyświetlacza 
    #(można ewentualnie zmienić kolejność to może
    #nie będzie mrygać przy bardziej złożonych
    #operacjach)
    root.canvas.delete(image_id)

    #operacja na obiekcie
    root.resize(1.1)

    #załadowanie obrazka do zmiennej którą 
    #zrozumie gui (przez to ImageTk)
    img = ImageTk.PhotoImage(root.image)

    #wyświetlenie zmiennej do gui
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def resize1():
    global image_id
    global img
    root.canvas.delete(image_id)
    root.resize(0.9)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def rotate_right():

    global image_id
    global img
    root.canvas.delete(image_id)
    root.rotate("right")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def rotate_left():

    global image_id
    global img
    #root.canvas.delete(image_id)
    root.rotate("left")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def spin(event):
    rotate_left()
    resize1()

def undo():
    
    global image_id
    global img
    root.undo()
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def filtr_med_func():

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

def rgb_slider():

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

    ## nowe funkcje do zmiany kontrastu i jasnosci, trzeba dodac jakis wybor wartosci do kazdej, obie biora wartosci od -255 do 255
def contrast_adjustment():
    global image_id
    global img
    root.contrast(255)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def brightness_adjustment():
    global image_id
    global img
    root.brightness(50)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def motion_get(event):
    global cursor_mode
    test = cursor_mode.get()
    root.cursor_mode = test
    root.canvas_position_x = root.canvas.winfo_x()
    root.canvas_position_y = root.canvas.winfo_y()

def motion_save_start(event):
    global cursor_lock
    global x
    global y
    if root.cursor_mode == 1 and cursor_lock == False:
        x, y = event.x, event.y
        root.set_cursor_position(x, y, 0)
        cursor_lock = True

def motion_save_end(event):
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

upperframe = tk.Frame(root.window)
upperframe.pack(before = root.canvas)

functionframe = tk.Frame(root.window)
functionframe.pack(before = root.canvas)

fieldframe = tk.Frame(root.window)
fieldframe.pack(before = root.canvas)

slideframe = tk.Frame(root.window)
slideframe.pack(before = root.canvas)


size_varr=tk.StringVar(value=str(size_var))
med_window1 = tk.Label(fieldframe , text = 'Długość okna filtru medianowego', font=('calibre',10, 'bold'))
med_window = tk.Entry(fieldframe ,textvariable = size_varr, font=('calibre',10,'normal'))
med_window1.pack(side = tk.LEFT)
med_window.pack(side = tk.LEFT)

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

##test kontrastu
test = tk.Button(functionframe, text="test", command=brightness_adjustment)
test.pack(side = tk.LEFT)

filtr_med = tk.Button(functionframe, text="Filtr Medianowy", command=filtr_med_func)
filtr_med.pack(side = tk.LEFT)

RGB_button = tk.Button(functionframe, text="Korekta RGB", command=rgb_slider)
RGB_button.pack(side = tk.LEFT)

mode_selector = tk.Checkbutton(functionframe, text="Cursor ON", variable=cursor_mode)
mode_selector.pack(side = tk.LEFT)

root.window.bind('<Motion>', motion_get)
root.window.bind('<KeyPress-Control_L>', motion_save_start)
root.window.bind('<KeyRelease-Control_L>', motion_save_end)

root.window.mainloop()




