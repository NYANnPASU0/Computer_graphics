import tkinter as tk
from tkinter import ttk
import os
import math
from generate_file import generate_new_file
from tkinter import messagebox, filedialog, simpledialog


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

        self.cell = 35
        self.canvas_width = 700
        self.canvas_height = 700

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

    def draw_rectangle(self):
        if self.rectangle:
            x1, y1 = self.coords_to_screen(self.rectangle.x_min, self.rectangle.y_min)
            x2, y2 = self.coords_to_screen(self.rectangle.x_max, self.rectangle.y_max)
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='blue', width=3, fill='', tags='rectangle')

    def load_file(self):
            from generate_file import select_existing_file 
            
            filepath = select_existing_file(self.root)
            if filepath:
                if self.read_data_from_file(filepath):
                    self.select_file = filepath
                    self.draw_grid()
                    self.draw_rectangle()
                    #self.draw_lines()


    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        #подзаголовок - файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Создать новый файл", command = lambda: generate_new_file(self.root, os.path.join("Line_clipping_algorithms_4", "files")))
        file_menu.add_command(label="Выбрать существущий файл   >", command = self.load_file)
        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Выход", command=self.root.quit) #выход


    def get_center(self):
        if self.rectangle is None:
            return 0, 0, self.canvas_width / 2, self.canvas_height / 2

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

        for x in range(-self.canvas_height, self.canvas_height):
            if x == 0:
                continue
            screen_x, screen_y = self.coords_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                self.canvas.create_text(screen_x, screen_y + 15, text=str(x), 
                                       fill='gray', font=('Arial', 9))
        
        for y in range(-self.canvas_width, self.canvas_width):
            if y == 0:
                continue
            screen_x, screen_y = self.coords_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                self.canvas.create_text(screen_x - 15, screen_y, text=str(y), 
                                       fill='gray', font=('Arial', 9))
        
        screen_x, screen_y = self.coords_to_screen(0, 0)
        if 0 <= screen_x <= self.canvas_width and 0 <= screen_y <= self.canvas_height:
            self.canvas.create_text(screen_x + 5, screen_y + 15, text="0",
                                   fill='gray', font=('Arial', 10, 'bold'))

    def read_data_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.lines = []
        self.rectangle = None
        
        #удаление пустых строк
        data_lines = []
        for line in lines:
            line = line.strip()
            if line:
                data_lines.append(line)
        
        rect_coords = []
        for i in range(4):
            coords = data_lines[i].split()
            x = int(coords[0])
            y = int(coords[1])
            rect_coords.append((x, y))
        
        A = Point(rect_coords[0][0], rect_coords[0][1])
        B = Point(rect_coords[1][0], rect_coords[1][1])
        C = Point(rect_coords[2][0], rect_coords[2][1])
        D = Point(rect_coords[3][0], rect_coords[3][1])
        self.rectangle = Rectangle(A, B, C, D)
        
        # читаем отрезки
        line_index = 4
        while line_index < len(data_lines):
            start_coords = data_lines[line_index].split()
            end_coords = data_lines[line_index + 1].split()
            
            x1 = int(start_coords[0])
            y1 = int(start_coords[1])
            x2 = int(end_coords[0])
            y2 = int(end_coords[1])
            
            start_point = Point(x1, y1)
            end_point = Point(x2, y2)
            self.lines.append((start_point, end_point))
            
            line_index += 2
        
        return True


if __name__ == "__main__":
    window = tk.Tk()
    app = Window(window)
    window.mainloop()