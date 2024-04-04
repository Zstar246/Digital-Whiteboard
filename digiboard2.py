import tkinter as tk
from tkinter import filedialog,simpledialog
import cv2
import random
from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageGrab

class DigitalWhiteboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Ace's Digital board")

        self.slides = [] 
        self.current_slide_index = 0 

        self.navbar = tk.Frame(self.master)
        self.navbar.pack(fill=tk.X)

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

       
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_canvas)
        self.file_menu.add_command(label="Open", command=self.open_canvas)


        self.insert_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Insert", menu=self.insert_menu)
        self.insert_menu.add_command(label="Insert Image", command=self.insert_image)
        self.insert_menu.add_command(label="Insert Video", command=self.insert_video)
        self.insert_menu.add_command(label="Insert Text", command=self.insert_text)
        self.insert_menu.add_command(label="Add Sticky Note", command=self.add_sticky_note)
        self.insert_menu.add_command(label="Remove Video", command=self.remove_video)
        self.insert_menu.add_command(label="Add Slide", command=self.add_slide)

        self.color_frame = tk.Frame(self.master, bg="white")
        self.color_frame.pack(fill=tk.BOTH)
        # self.save_button = tk.Button(self.navbar, text="Save", command=self.save_canvas)
        # self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.open_button = tk.Button(self.navbar, text="Open", command=self.open_canvas)
        # self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.insert_button = tk.Button(self.navbar, text="Insert Image", command=self.insert_image)
        # self.insert_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.insert_text_button = tk.Button(self.navbar, text="Insert Text", command=self.insert_text)
        # self.insert_text_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.add_sticky_button = tk.Button(self.navbar, text="Add Sticky Note", command=self.add_sticky_note)
        # self.add_sticky_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.color_frame, text="Clear Screen", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.insert_video_button = tk.Button(self.navbar, text="Insert Video", command=self.insert_video)
        # self.insert_video_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.insert_video_button = tk.Button(self.navbar, text="Remove Video", command=self.remove_video)
        # self.insert_video_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.add_slide_button = tk.Button(self.color_frame, text="Add Slide", command=self.add_slide)
        self.add_slide_button.pack(side=tk.LEFT, padx=5, pady=5)
       
        self.lbl_slide_count = tk.Label(self.color_frame, text="")
        self.lbl_slide_count.pack(side=tk.LEFT, padx=5, pady=5)

        self.paused = False

        

        self.colors = ["black", "red", "blue", "green", "yellow", "orange", "purple"]
        for color in self.colors:
            color_btn = tk.Button(self.color_frame, bg=color, width=2, command=lambda c=color: self.change_color(c))
            color_btn.pack(side=tk.LEFT)

        self.line_width_scale = tk.Scale(self.color_frame,background="white", from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_line_width)
        self.line_width_scale.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.color = "black"  
        self.line_width = 2  

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.prev_x, self.prev_y = None, None
        self.image_id = None
        self.video_inserted = tk.BooleanVar(value=False) 
        
    def draw(self, event):
        if self.prev_x and self.prev_y:
            x1, y1 = self.prev_x, self.prev_y
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.line_width)
        self.prev_x, self.prev_y = event.x, event.y

    def reset(self, event):
        self.prev_x, self.prev_y = None, None

    def change_color(self, new_color):
        self.color = new_color

    def change_line_width(self, value):
        self.line_width = int(value)

    def save_canvas(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            x0 = self.canvas.winfo_rootx()
            y0 = self.canvas.winfo_rooty()
            x1 = x0 + self.canvas.winfo_width()
            y1 = y0 + self.canvas.winfo_height()
            ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(filename)

    def open_canvas(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if filename:
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo  

    def insert_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if filename:
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
            self.canvas.bind("<Button-1>", self.move_start)
            self.canvas.bind("<B1-Motion>", self.move_image)

    def move_start(self, event):
        self.start_x, self.start_y = event.x, event.y

    def move_image(self, event):
        if self.image_id and self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.image_id, dx, dy)
            self.start_x, self.start_y = event.x, event.y

    def insert_text(self):
        text = simpledialog.askstring("Insert Text", "Enter your text:")
        if text:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            text_id = self.canvas.create_text(x, y, text=text, fill=self.color, font=("Helvetica", 12))
            self.canvas.tag_bind(text_id, "<Button-1>", self.select_text)
            self.canvas.tag_bind(text_id, "<B1-Motion>", self.move_text)

    def select_text(self, event):
        self.selected_item = event.widget.find_closest(event.x, event.y)[0]
        self.start_x, self.start_y = event.x, event.y

    def move_text(self, event):
        if self.selected_item and self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.selected_item, dx, dy)
            self.start_x, self.start_y = event.x, event.y

    def add_sticky_note(self):
        colors = ["yellow", "pink", "blue", "green"]  # List of available colors for sticky notes
        random_color = random.choice(colors)
        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() // 2
        sticky_note = self.canvas.create_rectangle(x - 200, y - 110, x + 50, y + 30, fill=random_color)
        text_x = (x - 200 + x + 50) // 2  # Center of the sticky note horizontally
        text_y = (y - 110 + y + 30) // 2  # Center of the sticky note vertically
        text = self.canvas.create_text(text_x, text_y, text="", fill=self.color, font=("Helvetica", 12))
        self.canvas.tag_bind(sticky_note, "<Button-1>", self.select_sticky_note)
        self.canvas.tag_bind(sticky_note, "<B1-Motion>", self.move_sticky_note)
        self.canvas.tag_bind(sticky_note, "<Double-Button-1>", lambda event: self.insert_text_in_sticky(event, text))

    def select_sticky_note(self, event):
        self.selected_item = event.widget.find_closest(event.x, event.y)[0]
        self.start_x, self.start_y = event.x, event.y

    def move_sticky_note(self, event):
        if self.selected_item and self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.selected_item, dx, dy)
            self.canvas.move(self.selected_item + 1, dx, dy)  # Move the associated text as well
            self.start_x, self.start_y = event.x, event.y
            self.color=""

    def insert_text_in_sticky(self, event, text_id):
        x1, y1, x2, y2 = self.canvas.coords(self.selected_item)
        text = simpledialog.askstring("Insert Text", "Enter text for sticky note:")
        if text:
            x = (x1 + x2)/2
            y = (y1 + y2)/2
            self.canvas.itemconfig(text_id, text=text)
            self.color=""

    def clear_canvas(self):
        self.canvas.delete("all")
    
    def remove_video(self):
        if self.video_label:
            self.video_label.destroy()
            self.video_label = None
            self.video = None
            self.video_width = None
            self.video_height = None
            self.video_inserted.set(False)  
            self.remove_video_button.grid_remove()

    def pause_video(self):
        if self.paused:
            self.paused = False
            self.update_video()
        else:
            self.paused = True

    def video_click_handler(self, event):
        self.pause_video()

    def update_video(self):
        if not self.paused:
            ret, frame = self.video.read()

            if ret:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                photo = ImageTk.PhotoImage(image)
                self.video_label.config(image=photo)
                self.video_label.image = photo
                self.canvas.after(25, self.update_video)

            else:
                self.video.release()
                self.video = None
                self.video_label.destroy()
                self.video_label = None
                self.video_inserted.set(False)
                self.remove_video_button.grid_remove()

    def insert_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if filename:
            self.video = cv2.VideoCapture(filename)

            # Get the video's width and height
            self.video_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Create a tkinter Label to display the video
            self.video_label = tk.Label(self.canvas, width=self.video_width, height=self.video_height)
            self.video_label.pack()

            # Bind click event to video label
            self.video_label.bind("<Button-1>", self.video_click_handler)

            # Start the video update loop
            self.update_video()
            self.video_inserted.set(True)  
            self.remove_video_button.grid()

   
    def add_slide(self):
        self.current_slide_index += 1  # Increment the current slide index
        self.slides.append([])  # Add an empty list for the new slide
        self.lbl_slide_count.config(text=f"Slide: {self.current_slide_index}")  # Update the label displaying the slide count
        
        # Clear the canvas to create a new slide
        self.canvas.delete('all')

        # Restore the content of the previous slide, if any
        if self.current_slide_index > 1:
            previous_slide_content = self.slides[self.current_slide_index - 2]
            for item in previous_slide_content:
                item_type = item[0]
                if item_type == 'line':
                    x1, y1, x2, y2, color, width = item[1:]
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                elif item_type == 'text':
                    x, y, text, color, font = item[1:]
                    self.canvas.create_text(x, y, text=text, fill=color, font=font)

   


def main():
    root = tk.Tk()
    whiteboard = DigitalWhiteboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
