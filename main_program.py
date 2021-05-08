import tkinter as tk
from PIL import ImageTk
from PIL import Image
from gui import GUI
from numpy import asarray
from functools import partial


print("czeźdź")

global root
root = GUI()

root.canvas.pack()
img = ImageTk.PhotoImage(root.image)
image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def resize():
    global image_id
    global img
    root.canvas.delete(image_id)
    root.resize(1.1)
    #root.canvas = root.canvas_init()   #czy mogę zmienić wielkość canvas?
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

def resize1():
    global image_id
    global img
    root.canvas.delete(image_id)
    root.resize(0.9)
    img = ImageTk.PhotoImage(root.image)
    image_id = root.canvas.create_image(20,20, anchor = tk.NW, image=img) 

#przyciski

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

root.window.mainloop()




