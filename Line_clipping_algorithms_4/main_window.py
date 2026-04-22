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
        self.normals = []


class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы отсечения отрезка")
        self.root.geometry("950x700")

        self.cell = 35
        self.canvas_width = 700
        self.canvas_height = 700

        self.select_file = None
        self.polygon = None
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
        button_frame.pack(pady=10, padx=30)

        title_label = ttk.Label(button_frame, text="Алгоритмы", font=('Arial', 11, 'bold'))
        title_label.pack(pady=10)

        self.cyrus_beck_btn = ttk.Button(
            button_frame, text="Алгоритм Цируса-Бека", 
            command=self.cyrus_beck_algorithm, width=35)
        self.cyrus_beck_btn.pack(pady=8)

        self.cohen_sutherland_btn = ttk.Button(
            button_frame, text="Алгоритм Сазерленда-Коэна", 
            command=self.cohen_sutherland_algorithm, width=35)
        self.cohen_sutherland_btn.pack(pady=5)

        self.midpoint_btn = ttk.Button(
            button_frame, text="Алгоритм средней точки", 
            command=self.midpoint_algorithm, width=35)
        self.midpoint_btn.pack(pady=5)

        self.file_label = ttk.Label(self.info_frame, text="Файл: не выбран", font=('Arial', 10, 'italic'), foreground='gray')
        self.file_label.pack(pady=10)

    def draw_base_scene(self):
        self.draw_grid()
        self.draw_polygon()
        self.draw_lines()

    def cyrus_beck_algorithm(self):
        """Алгоритм Цируса-Бека (заглушка)"""
        if not self.rectangle or not self.lines:
            messagebox.showwarning("Предупреждение", "Сначала загрузите файл с прямоугольником и отрезками")
            return
        
        messagebox.showinfo("Алгоритм Цируса-Бека", "Реализация алгоритма Цируса-Бека будет здесь")
        self.info_label.config(text="Выбран алгоритм: Цируса-Бека")


    def cohen_sutherland_algorithm(self):
        if not self.polygon or not self.lines:
            messagebox.showwarning("Предупреждение", "Сначала загрузите файл с прямоугольником и отрезками")
            return
        
        self.draw_base_scene()

        from Sutherland_Cohen_algorithm import Sutherlan_Cohen

        p1_orig, p2_orig = self.lines[0]

        line = Sutherlan_Cohen(self.polygon.x_min, self.polygon.y_min, self.polygon.x_max, self.polygon.y_max)
        result = line.clip_line(p1_orig, p2_orig)

        x1_orig, y1_orig = self.coords_to_screen(p1_orig.x, p1_orig.y)
        x2_orig, y2_orig = self.coords_to_screen(p2_orig.x, p2_orig.y)

        self.canvas.create_text(x1_orig - 15, y1_orig - 15, text="P₁", 
                            fill='black', font=('Arial', 11, 'bold'), tags='result_labels')
        self.canvas.create_text(x2_orig + 15, y2_orig + 15, text="P₂", 
                            fill='black', font=('Arial', 11, 'bold'), tags='result_labels')
    
        if result:
            clipped_p1, clipped_p2 = result

            x1_clip, y1_clip = self.coords_to_screen(clipped_p1.x, clipped_p1.y)
            x2_clip, y2_clip = self.coords_to_screen(clipped_p2.x, clipped_p2.y)
            
            self.canvas.create_line(x1_orig, y1_orig, x2_orig, y2_orig, fill='green', width=1, tags='clipped')
            self.canvas.create_line(x1_clip, y1_clip, x2_clip, y2_clip, fill='orange', width=2.3, tags='clipped')
            
            eps = 1e-5
            # изменились ли точки после отсечения(чтобы понять подписывать или нет)
            is_fully_inside = (abs(clipped_p1.x - p1_orig.x) < eps and abs(clipped_p1.y - p1_orig.y) < eps and
                            abs(clipped_p2.x - p2_orig.x) < eps and abs(clipped_p2.y - p2_orig.y) < eps)

            if not is_fully_inside:
                self.canvas.create_oval(x1_clip-3, y1_clip-3, x1_clip+3, y1_clip+3, fill='black', tags='result_points')
                self.canvas.create_oval(x2_clip-3, y2_clip-3, x2_clip+3, y2_clip+3, fill='black', tags='result_points')
                
                self.canvas.create_text(x1_clip + 10, y1_clip - 10, text="R", 
                                        fill='black', font=('Arial', 12, 'bold'), tags='result_labels')
                self.canvas.create_text(x2_clip + 10, y2_clip - 10, text="S", 
                                        fill='black', font=('Arial', 12, 'bold'), tags='result_labels')
                
        self.canvas.create_oval(x1_orig-3, y1_orig-3, x1_orig+3, y1_orig+3, fill='black')
        self.canvas.create_oval(x2_orig-3, y2_orig-3, x2_orig+3, y2_orig+3, fill='black')

    def midpoint_algorithm(self):
        if not self.polygon or not self.lines:
            messagebox.showwarning("Предупреждение", "Сначала загрузите файл с прямоугольником и отрезками")
            return
        
        self.canvas.delete('clipped_result')
        self.canvas.delete('result_labels')
        self.canvas.delete('result_points')
        self.canvas.delete('mid_points')

        self.draw_base_scene()

        from The_midpoint_algorithm import Midpoint
        p1_orig, p2_orig = self.lines[0]

        line = Midpoint(self.polygon.x_min, self.polygon.y_min, self.polygon.x_max, self.polygon.y_max)

        result_lines = line.clip_line(p1_orig, p2_orig, pixel_size=0.1)
    
        x1_orig, y1_orig = self.coords_to_screen(p1_orig.x, p1_orig.y)
        x2_orig, y2_orig = self.coords_to_screen(p2_orig.x, p2_orig.y)

        self.canvas.create_text(x1_orig - 15, y1_orig - 15, text="P₁", 
                            fill='black', font=('Arial', 11, 'bold'), tags='result_labels')
        self.canvas.create_text(x2_orig + 15, y2_orig + 15, text="P₂", 
                            fill='black', font=('Arial', 11, 'bold'), tags='result_labels')
        
        if result_lines:
            for i, (clipped_p1, clipped_p2) in enumerate(result_lines):
                x1_c, y1_c = self.coords_to_screen(clipped_p1.x, clipped_p1.y)
                x2_c, y2_c = self.coords_to_screen(clipped_p2.x, clipped_p2.y)
                
                self.canvas.create_line(x1_c, y1_c, x2_c, y2_c, 
                                    fill='orange', width=3, tags='clipped_result')
                
                
                if i == 0:
                    self.canvas.create_text(x1_c + 10, y1_c - 10, text="R", 
                                        fill='black', font=('Arial', 12, 'bold'), tags='result_labels')
                
                if i == len(result_lines) - 1:
                    self.canvas.create_text(x2_c + 10, y2_c - 10, text="S", 
                                        fill='black', font=('Arial', 12, 'bold'), tags='result_labels')
        for p in line.created_points:
            sx, sy = self.coords_to_screen(p.x, p.y)
            self.canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill='black', tags='mid_points')


    def draw_polygon(self):
        if self.polygon and len(self.polygon.points) >= 3:
            points = self.polygon.points
            n = len(points)

            for i in range(n):
                p1 = points[i]
                p2 = points[(i+1)%n]

                x1, y1 = self.coords_to_screen(p1.x, p1.y)
                x2, y2 = self.coords_to_screen(p2.x, p2.y)

                self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2.3, tags='polygon')

    def draw_lines(self):
        if self.lines:
            for line in self.lines:
                start_point, end_point = line
                x1, y1 = self.coords_to_screen(start_point.x, start_point.y)
                x2, y2 = self.coords_to_screen(end_point.x, end_point.y)
                self.canvas.create_line(x1, y1, x2, y2, fill='green', width=2.3, tags='line')


    def load_file(self):
            from generate_file import select_existing_file 
            
            filepath = select_existing_file(self.root)
            if filepath:
                if self.read_data_from_file(filepath):
                    self.select_file = filepath
                    self.file_label.config(text=f"Файл: {os.path.basename(filepath)}", foreground='black')


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
        if self.polygon is None:
            return 0, 0, self.canvas_width / 2, self.canvas_height / 2

        center_w_x = (self.polygon.x_min + self.polygon.x_max) / 2
        center_w_y = (self.polygon.y_min + self.polygon.y_max) / 2

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
        
        # отрезок
        if len(parts) > 1:
            lines_part = parts[1].strip()
            if lines_part:
                lines_data = lines_part.split('\n')
                
                # Читаем отрезки попарно
                for i in range(0, len(lines_data), 2):
                    start_coords = lines_data[i].strip().split()
                    end_coords = lines_data[i + 1].strip().split()
                    
                    x1 = int(start_coords[0])
                    y1 = int(start_coords[1])
                    x2 = int(end_coords[0])
                    y2 = int(end_coords[1])
                        
                    start_point = Point(x1, y1)
                    end_point = Point(x2, y2)
                    self.lines.append((start_point, end_point))
        
        return True


if __name__ == "__main__":
    window = tk.Tk()
    app = Window(window)
    window.mainloop()