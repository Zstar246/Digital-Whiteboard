import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

DigiBoard=customtkinter.CTk()
DigiBoard.geometry("1000x600")
DigiBoard.title('Ace Studyboard')



class DrawingApp:
    def __init__(self, width=800, height=600):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=width, height=height)
        self.canvas.pack()

        # Initialize drawing variables
        self.drawing = False
        self.start_x, self.start_y = None, None

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def run(self):
        self.window.mainloop()

    def on_button_press(self, event):
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y

    def on_motion(self, event):
        if self.drawing:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, width=5, capstyle="round")
            self.start_x, self.start_y = x2, y2

    def on_button_release(self, event):
        self.drawing = False

if __name__ == "__main__":
    app = DrawingApp()
    app.run()
