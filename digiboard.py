from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, simpledialog  # Import simpledialog module
import os
import cv2
from PIL import ImageGrab
import random  # Import random module

root = Tk()
root.title("WHITE BOARD")
root.geometry("1050x570+150+50")
root.config(bg="#f2f3f5")
root.resizable(True, True)

current_x = 0
current_y = 0
color = "black"
slide_count = 1
selected_item = None

def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def addline(work):
    global current_x, current_y
    canvas.create_line((current_x, current_y, work.x, work.y), width=get_current_value(), fill=color, capstyle=ROUND, smooth=True)
    current_x, current_y = work.x, work.y

def show_color(new_color):
    global color
    color = new_color

def new_canvas():
    canvas.delete('all')
    display_pallete()

def insertimage():
    global filename, f_img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file", filetypes=(("PNG file", "*.png"), ("All file", "new.txt")))
    f_img = tk.PhotoImage(file=filename)
    my_img = canvas.create_image(180, 50, image=f_img)
    root.bind("<B3-Motion>", my_callback)

def my_callback(event):
    f_img = tk.PhotoImage(file=filename)
    my_img = canvas.create_image(event.x, event.y, image=f_img)

def insert_video():
    video_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if video_file_path:
        cap = cv2.VideoCapture(video_file_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def save_slide():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab(bbox=(x, y, x1, y1)).save(file_path)

def add_slide():
    global slide_count
    slide_count += 1
    lbl_slide_count.config(text=f"Slide: {slide_count}")
    canvas.delete('all')

def add_text():
    text = simpledialog.askstring("Text", "Enter text:")
    if text:
        # Calculate the center position of the sticky note rectangle
        sticky_note_center_x = current_x + 100
        sticky_note_center_y = current_y + 75
        # Create the text item at the center of the sticky note
        text_item = canvas.create_text(sticky_note_center_x, sticky_note_center_y, text=text, fill=color, font=("Arial", 12), anchor="center")
        canvas.tag_bind(text_item, '<Button-1>', lambda event, item=text_item: select_item(event, item))
def select_item(event, item):
    global selected_item
    selected_item = item
    canvas.tag_bind(selected_item, '<B1-Motion>', move_item)

def move_item(event):
    global color
    if selected_item:
        x, y = event.x, event.y
        color = "" 
        canvas.coords(selected_item, x, y)

def create_sticky_note():
    colors = ["yellow", "pink", "blue", "green"]  # List of available colors for sticky notes
    random_color = random.choice(colors)  # Choose a random color from the list
    sticky_note = canvas.create_rectangle(current_x, current_y, current_x + 200, current_y + 150, fill=random_color, outline="black")
    canvas.tag_bind(sticky_note, '<Button-1>', lambda event: add_text())

# Sidebar
color_box = PhotoImage(file="")
Label(root, image=color_box, bg="#f2f3f5").place(x=10, y=2)

clear_btn = Button(root, text="Clear", bg="#f2f3f5", command=new_canvas)
clear_btn.place(x=30, y=400)

# Add the button for saving the slide
save_button = Button(root, text="Save", command=save_slide)
save_button.place(x=30, y=430)

insert_image = Button(root, text="Insert Image", bg="white", command=insertimage)
insert_image.place(x=30, y=450)

insert_video = Button(root, text="Insert Video", bg="white", command=insert_video)
insert_video.place(x=30, y=480)

# Create the label for slide count
lbl_slide_count = tk.Label(root, text=f"Slide: {slide_count}", bg="#f2f3f5")
lbl_slide_count.place(x=30, y=380)

# Button to add a new slide
btn_new_slide = tk.Button(root, text="New Slide", command=add_slide)
btn_new_slide.place(x=30, y=500)

# Button to add text
btn_add_text = tk.Button(root, text="Add Text", command=add_text)
btn_add_text.place(x=30, y=530)

# Button to create sticky note
btn_add_sticky = Button(root, text="Add Sticky Note", command=create_sticky_note)
btn_add_sticky.place(x=30, y=560)

# Colors
colors = Canvas(root, bg="#fff", width=37, height=300, bd=0)
colors.place(x=30, y=60)

def display_pallete():
    id = colors.create_rectangle((10, 10, 30, 30), fill="black")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('black'))

    id = colors.create_rectangle((10, 40, 30, 60), fill="grey")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('grey'))

    id = colors.create_rectangle((10, 70, 30, 90), fill="brown4")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('brown4'))

    id = colors.create_rectangle((10, 100, 30, 120), fill="red")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('red'))

    id = colors.create_rectangle((10, 130, 30, 150), fill="orange")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('orange'))

    id = colors.create_rectangle((10, 160, 30, 180), fill="yellow")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('yellow'))

    id = colors.create_rectangle((10, 190, 30, 210), fill="blue")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('blue'))

    id = colors.create_rectangle((10, 220, 30, 240), fill="green")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('green'))

    id = colors.create_rectangle((10, 250, 30, 270), fill="purple")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('purple'))

display_pallete()

# Main screen
canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=10)

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', addline)

# Slider
current_value = tk.DoubleVar()
def get_current_value():
    return '{: .2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=slider_changed, variable=current_value)
slider.place(x=30, y=570)

value_label = ttk.Label(root, text=get_current_value())
value_label.place(x=27, y=550)

root.mainloop()
