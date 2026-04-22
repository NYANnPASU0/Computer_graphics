import tkinter as tk
from tkinter import ttk
import math

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Section:
    def __init__(self, a: Point, b: Point):
        if a.y <= b.y:
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a

    def get_borders(self, indent: int = 3):
        min_x = min(self.a.x, self.b.x)
        min_y = min(self.a.y, self.b.y)
        max_x = max(self.a.x, self.b.x)
        max_y = max(self.a.y, self.b.y)

        min_x -= indent
        min_y -= indent
        max_x += indent
        max_y += indent

        return min_x, min_y, max_x, max_y

class Fill_area:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм заполнения областей")
        self.root.geometry("950x700")
        
        self.cell = 30
        self.section = None

        self.canvas_width = 700
        self.canvas_height = 700
        
        self.input_fields()
        
        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        self.draw_grid()
    
    def get_center(self):
        if self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=3)
            center_w_x = (min_x + max_x) / 2
            center_w_y = (min_y + max_y) / 2
        else:
            center_w_x = 0
            center_w_y = 0
        
        screen_center_x = self.canvas_width // 2
        screen_center_y = self.canvas_height // 2
        
        return center_w_x, center_w_y, screen_center_x, screen_center_y
    
    def coords_to_screen(self, x, y):
        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        
        screen_x = screen_center_x + (x - w_center_x) * self.cell
        screen_y = screen_center_y + (y - w_center_y) * self.cell
        
        return screen_x, screen_y
    
    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()
        
        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=False)
        
        if self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=3)
        else:
            min_x, min_y, max_x, max_y = -40, -40, 40, 40
        
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
        
    
    def input_fields(self):
        input_panel = ttk.LabelFrame(self.root, padding=10, text="Ввод координат")
        input_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def draw_section(self):
        self.circle = None
        x1 = int(self.ax_entry.get())
        y1 = int(self.ay_entry.get())
        x2 = int(self.bx_entry.get())
        y2 = int(self.by_entry.get())
            
        point_a = Point(x1, y1)
        point_b = Point(x2, y2)
        self.section = Section(point_a, point_b)


        self.draw_grid()

        x1, y1 = self.coords_to_screen(self.section.a.x, self.section.a.y)
        x2, y2 = self.coords_to_screen(self.section.b.x, self.section.b.y)
            
        self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
            
        self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, fill='black', outline='black')
        self.canvas.create_oval(x2-3, y2-3, x2+3, y2+3, fill='black', outline='black')
        
        self.rasterization_section()

    def algorithm_brezenhem(self, x0, y0, x1, y1):
        pixels = []
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        
        err = dx - dy
        
        x, y = x0, y0
        
        while True:
            pixels.append((x, y))
            
            if x == x1 and y == y1:
                break
                
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x += sx
                
            if e2 < dx:
                err += dx
                y += sy
                
        return pixels

    def rasterization_section(self):
        if not self.section:
            return
            
        pixels = self.algorithm_brezenhem(self.section.a.x, self.section.a.y, self.section.b.x, self.section.b.y)
        
        for x, y in pixels:
            screen_x, screen_y = self.coords_to_screen(x, y)

            point_size = 2

            self.canvas.create_oval(screen_x - point_size, screen_y - point_size,
                screen_x + point_size, screen_y + point_size, fill ='black', width=2)

    def clear_all(self):
        self.section = None
        self.draw_grid()
    

if __name__ == "__main__":
    window = tk.Tk()
    app = Fill_area(window)
    window.mainloop()