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
    root.canvas.delete(image_id)
    root.rotate("left")
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def undo():
    
    global image_id
    global img
    root.undo()
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)

def test():

    global image_id
    global img
    root.median_filter(3)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img)



#przyciski
#tu można definiować nowe przyciski tak jak widać poniżej

#command = oznacza funkcję którą się odpala po kliknięciu 
#przycisku (mogą to być funkcje wewnątrz obiektu root.cośtam
#albo funkcje definiowane powyżej tak jak resize)

exit_button = tk.Button(root.window, text="Exit", command=root.window.destroy)
exit_button.pack(before = root.canvas)
restart_button = tk.Button(root.window, text="Restart", command=root.reset)
restart_button.pack(before = root.canvas)
save_button = tk.Button(root.window, text="Save", command=root.save)
save_button.pack(before = root.canvas)
plus_size_button = tk.Button(root.window, text="+", command=resize)
plus_size_button.pack(before = root.canvas)
minus_size_button = tk.Button(root.window, text="-", command=resize1)
minus_size_button.pack(before = root.canvas)
undo_button = tk.Button(root.window, text="undo", command=undo)
undo_button.pack(before = root.canvas)

rotate_right_button = tk.Button(root.window, text="rotate right", command=rotate_right)
rotate_right_button.pack(before = root.canvas)
rotate_left_button = tk.Button(root.window, text="rotate left", command=rotate_left)
rotate_left_button.pack(before = root.canvas)

##przyciski do testowania filtru, trzeba dodac przyciskt i pole do wyboru rozmiaru okna
test = tk.Button(root.window, text="test", command=test)
test.pack(before = root.canvas)


root.window.mainloop()




