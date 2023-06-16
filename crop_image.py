import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import os

# Define global variables
image_width = 800
image_height = 600
resized_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
latest_value = 0
update_delay = 10  # milliseconds


def update_image(value, label):
    global latest_value
    latest_value = round(float(value), 3)


def update_image_continuous(label):
    global resized_image, latest_value
    y_coordinate = int(latest_value * image_height / 100)
    image_with_line = resized_image.copy()
    cv2.line(image_with_line, (0, y_coordinate), (image_width, y_coordinate), (0, 255, 0), 1)
    pil_image = Image.fromarray(image_with_line)
    image = ImageTk.PhotoImage(pil_image)
    label.configure(image=image)
    label.image = image
    label.after(update_delay, update_image_continuous, label)


def print_slider_value():
    global latest_value
    value = latest_value
    confirmation = messagebox.askquestion("Confirmation", "Do you want to finalize this value?")

    if confirmation == "yes":
        print(value)


def main_ui(image_name):
    global resized_image
    cap = cv2.imread(image_name)
    window = tk.Tk()
    window.title("Crop Image")
    window.state("zoomed")
    image_label = tk.Label(window)
    image_label.pack()
    slider = tk.Scale(window, from_=0, to=100, orient=tk.VERTICAL, resolution=0.001,
                  length=100, width=20, command=lambda value: update_image(value, image_label))

    slider.pack()
    ok_button = tk.Button(window, text="OK", command=print_slider_value)
    ok_button.pack()
    update_image_continuous(image_label)
    while True:
        frame = cap
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(rgb_image, (image_width, image_height))
        pil_image = Image.fromarray(resized_image)
        image = ImageTk.PhotoImage(pil_image)
        image_label.configure(image=image)
        image_label.image = image
        window.update()
        if not tk._default_root:
            break

    cv2.destroyAllWindows()


def initiate_crop_calibration(image_name):
    main_ui(image_name)
    global latest_value
    return latest_value

