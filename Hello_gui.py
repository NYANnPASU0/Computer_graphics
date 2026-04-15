import tkinter as tk
from math import floor, ceil

class RasterPolygonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Растеризация многоугольника - алгоритм со списком рёберных точек")

        self.cell_size = 25  # размер ячейки сетки
        self.offset_x = 80
        self.offset_y = 50
        
        self.canvas_width = 850
        self.canvas_height = 750

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(pady=10)

        # Панель с кнопками
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_step1 = tk.Button(btn_frame, text="1. Растеризация рёбер", command=self.step1, width=20)
        self.btn_step1.pack(side=tk.LEFT, padx=5)

        self.btn_step2 = tk.Button(btn_frame, text="2. Сортировка списков", command=self.step2, width=20)
        self.btn_step2.pack(side=tk.LEFT, padx=5)

        self.btn_step3 = tk.Button(btn_frame, text="3. Заливка", command=self.step3, width=20)
        self.btn_step3.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(btn_frame, text="Сброс", command=self.reset, width=15)
        self.btn_reset.pack(side=tk.LEFT, padx=20)

        self.label_info = tk.Label(root, text="Нажмите 'Шаг 1' - растеризация рёбер", font=("Arial", 10))
        self.label_info.pack()

        # Вершины многоугольника (в координатах сетки)
        # Y координаты теперь идут снизу вверх: 0 внизу, 24 вверху
        self.vertices_grid = [
            (8, 16),   # вершина 0 (было 8,8)
            (24, 18),  # вершина 1 (было 24,6)
            (27, 8),   # вершина 2 (было 27,16)
            (19, 0),   # вершина 3 (было 19,24)
            (12, 5),   # вершина 4 (было 12,19)
            (6, 10)    # вершина 5 (было 6,14)
        ]
        
        # Преобразование в пиксельные координаты для отрисовки контура
        self.vertices_pixel = [(self.grid_to_pixel_x(x), self.grid_to_pixel_y(y)) 
                                for x, y in self.vertices_grid]

        # Этап 1: Для каждой y-координаты список x-координат
        self.y_buckets = {}
        self.edge_pixels = []
        
        self.y_min = None
        self.y_max = None

        self.draw_grid()
        self.draw_outline()

    def grid_to_pixel_x(self, grid_x):
        """Преобразует координату сетки X в пиксельную (центр узла сетки)"""
        return self.offset_x + grid_x * self.cell_size

    def grid_to_pixel_y(self, grid_y):
        """Преобразует координату сетки Y в пиксельную (центр узла сетки)"""
        # Y координата: 0 внизу, максимальное значение вверху
        max_y = 25  # максимальная Y координата на сетке
        return self.offset_y + (max_y - grid_y) * self.cell_size

    def draw_grid(self):
        """Рисует сетку"""
        max_y = 25  # максимальная Y координата
        
        # Рисуем вертикальные линии сетки
        for i in range(0, 35):
            x_pixel = self.offset_x + i * self.cell_size
            self.canvas.create_line(x_pixel, self.offset_y, 
                                    x_pixel, self.canvas_height - self.offset_y + 30, 
                                    fill="lightgray", width=1)
            # Подписи X
            if i % 5 == 0:
                self.canvas.create_text(x_pixel, self.offset_y - 10, 
                                        text=str(i), font=("Arial", 8))

        # Рисуем горизонтальные линии сетки
        for i in range(0, max_y + 1):
            y_pixel = self.grid_to_pixel_y(i)
            self.canvas.create_line(self.offset_x - 20, y_pixel,
                                    self.canvas_width - self.offset_x + 20, y_pixel,
                                    fill="lightgray", width=1)
            # Подписи Y (снизу вверх: 0, 5, 10, 15, 20, 25)
            if i % 5 == 0:
                self.canvas.create_text(self.offset_x - 15, y_pixel,
                                        text=str(i), font=("Arial", 8))

    def draw_outline(self):
        """Рисует контур многоугольника чёрным цветом по узлам сетки"""
        # Рисуем линии между вершинами (по центрам узлов)
        for i in range(len(self.vertices_pixel)):
            x1, y1 = self.vertices_pixel[i]
            x2, y2 = self.vertices_pixel[(i + 1) % len(self.vertices_pixel)]
            self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
        
        # Отмечаем вершины
        for x, y in self.vertices_pixel:
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, 
                                   fill='black', outline='black')

    def add_boundary_point(self, grid_x, grid_y):
        """Рисует граничный пиксель как ТОЧКУ на пересечении сетки"""
        x_pixel = self.grid_to_pixel_x(grid_x)
        y_pixel = self.grid_to_pixel_y(grid_y)
        
        # Рисуем маленькую чёрную точку в узле сетки
        self.canvas.create_oval(x_pixel - 2, y_pixel - 2, 
                               x_pixel + 2, y_pixel + 2,
                               fill='black', outline='black', tags="boundary")
        
        self.edge_pixels.append((grid_x, grid_y))

    def add_filled_cell(self, grid_x, grid_y):
        """Закрашивает внутренний пиксель (ячейку)"""
        x_pixel = self.grid_to_pixel_x(grid_x) - self.cell_size//2
        y_pixel = self.grid_to_pixel_y(grid_y) - self.cell_size//2
        
        # Закрашиваем ячейку вокруг узла
        self.canvas.create_rectangle(x_pixel, y_pixel,
                                     x_pixel + self.cell_size, y_pixel + self.cell_size,
                                     fill='lightblue', outline='lightblue', tags="filled")

    def rasterize_edge(self, x1, y1, x2, y2):
        """Растеризация ребра - отмечаем пиксели ТОЧКАМИ на пересечениях сетки"""
        dy = y2 - y1
        dx = x2 - x1

        # Вертикальное ребро
        if dx == 0:
            x = x1
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if y not in self.y_buckets:
                    self.y_buckets[y] = []
                if x not in self.y_buckets[y]:
                    self.y_buckets[y].append(x)
                    self.add_boundary_point(x, y)
            return

        # Используем DDA
        slope_inv = dx / dy
        x = x1
        
        for y in range(min(y1, y2), max(y1, y2) + 1):
            xi = int(round(x))
            if y not in self.y_buckets:
                self.y_buckets[y] = []
            if xi not in self.y_buckets[y]:
                self.y_buckets[y].append(xi)
                self.add_boundary_point(xi, y)
            x += slope_inv

    def step1(self):
        """ЭТАП 1: Растеризация всех негоризонтальных рёбер"""
        self.label_info.config(text="Этап 1: Растеризация рёбер (чёрные точки на пересечениях)...")
        self.btn_step1.config(state=tk.DISABLED)
        self.btn_step2.config(state=tk.NORMAL)
        
        # Очищаем предыдущие данные
        self.y_buckets.clear()
        self.edge_pixels.clear()

        # Растеризуем все рёбра многоугольника
        n = len(self.vertices_grid)
        for i in range(n):
            x1, y1 = self.vertices_grid[i]
            x2, y2 = self.vertices_grid[(i + 1) % n]
            
            # Пропускаем горизонтальные рёбра
            if y1 == y2:
                continue
            
            # Приводим к порядку y1 < y2
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            self.rasterize_edge(x1, y1, x2, y2)

        # Определяем y_min и y_max
        if self.y_buckets:
            self.y_min = min(self.y_buckets.keys())
            self.y_max = max(self.y_buckets.keys())
        else:
            self.y_min = self.y_max = 0

        self.label_info.config(
            text=f"Этап 1 завершён. y∈[{self.y_min}, {self.y_max}]. "
                 f"Найдено {len(self.edge_pixels)} граничных пикселей."
        )

    def step2(self):
        """ЭТАП 2: Показываем отсортированные списки x-координат"""
        self.label_info.config(text="Этап 2: Сортировка x-координат...")
        self.btn_step2.config(state=tk.DISABLED)
        self.btn_step3.config(state=tk.NORMAL)

        # Сортируем каждый список по возрастанию
        for y in self.y_buckets:
            self.y_buckets[y] = sorted(set(self.y_buckets[y]))

        # Показываем отсортированные списки
        info_text = "ОТСОРТИРОВАННЫЕ СПИСКИ (y → [x1, x2, x3, x4, ...]):\n\n"
        info_text += "Для каждой горизонтальной строки y:\n"
        info_text += "список x-координат пикселей, принадлежащих рёбрам.\n"
        info_text += "=" * 50 + "\n\n"
        
        for y in sorted(self.y_buckets.keys()):
            x_list = self.y_buckets[y]
            info_text += f"y = {y:2d}: {x_list}\n"
            
            num_pairs = len(x_list) // 2
            if num_pairs > 0:
                info_text += f"       → будет залито {num_pairs} отрезков: "
                for i in range(0, len(x_list) - 1, 2):
                    info_text += f"[{x_list[i]}, {x_list[i+1]}] "
                info_text += "\n\n"
        
        info_window = tk.Toplevel(self.root)
        info_window.title("Этап 2 - Отсортированные списки X-координат")
        info_window.geometry("500x600")
        text_widget = tk.Text(info_window, wrap=tk.WORD, font=("Courier", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)

        self.label_info.config(text="Этап 2 завершён. Списки отсортированы.")

    def step3(self):
        """ЭТАП 3: Заливка отрезков между парами [x₂ᵢ₋₁, x₂ᵢ]"""
        self.label_info.config(text="Этап 3: Заливка внутренних пикселей...")
        self.btn_step3.config(state=tk.DISABLED)

        filled_pixels = 0
        
        # Проходим по всем y от y_min до y_max
        for y in range(self.y_min, self.y_max + 1):
            if y not in self.y_buckets:
                continue
            
            x_list = self.y_buckets[y]
            
            # Заливаем отрезки между парами x
            for i in range(0, len(x_list) - 1, 2):
                x_start = x_list[i]
                x_end = x_list[i + 1]
                
                # Закрашиваем все пиксели от x_start до x_end включительно
                for x in range(x_start, x_end + 1):
                    if (x, y) not in self.edge_pixels:
                        self.add_filled_cell(x, y)
                        filled_pixels += 1
        
        # Поднимаем границы и контур на передний план
        self.canvas.tag_raise("boundary")
        # Перерисовываем контур поверх заливки
        self.draw_outline()

        self.label_info.config(
            text=f"Этап 3 завершён! Закрашено {filled_pixels} внутренних пикселей."
        )

    def reset(self):
        """Полный сброс"""
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_outline()
        
        self.y_buckets.clear()
        self.edge_pixels.clear()
        self.y_min = None
        self.y_max = None
        
        self.label_info.config(text="Сброшено. Нажмите 'Шаг 1'")
        self.btn_step1.config(state=tk.NORMAL)
        self.btn_step2.config(state=tk.DISABLED)
        self.btn_step3.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterPolygonApp(root)
    app.btn_step2.config(state=tk.DISABLED)
    app.btn_step3.config(state=tk.DISABLED)
    root.mainloop()