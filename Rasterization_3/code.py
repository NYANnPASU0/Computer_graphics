import tkinter as tk
from tkinter import ttk
import math

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Section:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

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

class Circle:
    def __init__(self, center: Point, radius: int):
        self.center = center
        self.radius = radius

    def get_borders(self, indent: int = 3):
        min_x = self.center.x - self.radius - indent
        min_y = self.center.y - self.radius - indent
        max_x = self.center.x + self.radius + indent
        max_y = self.center.y + self.radius + indent
        return min_x, min_y, max_x, max_y
        


class Rasterization_section:
    def __init__(self, root):
        self.root = root
        self.root.title("Растеризация отрезка")
        self.root.geometry("950x700")
        
        self.cell = 30
        self.section = None
        self.circle = None
        
        self.canvas_width = 700
        self.canvas_height = 700
        
        self.input_fields()
        
        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.draw_grid()
    
    def get_center(self):
        if self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=2)
            center_world_x = (min_x + max_x) / 2
            center_world_y = (min_y + max_y) / 2
        elif self.circle:
            min_x, min_y, max_x, max_y = self.circle.get_borders(indent=2)
            center_world_x = (min_x + max_x) / 2
            center_world_y = (min_y + max_y) / 2
        else:
            center_world_x = 0
            center_world_y = 0
        
        screen_center_x = self.canvas_width // 2
        screen_center_y = self.canvas_height // 2
        
        return center_world_x, center_world_y, screen_center_x, screen_center_y
    
    def world_to_screen(self, x, y):
        world_center_x, world_center_y, screen_center_x, screen_center_y = self.get_center()
        
        screen_x = screen_center_x + (x - world_center_x) * self.cell
        screen_y = screen_center_y - (y - world_center_y) * self.cell
        
        return screen_x, screen_y
    
    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()
        
        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        if self.circle:
            min_x, min_y, max_x, max_y = self.circle.get_borders(indent=3)
        elif self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=3)
        else:
            min_x, min_y, max_x, max_y = -40, -40, 40, 40
        
        world_center_x, world_center_y, screen_center_x, screen_center_y = self.get_center()
        
        for x in range(-self.canvas_height, self.canvas_height):
            screen_x, _ = self.world_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                if x == 0:
                    color = 'black'
                else:
                    color = 'lightgray'
                self.canvas.create_line(screen_x, 0, screen_x, self.canvas_height, fill=color)
        
        for y in range(-self.canvas_width, self.canvas_width):
            _, screen_y = self.world_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                if y == 0:
                    color = 'black'
                else:
                    color = 'lightgray'
                self.canvas.create_line(0, screen_y, self.canvas_width, screen_y, fill=color)
        
        for x in range(-self.canvas_height, self.canvas_height):
            if x == 0:
                continue
            screen_x, screen_y = self.world_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                self.canvas.create_text(screen_x, screen_y + 15, text=str(x), 
                                       fill='gray', font=('Arial', 9))
        
        for y in range(-self.canvas_width, self.canvas_width):
            if y == 0:
                continue
            screen_x, screen_y = self.world_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                self.canvas.create_text(screen_x - 15, screen_y, text=str(y), 
                                       fill='gray', font=('Arial', 9))
        
        screen_x, screen_y = self.world_to_screen(0, 0)
        if 0 <= screen_x <= self.canvas_width and 0 <= screen_y <= self.canvas_height:
            self.canvas.create_text(screen_x + 5, screen_y + 15, text="0",
                                   fill='gray', font=('Arial', 10, 'bold'))
        
    
    def input_fields(self):
        input_panel = ttk.LabelFrame(self.root, padding=10, text="Ввод координат")
        input_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        ttk.Label(input_panel, text="Отрезок", font=('Arial', 10, 'bold underline')).pack(anchor=tk.W, pady=(10,0))

        #A
        ttk.Label(input_panel, text="Точка A:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5,0))

        frame_a = ttk.Frame(input_panel)
        frame_a.pack(fill=tk.X, pady=5)

        ttk.Label(frame_a, text="X:").pack(side=tk.LEFT, padx=5)
        self.ax_entry = ttk.Entry(frame_a, width=10)
        self.ax_entry.pack(side=tk.LEFT, padx=5)
        self.ax_entry.insert(0, "0")

        ttk.Label(frame_a, text="Y:").pack(side=tk.LEFT, padx=5)
        self.ay_entry = ttk.Entry(frame_a, width=10)
        self.ay_entry.pack(side=tk.LEFT, padx=5)
        self.ay_entry.insert(0, "0")

        #B
        ttk.Label(input_panel, text="Точка B:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(10,0))

        frame_b = ttk.Frame(input_panel)
        frame_b.pack(fill=tk.X, pady=5)

        ttk.Label(frame_b, text="X:").pack(side=tk.LEFT, padx=5)
        self.bx_entry = ttk.Entry(frame_b, width=10)
        self.bx_entry.pack(side=tk.LEFT, padx=5)
        self.bx_entry.insert(0, "5")

        ttk.Label(frame_b, text="Y:").pack(side=tk.LEFT, padx=5)
        self.by_entry = ttk.Entry(frame_b, width=10)
        self.by_entry.pack(side=tk.LEFT, padx=5)
        self.by_entry.insert(0, "5")

        ttk.Label(input_panel, text="Круг", font=('Arial', 10, 'bold underline')).pack(anchor=tk.W, pady=(10,0))

        frame_r = ttk.Frame(input_panel)
        frame_r.pack(fill=tk.X, pady=5)

        ttk.Label(frame_r, text="Радиус r:").pack(side=tk.LEFT, padx=5)
        self.radius_entry = ttk.Entry(frame_r, width=10)
        self.radius_entry.pack(side=tk.LEFT, padx=5)
        self.radius_entry.insert(0, "5")


        ttk.Label(input_panel, text="Центр окружности", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(10,0))

        frame_center = ttk.Frame(input_panel)
        frame_center.pack(fill=tk.X, pady=5)

        ttk.Label(frame_center, text="X:").pack(side=tk.LEFT, padx=5)
        self.cx_entry = ttk.Entry(frame_center, width=10)
        self.cx_entry.pack(side=tk.LEFT, padx=5)
        self.cx_entry.insert(0, "0")

        ttk.Label(frame_center, text="Y:").pack(side=tk.LEFT, padx=5)
        self.cy_entry = ttk.Entry(frame_center, width=10)
        self.cy_entry.pack(side=tk.LEFT, padx=5)
        self.cy_entry.insert(0, "0")

        ttk.Button(input_panel, text="Нарисовать отрезок", command=self.draw_section).pack(anchor='w', pady=3)
        ttk.Button(input_panel, text="Нарисовать круг", command=self.draw_circle).pack(anchor='w', pady=3)
        ttk.Button(input_panel, text="Очистить", command=self.clear_all).pack(anchor='w', pady=3)

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

        x1, y1 = self.world_to_screen(self.section.a.x, self.section.a.y)
        x2, y2 = self.world_to_screen(self.section.b.x, self.section.b.y)
            
        self.canvas.create_line(x1, y1, x2, y2, fill='red', width=3)
            
        self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, fill='black', outline='darkblue')
        self.canvas.create_oval(x2-3, y2-3, x2+3, y2+3, fill='black', outline='darkblue')
        
        self.rasterization_section()

    def rasterization_section(self):
        

    def clear_all(self):
        self.section = None
        self.circle = None
        self.draw_grid()

    def draw_circle(self):
        self.section = None
        cx = int(self.cx_entry.get())
        cy = int(self.cy_entry.get())
        r = int(self.radius_entry.get())
            
        self.circle = Circle(Point(cx, cy), r)

        self.draw_grid()

        cx, cy = self.world_to_screen(self.circle.center.x, self.circle.center.y)
        r_pixels = r * self.cell

        self.canvas.create_oval(cx-r_pixels, cy+r_pixels, cx+r_pixels, cy-r_pixels, outline='red', width=3)


if __name__ == "__main__":
    window = tk.Tk()
    app = Rasterization_section(window)
    window.mainloop()