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
    

class Polygon:
    def __init__(self, points: list):
        self.points = points

        all_x = [p.x for p in points]
        all_y = [p.y for p in points]

        self.x_min = min(all_x)
        self.x_max = max(all_x)
        self.y_min = min(all_y)
        self.y_max = max(all_y)

        self.edges = []
        self.vertices_world = [(p.x, p.y) for p in points]
        self.polygon_world = self.vertices_world + [self.vertices_world[0]]

class Fill_area:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм заполнения областей")
        self.root.geometry("950x700")
        
        self.cell = 30
        self.section = None
        self.polygon = None

        self.polygon_points = []
        self.edge_pixels = []
        self.lbl_fill = {}
        self.canvas_width = 700
        self.canvas_height = 700
        
        self.input_fields()
        
        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        self.draw_grid()
    
    def get_center(self):
        if not self.polygon_points:
            return 0, 0, self.canvas_width // 2, self.canvas_height // 2
        
        xs = [p.x for p in self.polygon_points]
        ys = [p.y for p in self.polygon_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        indent = 3
        min_x -= indent
        max_x += indent
        min_y -= indent
        max_y += indent
        
        center_w_x = (min_x + max_x) / 2
        center_w_y = (min_y + max_y) / 2
        
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
        
        if not self.polygon_points:
            min_x, min_y, max_x, max_y = -40, -40, 40, 40
        else:
            xs = [p.x for p in self.polygon_points]
            ys = [p.y for p in self.polygon_points]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            indent = 5
            min_x -= indent; max_x += indent
            min_y -= indent; max_y += indent
        
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
        input_panel = ttk.LabelFrame(self.root, padding=10, text="")
        input_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        ttk.Button(input_panel, text="Выбрать многоугольник", 
                  command=self.load_file).pack(anchor='w', pady=3)
        
        self.btn_step1 = ttk.Button(input_panel, text="1. Растеризация рёбер", 
                                   command=self.raster_edges, state=tk.DISABLED)
        self.btn_step1.pack(anchor='w', pady=2)
        
        self.btn_step2 = ttk.Button(input_panel, text="2. Сортировка списков", 
                                   command=self.sort_list, state=tk.DISABLED)
        self.btn_step2.pack(anchor='w', pady=2)
        
        self.btn_step3 = ttk.Button(input_panel, text="3. Заливка", 
                                   command=self.fill_polygon, state=tk.DISABLED)
        self.btn_step3.pack(anchor='w', pady=2)
        
        ttk.Button(input_panel, text="Очистить всё", 
                  command=self.clear_all).pack(anchor='w', pady=10)
        

        ttk.Label(input_panel, text="Информация:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(15, 5))
            
        log_frame = ttk.Frame(input_panel)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
        self.text_log = tk.Text(log_frame, height=10, width=25, state=tk.DISABLED, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(log_frame, command=self.text_log.yview)
            
        self.text_log.configure(yscrollcommand=scrollbar.set)
            
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
    

    def raster_edges(self):
        self.canvas.delete('pixel')
        self.lbl_fill.clear()


    def sort_list(self):
        self.text_log.config(state=tk.NORMAL)
        self.text_log.delete('1.0', tk.END)


    def fill_polygon(self):
        self.canvas.delete('fill')


    def clear_all(self):
        self.section = None
        self.polygon = None
        self.draw_grid()


    def read_data_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.lines = []
        self.polygon = None
        
        # strip() удаляет пробелы и переносы в начале и конце
        # split('\n\n') разделяет текст на части там, где есть пустая строка
        parts = content.strip().split('\n\n')
        
        # вершины многоугольника
        # split('\n') разбивает на отдельные строки
        polygon_lines = parts[0].strip().split('\n')
        polygon_points = []
        
        for line in polygon_lines:
            line = line.strip()
            if not line:
                continue
            
            coords = line.split() #разбиваем строку по пробелам
            
            x = int(coords[0])
            y = int(coords[1])
            polygon_points.append(Point(x, y))
        
        self.polygon = Polygon(polygon_points)

        self.draw_polygon()

    def draw_polygon(self):
        if self.polygon and len(self.polygon.points) >= 3:
            points = self.polygon.points
            n = len(points)

            for i in range(n):
                p1 = points[i]
                p2 = points[(i+1)%n]

                x1, y1 = self.coords_to_screen(p1.x, p1.y)
                x2, y2 = self.coords_to_screen(p2.x, p2.y)

                self.canvas.create_line(x1, y1, x2, y2, fill='purple', width=2.3, tags='polygon')
    
    def load_file(self):
        from generate_file import select_existing_file 
            
        filepath = select_existing_file(self.root)
        if filepath:
            self.read_data_from_file(filepath)

        self.btn_step1.config(state=tk.NORMAL) 


if __name__ == "__main__":
    window = tk.Tk()
    app = Fill_area(window)
    window.mainloop()