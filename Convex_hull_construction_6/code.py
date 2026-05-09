import tkinter as tk
from tkinter import ttk, filedialog
import math

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Jarvis_algorithm:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм Джарвиса")
        self.root.geometry("950x700")


        style = ttk.Style()
        style.configure('Red.TLabel', foreground='red')
        style.configure('Green.TLabel', foreground='green')
        style.configure('Blue.TLabel', foreground='blue')
        style.configure('Purple.TLabel', foreground='purple')

        self.cell = 30
        self.section = None
        self.circle = None

        self.points= []
        self.y_min = None
        self.y_max = None

        self.canvas_width = 700
        self.canvas_height = 700

        self.create_interface()
        self.draw_grid()

    def create_interface(self):
        main_place = ttk.Frame(self.root)
        main_place.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_container = ttk.Frame(main_place)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        control_place = ttk.LabelFrame(main_place, padding=5, width=200)
        control_place.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        top_frame = ttk.Frame(control_place)
        top_frame.pack(fill=tk.X, pady=(0, 5))
        
        center_frame = ttk.Frame(top_frame)
        center_frame.pack(anchor=tk.CENTER)
        
        ttk.Label(center_frame, text="Кол-во точек:", font=('Arial', 9)).pack(pady=(0, 3))
        self.num_points_var = tk.StringVar(value="15")
        num_points_entry = ttk.Entry(center_frame, textvariable=self.num_points_var, width=5)
        num_points_entry.pack(pady=(0, 3))
        
        ttk.Button(center_frame, text="Создать", command=self.create_point_entries, width=10).pack(pady=(0, 5))
        
        ttk.Separator(control_place, orient='horizontal').pack(fill=tk.X, pady=3)
        
        self.points_frame = ttk.Frame(control_place)
        self.points_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        ttk.Button(control_place, text="Отобразить точки", command=self.display_points, width=15).pack(fill=tk.X, pady=(0, 3))

        
        ttk.Separator(control_place, orient='horizontal').pack(fill=tk.X, pady=3)
        
        ttk.Label(control_place, text="Построение выпуклой оболочки ", font=('Arial', 9), style='Red.TLabel').pack(pady=(0, 3))
        ttk.Button(control_place, text="Пошагово", command=self.show_next_step, width=20).pack(fill=tk.X, pady=(0, 3))
        ttk.Button(control_place, text="Автопоказ", command=self.auto_play, width=20).pack(fill=tk.X, pady=(0, 3))

        ttk.Button(control_place, text="Очистить", command=self.clear, width=15).pack(fill=tk.X)

        self.create_point_entries()
    
    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width,
                                height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=False)

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

    def create_point_entries(self):
        for widget in self.points_frame.winfo_children():
            widget.destroy()
        
        num_points = int(self.num_points_var.get())
        if num_points <= 0 or num_points > 50:
            return
            
        self.point_entries = []
        
        header_frame = ttk.Frame(self.points_frame)
        header_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(header_frame, text="№", width=2, font=('Arial', 8), style='Blue.TLabel').pack(side=tk.LEFT)
        ttk.Label(header_frame, text="X", width=4, font=('Arial', 8), style='Blue.TLabel').pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(header_frame, text="Y", width=4, font=('Arial', 8), style='Blue.TLabel').pack(side=tk.LEFT, padx=(45, 0))

        canvas = tk.Canvas(self.points_frame, height=250, width=170)
        scrollbar = ttk.Scrollbar(self.points_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind( "<Configure>", #событие, которое вызывается когда виджет изменяется
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) #область прокрутки ограничивающего проямоугольника

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") #туда кладем область прокрутки
        canvas.configure(yscrollcommand=scrollbar.set) #связывает вертикальную полосу прокрутки с областью прокрутки

        #поля ввода
        for i in range(num_points):
            point_frame = ttk.Frame(scrollable_frame)
            point_frame.pack(fill=tk.X, pady=1)
            
            ttk.Label(point_frame, text=f"{i+1}", width=2, font=('Arial', 8), style='Purple.TLabel').pack(side=tk.LEFT)
            
            x_var = tk.StringVar(value="0")
            y_var = tk.StringVar(value="0")
            
            x_entry = ttk.Entry(point_frame, textvariable=x_var, width=10, font=('Arial', 8))
            x_entry.pack(side=tk.LEFT, padx=(8, 0))
            
            y_entry = ttk.Entry(point_frame, textvariable=y_var, width=10, font=('Arial', 8))
            y_entry.pack(side=tk.LEFT, padx=(8, 0))
            
            self.point_entries.append((x_var, y_var))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        

    def get_center(self):
        w_center_x, w_center_y = 0, 0
        screen_center_x = self.canvas_width // 2
        screen_center_y = self.canvas_height // 2
        return w_center_x, w_center_y, screen_center_x, screen_center_y
    
    def coords_to_screen(self, x, y):
        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        screen_x = screen_center_x + (x - w_center_x) * self.cell
        screen_y = screen_center_y - (y - w_center_y) * self.cell
        return screen_x, screen_y
    
    def display_points(self):
        if not hasattr(self, 'point_entries'):
            return
        
        self.canvas.delete('point')
        
        for i, (x_var, y_var) in enumerate(self.point_entries):
            x = float(x_var.get())
            y = float(y_var.get())
            screen_x, screen_y = self.coords_to_screen(x, y)
                
            self.canvas.create_oval( screen_x - 3, screen_y - 3, screen_x + 3, screen_y + 3,
                                    fill='lightblue', outline='blue', tags='point')


    def cross_product(self, p1, p2, p3): #косое произведение векторов
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


    def distance_sq(self, p1, p2): #квадрат расстояния между двумя точками
        return (p2.x - p1.x)**2 + (p2.y - p1.y)**2


    def find_start_point(self): #первая точка выпуклой оболочки
        if not self.points:
            return None
        
        start = self.points[0]
        for p in self.points[1:]:
            if p.x < start.x or (p.x == start.x and p.y < start.y):
                start = p
        return start

    def show_next_step(self):
        if self.current_step == -1:
            self.convex_hull = []
            self.algorithm_steps = []
            self.convex_hull = self.jarvis_march()
            self.current_step = 0
            
    def auto_play(self):
        if self.current_step == -1:
            self.convex_hull = []
            self.algorithm_steps = []
            self.convex_hull = self.jarvis_march()
            self.current_step = 0

    def clear(self):
        self.canvas.delete('point')
        if hasattr(self, 'point_entries'):
            for x_var, y_var in self.point_entries:
                x_var.set("0")
                y_var.set("0")

if __name__ == "__main__":
    window = tk.Tk()
    app = Jarvis_algorithm(window)
    window.mainloop()