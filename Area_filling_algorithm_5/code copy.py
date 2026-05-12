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

class Rasterization_section:
    def __init__(self, root):
        self.root = root
        self.root.title("Растеризация многоугольников")
        self.root.geometry("1050x650")

        self.cell = 30
        self.section = None
        self.circle = None

        self.polygon_mode = False
        self.vertices_world = []
        self.polygon_world = []
        self.y_buckets = {}
        self.edge_pixels = []
        self.y_min = None
        self.y_max = None
        self.step_state = 0
        
        # Для динамических полей ввода вершин
        self.vertex_entries = []
        self.num_vertices_var = tk.IntVar(value=5)

        self.canvas_width = 650
        self.canvas_height = 650

        self.input_fields()
        self.create_vertex_inputs()

        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.draw_grid()

    def get_center(self):
        if self.polygon_mode and self.vertices_world:
            xs = [v[0] for v in self.vertices_world]
            ys = [v[1] for v in self.vertices_world]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            indent = 3
            min_x -= indent
            min_y -= indent
            max_x += indent
            max_y += indent
            center_w_x = (min_x + max_x) / 2
            center_w_y = (min_y + max_y) / 2
        elif self.section:
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
        screen_y = screen_center_y - (y - w_center_y) * self.cell
        return screen_x, screen_y
    
    def half_coords_to_screen(self, x, y):
        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        screen_x = screen_center_x + (x / 2 - w_center_x) * self.cell
        screen_y = screen_center_y - (y / 2 - w_center_y) * self.cell
        return screen_x, screen_y

    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width,
                                height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=False)

        if self.polygon_mode and self.vertices_world:
            xs = [v[0] for v in self.vertices_world]
            ys = [v[1] for v in self.vertices_world]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            indent = 5
            min_x -= indent
            min_y -= indent
            max_x += indent
            max_y += indent
        elif self.circle:
            min_x, min_y, max_x, max_y = self.circle.get_borders(indent=5)
        elif self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=5)
        else:
            min_x, min_y, max_x, max_y = -40, -40, 40, 40

        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        half_width_w = (self.canvas_width / 2) / self.cell
        half_height_w = (self.canvas_height / 2) / self.cell

        start_x = math.floor(w_center_x - half_width_w) - 1
        end_x = math.ceil(w_center_x + half_width_w) + 1
        start_y = math.floor(w_center_y - half_height_w) - 1
        end_y = math.ceil(w_center_y + half_height_w) + 1

        for x in range(start_x, end_x + 1):
            screen_x, _ = self.coords_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                color = 'black' if x == 0 else 'lightgray'
                self.canvas.create_line(screen_x, 0, screen_x, self.canvas_height, fill=color, tags='grid')

        for y in range(start_y, end_y + 1):
            _, screen_y = self.coords_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                color = 'black' if y == 0 else 'lightgray'
                self.canvas.create_line(0, screen_y, self.canvas_width, screen_y, fill=color, tags='grid')

        for x in range(start_x, end_x + 1):
            if x == 0: continue
            screen_x, screen_y = self.coords_to_screen(x, 0)
            if 0 <= screen_x <= self.canvas_width:
                self.canvas.create_text(screen_x, screen_y + 15, text=str(x),
                                        fill='gray', font=('Arial', 9), tags='grid')
                
        for y in range(start_y, end_y + 1):
            if y == 0: continue
            screen_x, screen_y = self.coords_to_screen(0, y)
            if 0 <= screen_y <= self.canvas_height:
                self.canvas.create_text(screen_x - 15, screen_y, text=str(y),
                                        fill='gray', font=('Arial', 9), tags='grid')
        screen_x, screen_y = self.coords_to_screen(0, 0)
        if 0 <= screen_x <= self.canvas_width and 0 <= screen_y <= self.canvas_height:
            self.canvas.create_text(screen_x + 5, screen_y + 15, text="0",
                                    fill='gray', font=('Arial', 10, 'bold'), tags='grid')

    def input_fields(self):
        right_panel = ttk.Frame(self.root)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=1, pady=1)

        canvas = tk.Canvas(right_panel, width=350)
        canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Выбор количества вершин
        vertex_count_frame = ttk.LabelFrame(self.scrollable_frame, padding=10, text="Настройки многоугольника")
        vertex_count_frame.pack(fill=tk.X, pady=5)

        ttk.Label(vertex_count_frame, text="Количество вершин (3-20):").pack(anchor='w')
        num_spin = ttk.Spinbox(vertex_count_frame, from_=3, to=20, textvariable=self.num_vertices_var, width=5)
        num_spin.pack(anchor='w', pady=3)
        num_spin.bind('<FocusOut>', lambda e: self.update_vertex_inputs())
        num_spin.bind('<Return>', lambda e: self.update_vertex_inputs())

        ttk.Button(vertex_count_frame, text="Обновить", command=self.update_vertex_inputs).pack(anchor='w', pady=3)

        # Контейнер для полей вершин
        self.vertex_inputs_frame = ttk.LabelFrame(self.scrollable_frame, padding=10, text="Координаты вершин")
        self.vertex_inputs_frame.pack(fill=tk.X, pady=5)

        # Кнопки управления
        btn_frame = ttk.Frame(self.scrollable_frame)
        btn_frame.pack(fill=tk.X, pady=1)

        ttk.Button(btn_frame, text="1. Создание многоугольника", command=self.create_polygon_from_inputs).pack(anchor='w', pady=2)

        # Кнопки шагов растеризации
        self.btn_poly_step1 = ttk.Button(btn_frame, text="2. Растеризация рёбер", command=self.polygon_step1, state=tk.DISABLED)
        self.btn_poly_step1.pack(anchor='w', pady=2)
        self.btn_poly_step2 = ttk.Button(btn_frame, text="3. Сортировка списков", command=self.polygon_step2, state=tk.DISABLED)
        self.btn_poly_step2.pack(anchor='w', pady=2)
        self.btn_poly_step3 = ttk.Button(btn_frame, text="4. Заливка", command=self.polygon_step3, state=tk.DISABLED)
        self.btn_poly_step3.pack(anchor='w', pady=2)
        
        ttk.Button(btn_frame, text="Очистить всё", command=self.clear_all).pack(anchor='w', pady=15)



    def create_vertex_inputs(self): # поля ввода для вершин многоугольника
        for widget in self.vertex_inputs_frame.winfo_children():
            widget.destroy()
        self.vertex_entries = []

        num_vertices = self.num_vertices_var.get()
        my_coordinates = [
            (1, 1),
            (2, 6),
            (4, 2), 
            (6, 5),
            (8, 1),
        ]

        for i in range(num_vertices):
            frame = ttk.Frame(self.vertex_inputs_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"V{i+1}:").pack(side=tk.LEFT, padx=(0,5))
            
            x_entry = ttk.Entry(frame, width=5)
            x_val = my_coordinates[i][0] if i < len(my_coordinates) else 0
            x_entry.insert(0, str(x_val))
            x_entry.pack(side=tk.LEFT, padx=2)
            
            ttk.Label(frame, text=",").pack(side=tk.LEFT)
            
            y_entry = ttk.Entry(frame, width=5)
            y_val = my_coordinates[i][1] if i < len(my_coordinates) else 0
            y_entry.insert(0, str(y_val))
            y_entry.pack(side=tk.LEFT, padx=2)
            
            self.vertex_entries.append((x_entry, y_entry))


    def update_vertex_inputs(self): # обновляет количество полей ввода при изменении числа вершин
        try:
            num = self.num_vertices_var.get()
            if num < 3:
                self.num_vertices_var.set(3)
            elif num > 20:
                self.num_vertices_var.set(20)
            self.create_vertex_inputs()
        except:
            self.num_vertices_var.set(3)
            self.create_vertex_inputs()



    def create_polygon_from_inputs(self): # прямоугольник из введённых координат
        self.clear_all()
        self.polygon_mode = True
        
        self.vertices_world = []
        for x_entry, y_entry in self.vertex_entries:
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                self.vertices_world.append((x, y))
            except ValueError:
                continue
        
        self.polygon_world = self.vertices_world + [self.vertices_world[0]]
        self.y_buckets = {}
        self.edge_pixels = []
        self.y_min = None
        self.y_max = None
        self.step_state = 0

        self.draw_grid()
        screen_vertices = [self.coords_to_screen(x, y) for x, y in self.vertices_world]
        self.canvas.create_polygon(screen_vertices, outline='black', fill='', width=2, tags='outline')

        self.btn_poly_step1.config(state=tk.NORMAL)
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.DISABLED)


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
        pixels = self.algorithm_brezenhem(self.section.a.x, self.section.a.y,
                                          self.section.b.x, self.section.b.y)
        for x, y in pixels:
            screen_x, screen_y = self.coords_to_screen(x, y)
            point_size = 2
            self.canvas.create_oval(screen_x - point_size, screen_y - point_size,
                                    screen_x + point_size, screen_y + point_size,
                                    fill='black', width=2, tags='pixel')

    def clear_all(self):
        self.section = None
        self.circle = None
        self.polygon_mode = False
        self.vertices_world = []
        self.polygon_world = []
        self.y_buckets.clear()
        self.edge_pixels.clear()
        self.y_min = None
        self.y_max = None
        self.step_state = 0
        self.btn_poly_step1.config(state=tk.DISABLED)
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.DISABLED)
        self.canvas.delete('pixel', 'fill', 'outline')
        self.draw_grid()

    def rasterize_edge_brez(self, x1, y1, x2, y2):
        x1_scaled = int(round(x1 * 2))
        y1_scaled = int(round(y1 * 2))
        x2_scaled = int(round(x2 * 2))
        y2_scaled = int(round(y2 * 2))

        dx = abs(x2_scaled - x1_scaled)
        dy = abs(y2_scaled - y1_scaled)
        sx = 1 if x1_scaled < x2_scaled else -1
        sy = 1 if y1_scaled < y2_scaled else -1
        err = dx - dy

        x, y = x1_scaled, y1_scaled
        while True:
            self.y_buckets.setdefault(y, []).append(x)
            screen_x, screen_y = self.half_coords_to_screen(x, y)
            point_size = 1.5
            self.canvas.create_oval(screen_x - point_size, screen_y - point_size,
                                    screen_x + point_size, screen_y + point_size,
                                    fill='red', outline='red', tags='pixel')
            self.edge_pixels.append((x, y))
            if x == x2_scaled and y == y2_scaled:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def polygon_step1(self):
        if not self.polygon_mode:
            return
        self.step_state = 1
        self.canvas.delete('pixel')
        self.y_buckets.clear()
        self.edge_pixels.clear()

        for i in range(len(self.polygon_world) - 1):
            x1, y1 = self.polygon_world[i]
            x2, y2 = self.polygon_world[i+1]
            if y1 == y2:
                continue
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            self.rasterize_edge_brez(x1, y1, x2, y2)

        if self.y_buckets:
            self.y_min = min(self.y_buckets.keys())
            self.y_max = max(self.y_buckets.keys())
        else:
            self.y_min = self.y_max = 0

        self.btn_poly_step2.config(state=tk.NORMAL)
        self.btn_poly_step1.config(state=tk.DISABLED)

    def polygon_step2(self):
        if self.step_state != 1:
            return
        self.step_state = 2
        for y in self.y_buckets:
            self.y_buckets[y] = sorted(set(self.y_buckets[y]))
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.NORMAL)

    def polygon_step3(self):
        if self.step_state != 2:
            return
        self.step_state = 3
        for y in range(self.y_min, self.y_max + 1):
            if y not in self.y_buckets:
                continue
            x_list = self.y_buckets[y]
            for i in range(0, len(x_list) - 1, 2):
                x_start = x_list[i]
                x_end = x_list[i+1]
                for x in range(x_start, x_end + 1):
                    screen_x, screen_y = self.half_coords_to_screen(x, y)
                    self.canvas.create_rectangle(screen_x - self.cell/4, screen_y - self.cell/4,
                                                 screen_x + self.cell/4, screen_y + self.cell/4,
                                                 fill='pink', outline='red', stipple='gray50', tags='fill')
        self.canvas.tag_raise('outline')
        self.btn_poly_step3.config(state=tk.DISABLED)

if __name__ == "__main__":
    window = tk.Tk()
    app = Rasterization_section(window)
    window.mainloop()