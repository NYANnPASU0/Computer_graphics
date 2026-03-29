import tkinter as tk
from tkinter import ttk, simpledialog
import math

class Draw:
    def __init__(self, root):
        self.root = root
        self.root.title("Геометрические преобразования")
        self.root.geometry("1280x1024")
        
        self.scale = 30
        self.offset_x = 500 
        self.offset_y = 350
        
        self.points = []
        self.edges = []
        self.original_points = []
        
        self.create_star()
        self.save_original_points()
        self.create_interface()
    
    def multipl(self, matrix_1, matrix_2):
        row1 = len(matrix_1)
        col1 = len(matrix_1[0])
        row2 = len(matrix_2)
        col2 = len(matrix_2[0])
        
        result = [[0 for c in range(col2)] for c in range(row1)]
        
        for i in range(row1):
            for j in range(col2):
                for k in range(col1):
                    result[i][j] += matrix_1[i][k] * matrix_2[k][j]
        return result
    
    def create_star(self):
        star_points = [
            (0, 3.0), (0.9, 1.0),
            (3.0, 1.0), (1.2, -0.2),
            (2.0, -2.5), (0, -1.0),
            (-2.0, -2.5), (-1.2, -0.2),
            (-3.0, 1.0), (-0.9, 1.0)
        ]
        
        for x, y in star_points:
            point_matrix = [[x, y, 1]]
            self.points.append(point_matrix)
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), 
            (5, 6), (6, 7), (7, 8), (8, 9), (9, 0),
            (9, 5), (1, 5), (7, 5), (3, 5)
        ]
    
    def save_original_points(self):
        self.original_points = []
        for point_matrix in self.points:
            point_copy = [row[:] for row in point_matrix]
            self.original_points.append(point_copy)
    
    def reset(self):
        self.points = []
        for original_matrix in self.original_points:
            point_copy = [row[:] for row in original_matrix]
            self.points.append(point_copy)
        self.draw_figure()
    
    def transformation(self, matrix):
        for i, point_matrix in enumerate(self.points):
            new_point = self.multipl(point_matrix, matrix)
            self.points[i] = new_point
        self.draw_figure()
    
    def create_interface(self):
        main_place = ttk.Frame(self.root)
        main_place.pack(fill=tk.BOTH, expand=True)
        
        button_place = ttk.LabelFrame(main_place, padding=10)
        button_place.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        buttons = [
            ("Перенос по X", lambda: self.translate(ask=True, axis='x')),
            ("Перенос по Y", lambda: self.translate(ask=True, axis='y')),
            ("Отражение по X", lambda: self.transformation(self.reflection('x'))),
            ("Отражение по Y", lambda: self.transformation(self.reflection('y'))),
            ("Отражение по Y=X", lambda: self.transformation(self.reflection('yx'))),
            ("Поворот относительно центра", self.rotate_center),
            ("Поворот относительно точки", self.rotate_point),
            ("Масштабирование", self.scale_xy),
            ("Восстановить", self.reset),
            ("Самолет", self.open_plane_window)
        ]
        
        for text, cmd in buttons:
            btn = ttk.Button(button_place, text=text, command=cmd)
            btn.pack(fill=tk.X, pady=3)
        
        main_field = ttk.LabelFrame(main_place, padding=5)
        main_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(main_field, width=600, height=500, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.draw_figure()
        
        self.root.after(100, self.draw_axes)
    
    def draw_axes(self):
        self.canvas.update_idletasks()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        self.canvas.delete("axes")
        
        self.canvas.create_line(0, self.offset_y, w, self.offset_y, fill='gray', dash=(2, 2), tags="axes")
        self.canvas.create_line(self.offset_x, 0, self.offset_x, h, fill='gray', dash=(2, 2), tags="axes")
        self.canvas.create_text(self.offset_x - 5, self.offset_y + 10, text="0", fill='gray', tags="axes")
        
        for x in range(-100, 100):
            if x != 0:
                cx = self.offset_x + x * self.scale
                if 0 <= cx <= w:
                    self.canvas.create_line(cx, self.offset_y-2, cx, self.offset_y+2, fill='gray', tags="axes")
                    self.canvas.create_text(cx, self.offset_y + 10, text=str(x), fill='gray', tags="axes")
        
        for y in range(-100, 100):
            if y != 0:
                cy = self.offset_y - y * self.scale
                if 0 <= cy <= h:
                    self.canvas.create_line(self.offset_x-3, cy, self.offset_x+3, cy, fill='gray', tags="axes")
                    self.canvas.create_text(self.offset_x - 10, cy, text=str(y), fill='gray', tags="axes")
    
    def transform_coords(self, x, y):
        return self.offset_x + x * self.scale, self.offset_y - y * self.scale
    
    def draw_figure(self):
        self.canvas.delete("figure")
        
        for i1, i2 in self.edges:
            x1 = self.points[i1][0][0]
            y1 = self.points[i1][0][1] 
            
            x2 = self.points[i2][0][0]
            y2 = self.points[i2][0][1]
            
            cx1, cy1 = self.transform_coords(x1, y1)
            cx2, cy2 = self.transform_coords(x2, y2)
            self.canvas.create_line(cx1, cy1, cx2, cy2, fill='red', width=2, tags="figure")
        
        for point_matrix in self.points:
            x = point_matrix[0][0]
            y = point_matrix[0][1]
            cx, cy = self.transform_coords(x, y)
            self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill='black', tags="figure")
    
    def move_matrix(self, e, f):
        return [
            [1, 0, 0],
            [0, 1, 0],
            [e, f, 1]
        ]
    
    def reflection(self, axis):
        if axis == 'x':
            return [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ]
        elif axis == 'y':
            return [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        elif axis == 'yx':
            return [
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]
            ]
    
    def scaling_matrix(self, sx, sy):
        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]
    
    def rotation_matrix(self, angle, direction='counter'):
        radians = math.radians(angle)
        if direction == 'clockwise':
            radians = -radians
        
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)
        
        return [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]
    
    def rotation_about_point_matrix(self, angle, center_x, center_y, direction='counter'):
        rad = math.radians(angle)
        if direction == 'clockwise':
            rad = -rad
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        T1 = [
            [1, 0, 0],
            [0, 1, 0],
            [-center_x, -center_y, 1]
        ]
        R = [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]
        T2 = [
            [1, 0, 0],
            [0, 1, 0],
            [center_x, center_y, 1]
        ]
        
        temp = self.multipl(T1, R) 
        final = self.multipl(temp, T2) 
        return final
    
    def rotate_center(self):
        angle = simpledialog.askfloat("Поворот", "Введите угол поворота (в градусах):", minvalue=-360, maxvalue=360)
        direction = simpledialog.askstring("Направление поворота",
                                           "Выберите направление:\n'против' - против часовой\n'по' - по часовой",
                                           initialvalue='против')
        if direction.lower() == 'по':
            type = 'counter'
        else:
            type = 'clockwise'
        
        matrix = self.rotation_matrix(angle, type)
        self.transformation(matrix)
    
    def rotate_point(self):
        center_x = simpledialog.askfloat("Центр поворота", "Введите X координату точки:", minvalue=-17, maxvalue=17)
        center_y = simpledialog.askfloat("Центр поворота", "Введите Y координату точки:", minvalue=-17, maxvalue=17)
        angle = simpledialog.askfloat("Поворот", "Введите угол поворота (в градусах):", minvalue=-360, maxvalue=360)
        direction = simpledialog.askstring("Направление поворота", "Выберите направление:\n'против' - против часовой\n'по' - по часовой",
                                           initialvalue='против')
        
        if direction.lower() == 'против':
            dir_type = 'clockwise'
        else:
            dir_type = 'counter'
        matrix = self.rotation_about_point_matrix(angle, center_x, center_y, dir_type)
        self.transformation(matrix)
        

    def translate(self, ask=True, axis=None, dx=0, dy=0):
        if ask:
            if axis == 'x':
                dx = simpledialog.askfloat("Перенос", "Смещение по X:", minvalue=-17, maxvalue=17)
                dy = 0
            elif axis == 'y':
                dy = simpledialog.askfloat("Перенос", "Смещение по Y:", minvalue=-17, maxvalue=17)
                dx = 0
        self.transformation(self.move_matrix(dx, dy))
    
    def scale_xy(self):
        sx = simpledialog.askfloat("Масштабирование", "Коэффициент по X (0.1-10):", minvalue=0.1, maxvalue=10)
        if sx:
            sy = simpledialog.askfloat("Масштабирование", "Коэффициент по Y (0.1-10):", minvalue=0.1, maxvalue=10)
            if sy:
                self.transformation(self.scaling_matrix(sx, sy))

    def open_plane_window(self):
        plane_window = tk.Toplevel(self.root)
        plane_window.title("Летящий самолет")
        plane_window.geometry("1000x650")
        Plane(plane_window, self)

class Plane:
    def __init__(self, window, parent):
        self.window = window
        self.parent = parent
        self.scale = 15
        self.offset_x = 500
        self.offset_y = 300

        self.x_position = -20
        self.y_position = 0 
        self.rotation_angle = 0

        self.position = [[-20, 0, 1]]

        self.create_plane_figure()
        self.create_interface()
        self.animate()

    def create_plane_figure(self):
        self.plane_points = [
            (0, 2), (-1, 2.5), (-1, 1.5), (-1, 0.5), (-1, 3.5),
            (-2, 0), (-2, 4), (-5, 0), (-8, -4), (-11, -4),
            (-8, 0), (-15.5, 2), (-13, 2.5), (-14, 5), (-17, 4),
            (-3.5, 2), (-6.5, 2), (-7.5, 3.8), (-10, 7), (-6, 7),
            (-7, 4), (-6, 5.7), (-5.5, 6), (-3.5, 6), (-3, 5.7),
            (-2.5, 4), (-4, 4), (-4, 6)
        ]

        self.plane_edges = [
            (0, 1), (0, 2), (4, 3), (3, 5), (4, 6), (5, 6),
            (5, 7), (10, 16),(15, 16), (15, 7), (9, 10), (9, 8), (7, 8),
            (10, 11), (11, 14), (14, 13), (13, 12), (11, 12), (12, 17),
            (17, 20), (20, 21), (21, 22), (22, 19), (19, 18), (18, 17), 
            (22, 23), (23, 24), (24, 25), (25, 6), (20, 25), (26, 27)
        ]

        self.vint_points = [
            (0, 2), (0, 6), (-1, 6), (4, 2), (4, 3),
            (0, -2), (1, -2), (-4, 2), (-4, 1)
        ]

        self.vint_edges = [
            (0, 1), (1, 2), (2, 0),
            (0, 3), (3, 4), (4, 0),
            (0, 5), (5, 6), (6, 0),
            (0, 7), (7, 8), (8, 0)
        ]

        self.vint_center = (0, 2)

    def create_interface(self):
        main_field = ttk.Frame(self.window)
        main_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(main_field, width=950, height=600, bg='lightblue', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def transform_point(self, point, matrix):
        point_matrix = [[point[0], point[1], 1]]
        result = self.parent.multipl(point_matrix, matrix)
        return (result[0][0], result[0][1])
    
    def draw_shape(self, points, edges, color, width, matrix=None):
        transformed_points = []
        
        for x, y in points:
            if matrix:
                tx, ty = self.transform_point((x, y), matrix)
            else:
                tx, ty = x, y
            
            canvas_x = self.offset_x + (self.position[0][0] + tx) * self.scale
            canvas_y = self.offset_y - (self.position[0][1] + ty) * self.scale
            transformed_points.append((canvas_x, canvas_y))
        
        for i1, i2 in edges:
            self.canvas.create_line(transformed_points[i1][0], transformed_points[i1][1],
                                    transformed_points[i2][0], transformed_points[i2][1],
                                    fill=color, width=width, tags="plane")
    
    def draw_plane(self):
        self.draw_shape(self.plane_points, self.plane_edges, 'black', 2)
        
        rotating_matrix = self.parent.rotation_matrix(self.rotation_angle, 'counter')
        rotated_vint_points = []
        
        for x, y in self.vint_points:
            rel_x = x - self.vint_center[0]
            rel_y = y - self.vint_center[1]
            rotated_rel = self.transform_point((rel_x, rel_y), rotating_matrix)
            rotated_x = rotated_rel[0] + self.vint_center[0]
            rotated_y = rotated_rel[1] + self.vint_center[1]
            rotated_vint_points.append((rotated_x, rotated_y))
        
        self.draw_shape(rotated_vint_points, self.vint_edges, 'black', 2)
    
    def animate(self):
        self.canvas.delete("plane")

        translation_matrix = self.parent.move_matrix(0.5, 0)
        new_position = self.parent.multipl(self.position, translation_matrix)
        self.position = new_position
        
        if self.position[0][0] * self.scale > 1000:
            self.position = [[-40, 0, 1]]

        self.rotation_angle = (self.rotation_angle + 15) % 360    
        self.draw_plane()
            
        self.window.after(50, self.animate)

if __name__ == "__main__":
    window = tk.Tk()
    app = Draw(window)
    window.mainloop()