import tkinter as tk
from PIL import ImageTk
from gui import GUI

print("czeźdź")

root = GUI("kek.jpg")
canvas = root.canvas_init()
img = ImageTk.PhotoImage(root.image)
canvas.create_image(20,20, anchor = tk.NW, image=img)
root.window.mainloop()

#root = tk.Tk()
#canvas = tk.Canvas(root, width = 900, height = 1000)      
#canvas.pack()      
#img = ImageTk.PhotoImage(file="kek.jpg")      
#canvas.create_image(20,20, anchor=tk.NW, image=img)      
#tk.mainloop()