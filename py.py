import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import math


root = tk.Tk()
root.title("Вимірювання відстані на карті")


canvas = tk.Canvas(root, width=800, height=600, bg="light gray")
canvas.pack()


points = []

def load_image():
    """Завантажити зображення з файлу."""
    global img, img_tk
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        canvas.config(width=img_tk.width(), height=img_tk.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        points.clear()
        result_label.config(text="Відстань: ")

def paste_image():
    """Вставити зображення з буфера обміну."""
    global img, img_tk
    img = ImageGrab.grabclipboard()
    if img is not None:
        img_tk = ImageTk.PhotoImage(img)
        canvas.config(width=img_tk.width(), height=img_tk.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        points.clear()
        result_label.config(text="Відстань: ")
    else:
        result_label.config(text="Буфер обміну порожній або не містить зображення.")

def on_click(event):
    if len(points) < 2:
        points.append((event.x, event.y))
        canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
    if len(points) == 2:
        calculate_distance()

def calculate_distance():
    
    x1, y1 = points[0]
    x2, y2 = points[1]

    
    pixel_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    
    try:
        grid_scale_meters = float(scale_entry.get())
    except ValueError:
        result_label.config(text="Введіть коректний масштаб!")
        return

    
    grid_size_pixels = img.width / 7  

    
    real_distance = (pixel_distance / grid_size_pixels) * grid_scale_meters

    
    result_label.config(text=f"Відстань: {real_distance:.2f} м")

def reset_image():
    
    canvas.delete("all")
    points.clear()
    result_label.config(text="Відстань: ")
    scale_entry.delete(0, tk.END)


load_button = tk.Button(root, text="Завантажити зображення", command=load_image)
load_button.pack()


paste_button = tk.Button(root, text="Вставити зображення з буфера обміну", command=paste_image)
paste_button.pack()


reset_button = tk.Button(root, text="Скинути", command=reset_image)
reset_button.pack()


tk.Label(root, text="Масштаб (метрів у клітинці):").pack()
scale_entry = tk.Entry(root)
scale_entry.pack()


result_label = tk.Label(root, text="Відстань: ")
result_label.pack()


canvas.bind("<Button-1>", on_click)


root.mainloop()
