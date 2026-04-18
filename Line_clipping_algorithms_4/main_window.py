import tkinter as tk
from tkinter import ttk
import os
import math
from generate_file import open_file_explorer,  generate_new_file


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, A: Point, B: Point, C: Point, D: Point):
        self.A = A 
        self.B = B
        self.C = C
        self.D = D 

        all_x = [A.x, B.x, C.x, D.x]
        all_y = [A.y, B.y, C.y, D.y]
        
        self.x_min = min(all_x)
        self.x_max = max(all_x)
        self.y_min = min(all_y)
        self.y_max = max(all_y)

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы отсечения отрезка")
        self.root.geometry("950x700")

        self.cell = 30
        self.canvas_width = 700
        self.canvas_height = 900

        self.select_file = None
        self.rectangle = None
        self.lines = []  # список отрезков

        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_fields()
        self.create_menu()

        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.draw_grid()


    def input_fields(self):
        button_frame = ttk.Frame(self.info_frame)
        button_frame.pack(pady=20, padx=10)


    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        #подзаголовок - файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Создать новый файл", command = lambda: generate_new_file(self.root, os.path.join("Line_clipping_algorithms_4", "files")))
        file_menu.add_command(label="Выбрать существущий файл   >", command = lambda: open_file_explorer(os.path.join("Line_clipping_algorithms_4", "files")))
        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Выход", command=self.root.quit) #выход
        
    
    def set_rectangle(self, x_min, y_min, x_max, y_max):
        A = Point(x_min, y_min)
        B = Point(x_max, y_min)
        C = Point(x_max, y_max)
        D = Point(x_min, y_max)
        self.rectangle = Rectangle(A, B, C, D)
    
    def get_center(self):
        center_w_x = (self.rectangle.x_min + self.rectangle.x_max) / 2
        center_w_y = (self.rectangle.y_min + self.rectangle.y_max) / 2

        screen_center_x = self.canvas_width / 2
        screen_center_y = self.canvas_height / 2
        
        return center_w_x, center_w_y, screen_center_x, screen_center_y


    def coords_to_screen(self, x, y):
        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        
        screen_x = screen_center_x + (x - w_center_x) * self.cell
        screen_y = screen_center_y - (y - w_center_y) * self.cell
        
        return screen_x, screen_y
    
    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=False)

        for x in range(-self.canvas_height, self.canvas_height):
            screen_x, c = self.coords_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                if x == 0:
                    color = 'black'
                else:
                    color = 'lightgray'
                self.canvas.create_line(screen_x, 0, screen_x, self.canvas_height, fill=color)
        
        for y in range(-self.canvas_width, self.canvas_width):
            c, screen_y = self.coords_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                if y == 0:
                    color = 'black'
                else:
                    color = 'lightgray'
                self.canvas.create_line(0, screen_y, self.canvas_width, screen_y, fill=color)
        

if __name__ == "__main__":
    window = tk.Tk()
    app = Window(window)
    window.mainloop()