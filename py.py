import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import math

root = tk.Tk()
root.title("Вимірювання відстані на карті")

canvas = tk.Canvas(root, width=800, height=600, bg="light gray")
canvas.pack()

points = []
scale_factor = 1.0  
img = None
img_tk = None
crop_mode = False

def load_image():
    """Завантажити зображення з файлу."""
    global img, img_tk, scale_factor
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        scale_factor = 1.0  
        update_image()

def paste_image():
    """Вставити зображення з буфера обміну."""
    global img, img_tk, scale_factor
    img = ImageGrab.grabclipboard()
    if img is not None:
        scale_factor = 1.0  
        update_image()
    else:
        result_label.config(text="Буфер обміну порожній або не містить зображення.")

def update_image():
    """Оновити зображення на полотні відповідно до масштабу."""
    global img_tk
    if img is not None:
        img_resized = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)

        canvas.config(width=img_tk.width(), height=img_tk.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        for point in points:
            scaled_x = point[0] * scale_factor
            scaled_y = point[1] * scale_factor
            canvas.create_oval(scaled_x-2, scaled_y-2, scaled_x+2, scaled_y+2, fill='red')

        distance = calculate_distance()
        azimuth = calculate_azimuth()
        result_label.config(text=f"Відстань: {distance:.2f} м, Азимут: {azimuth:.2f}°")

def on_click(event):
    global crop_mode
    if crop_mode:
        crop_to_point(event.x)
        crop_mode = False
    elif len(points) < 2:
        points.append((event.x / scale_factor, event.y / scale_factor))  
        canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        if len(points) == 2:
            result_label.config(text=f"Відстань: {calculate_distance():.2f} м, Азимут: {calculate_azimuth():.2f}°")

def calculate_distance():
    if len(points) < 2:
        return 0  

    x1, y1 = points[0]
    x2, y2 = points[1]
    pixel_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    try:
        grid_scale_meters = float(scale_entry.get())
    except ValueError:
        result_label.config(text="Введіть коректний масштаб!")
        return 0

    grid_size_pixels = img.width / 7  
    real_distance = (pixel_distance / grid_size_pixels) * grid_scale_meters
    return real_distance

def calculate_azimuth():
    if len(points) < 2:
        return 0

    x1, y1 = points[0]
    x2, y2 = points[1]

    delta_x = x2 - x1
    delta_y = y2 - y1

    azimuth = math.degrees(math.atan2(delta_y, delta_x))
    azimuth = (azimuth + 90) % 360

    return azimuth

def reset_image():
    canvas.delete("all")
    points.clear()
    result_label.config(text="Відстань: ")
    scale_entry.delete(0, tk.END)

def zoom_in(event):
    global scale_factor
    scale_factor *= 1.1  
    update_image()

def zoom_out(event):
    global scale_factor
    scale_factor *= 0.9  
    update_image()

def crop_to_point(x_click):
    """Обрізати зображення по правому краю до обраної точки."""
    global img, img_tk
    if img is not None:
        right_crop = x_click / scale_factor
        cropped_img = img.crop((0, 0, min(right_crop, img.width), img.height))
        img = cropped_img  # Оновлюємо зображення
        update_image()

def activate_crop_mode():
    """Активувати режим обрізки зображення."""
    global crop_mode
    crop_mode = True
    result_label.config(text="Клацніть на зображення, щоб обрізати по правому краю.")

# Кнопки та елементи інтерфейсу
load_button = tk.Button(root, text="Завантажити зображення", command=load_image)
load_button.pack()

paste_button = tk.Button(root, text="Вставити зображення з буфера обміну", command=paste_image)
paste_button.pack()

reset_button = tk.Button(root, text="Скинути", command=reset_image)
reset_button.pack()

crop_button = tk.Button(root, text="Обрізати", command=activate_crop_mode)
crop_button.pack()

tk.Label(root, text="Масштаб (метрів у клітинці):").pack()
scale_entry = tk.Entry(root)
scale_entry.pack()

result_label = tk.Label(root, text="Відстань: ")
result_label.pack()

canvas.bind("<Button-1>", on_click)
root.bind("<Up>", zoom_in)   
root.bind("<Down>", zoom_out) 

root.mainloop()
