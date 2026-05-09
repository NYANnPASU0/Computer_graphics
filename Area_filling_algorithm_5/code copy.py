import tkinter as tk
from tkinter import ttk, filedialog
import math
import os

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
        min_x -= indent; min_y -= indent
        max_x += indent; max_y += indent
        return min_x, min_y, max_x, max_y

class Rasterization_section:
    def __init__(self, root):
        self.root = root
        self.root.title("Растеризация отрезков")
        self.root.geometry("950x700")

        self.cell = 30
        self.section = None
        self.circle = None

        # Для многоугольника
        self.polygon_mode = False
        self.vertices_world = []
        self.polygon_world = []
        self.y_buckets = {}
        self.edge_pixels = []
        self.y_min = None
        self.y_max = None
        self.step_state = 0

        self.canvas_width = 700
        self.canvas_height = 700

        self.input_fields()
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
            min_x -= indent; min_y -= indent
            max_x += indent; max_y += indent
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
            min_x -= indent; min_y -= indent
            max_x += indent; max_y += indent
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
        input_panel = ttk.LabelFrame(self.root, padding=10, text="Управление")
        input_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # 🔴 Кнопка загрузки из файла вместо hardcoded-полигона
        ttk.Button(input_panel, text="Загрузить многоугольник из файла", 
                  command=self.load_file).pack(anchor='w', pady=3)

        self.btn_poly_step1 = ttk.Button(input_panel, text="1. Растеризация рёбер", 
                                        command=self.polygon_step1, state=tk.DISABLED)
        self.btn_poly_step1.pack(anchor='w', pady=2)

        self.btn_poly_step2 = ttk.Button(input_panel, text="2. Сортировка списков", 
                                        command=self.polygon_step2, state=tk.DISABLED)
        self.btn_poly_step2.pack(anchor='w', pady=2)

        self.btn_poly_step3 = ttk.Button(input_panel, text="3. Заливка", 
                                        command=self.polygon_step3, state=tk.DISABLED)
        self.btn_poly_step3.pack(anchor='w', pady=2)
        
        ttk.Button(input_panel, text="Очистить всё", 
                  command=self.clear_all).pack(anchor='w', pady=10)

    def algorithm_brezenhem(self, x0, y0, x1, y1):
        pixels = []
        dx = abs(x1 - x0); dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            pixels.append((x, y))
            if x == x1 and y == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x += sx
            if e2 < dx: err += dx; y += sy
        return pixels

    def rasterize_edge_brez(self, x1, y1, x2, y2):
        """Растеризация ребра с масштабированием ×2"""
        x1_s = int(round(x1 * 2)); y1_s = int(round(y1 * 2))
        x2_s = int(round(x2 * 2)); y2_s = int(round(y2 * 2))
        dx = abs(x2_s - x1_s); dy = abs(y2_s - y1_s)
        sx = 1 if x1_s < x2_s else -1; sy = 1 if y1_s < y2_s else -1
        err = dx - dy
        x, y = x1_s, y1_s
        while True:
            self.y_buckets.setdefault(y, []).append(x)
            screen_x, screen_y = self.half_coords_to_screen(x, y)
            self.canvas.create_oval(screen_x - 1.5, screen_y - 1.5,
                                    screen_x + 1.5, screen_y + 1.5,
                                    fill='red', outline='red', tags='pixel')
            self.edge_pixels.append((x, y))
            if x == x2_s and y == y2_s: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x += sx
            if e2 < dx: err += dx; y += sy

    def polygon_step1(self):
        if not self.polygon_mode: return
        self.step_state = 1
        self.canvas.delete('pixel')
        self.y_buckets.clear()
        self.edge_pixels.clear()

        for i in range(len(self.polygon_world) - 1):
            x1, y1 = self.polygon_world[i]
            x2, y2 = self.polygon_world[i+1]
            if y1 == y2: continue  # пропускаем горизонтальные
            if y1 > y2: x1, x2 = x2, x1; y1, y2 = y2, y1
            self.rasterize_edge_brez(x1, y1, x2, y2)

        if self.y_buckets:
            self.y_min = min(self.y_buckets.keys())
            self.y_max = max(self.y_buckets.keys())
        else:
            self.y_min = self.y_max = 0

        self.btn_poly_step2.config(state=tk.NORMAL)
        self.btn_poly_step1.config(state=tk.DISABLED)
        print(f"Шаг 1: {len(self.edge_pixels)} пикселей")

    def polygon_step2(self):
        if self.step_state != 1: return
        self.step_state = 2
        for y in self.y_buckets:
            self.y_buckets[y] = sorted(set(self.y_buckets[y]))
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.NORMAL)
        print("Шаг 2: сортировка завершена")

    def polygon_step3(self):
        if self.step_state != 2: return
        self.step_state = 3
        for y in range(self.y_min, self.y_max + 1):
            if y not in self.y_buckets: continue
            x_list = self.y_buckets[y]
            for i in range(0, len(x_list) - 1, 2):
                x_start, x_end = x_list[i], x_list[i+1]
                for x in range(x_start, x_end + 1):
                    screen_x, screen_y = self.half_coords_to_screen(x, y)
                    self.canvas.create_rectangle(
                        screen_x - self.cell/4, screen_y - self.cell/4,
                        screen_x + self.cell/4, screen_y + self.cell/4,
                        fill='pink', outline='', tags='fill'
                    )
        self.canvas.tag_raise('outline')
        self.btn_poly_step3.config(state=tk.DISABLED)
        print("Шаг 3: заливка завершена")

    # 🔴 НОВЫЕ МЕТОДЫ ДЛЯ ЗАГРУЗКИ ИЗ ФАЙЛА

    def read_data_from_file(self, filepath):
        """Чтение вершин многоугольника из файла"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parts = content.strip().split('\n\n')
        polygon_lines = parts[0].strip().split('\n')
        vertices = []
        
        for line in polygon_lines:
            line = line.strip()
            if not line: continue
            coords = line.split()
            x, y = int(coords[0]), int(coords[1])
            vertices.append((x, y))
        
        if len(vertices) < 3:
            print("⚠️ Многоугольник должен иметь минимум 3 вершины")
            return
        
        # Инициализация данных многоугольника
        self.polygon_mode = True
        self.vertices_world = vertices
        self.polygon_world = vertices + [vertices[0]]  # замкнутый контур
        self.y_buckets = {}
        self.edge_pixels = []
        self.y_min = self.y_max = None
        self.step_state = 0

        # Перерисовка
        self.draw_grid()
        self.draw_polygon()
        self.btn_poly_step1.config(state=tk.NORMAL)
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.DISABLED)
        print(f"✅ Загружено {len(vertices)} вершин")

    def draw_polygon(self):
        """Отрисовка контура многоугольника"""
        if not self.polygon_mode or not self.vertices_world:
            return
        
        # Удаляем старый контур
        self.canvas.delete('outline')
        
        # Рисуем рёбра
        for i in range(len(self.vertices_world)):
            x1, y1 = self.vertices_world[i]
            x2, y2 = self.vertices_world[(i+1) % len(self.vertices_world)]
            sx1, sy1 = self.coords_to_screen(x1, y1)
            sx2, sy2 = self.coords_to_screen(x2, y2)
            self.canvas.create_line(sx1, sy1, sx2, sy2, 
                                   fill='purple', width=2, tags='outline')

    def load_file(self):
        """Загрузка многоугольника из файла"""
        try:
            from generate_file import select_existing_file
            filepath = select_existing_file(self.root)
        except ImportError:
            filepath = filedialog.askopenfilename(
                title="Выберите файл с многоугольником",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialdir=os.path.join(os.getcwd(), "files")
            )
        
        if filepath:
            self.clear_all()  # сброс предыдущих данных
            self.read_data_from_file(filepath)

    def clear_all(self):
        self.section = None
        self.polygon_mode = False
        self.vertices_world = []
        self.polygon_world = []
        self.y_buckets.clear()
        self.edge_pixels.clear()
        self.step_state = 0
        self.btn_poly_step1.config(state=tk.DISABLED)
        self.btn_poly_step2.config(state=tk.DISABLED)
        self.btn_poly_step3.config(state=tk.DISABLED)
        self.canvas.delete('pixel', 'fill', 'outline')
        self.draw_grid()

if __name__ == "__main__":
    window = tk.Tk()
    app = Rasterization_section(window)
    window.mainloop()