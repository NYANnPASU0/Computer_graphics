import tkinter as tk
from tkinter import ttk, simpledialog
import math

#1
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Section:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def get_borders(self, indent: int = 3): #для правильного отображения координатной сетки
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
        self.root.title("Растеризация отрезка")
        self.root.geometry("900x700")
        
        self.cell = 35 

        self.section = None

        self.offset_x = 500 
        self.offset_y = 350

        self.draw_grid()


    def draw_grid(self):
        main_place = ttk.Frame(self.root)
        main_place.pack(fill=tk.BOTH, expand=False)

        main_field = ttk.LabelFrame(main_place, padding=5)
        main_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        if self.section:
            min_x, min_y, max_x, max_y = self.section.get_borders(indent=3)
        else:
            min_x, min_y, max_x, max_y = -10, -10, 10, 10
        
        width_m = (max_x - min_x) * self.cell
        height_m = (max_y - min_y) * self.cell

        self.canvas = tk.Canvas(main_field, width=width_m, height=height_m, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        for i in range(0, width_m):
            if i % 35 == 0:
                self.canvas.create_line(0, i, height_m, i, fill='azure3', tags="axes")

        for i in range(0, height_m):
            if i % 35 == 0:
                self.canvas.create_line(i, 0, i, width_m, fill='azure3', tags="axes")

        y_zero = (-min_y) * self.cell
        x_zero = (-min_x) * self.cell

        if 0 <= x_zero <= height_m:
            self.canvas.create_line(x_zero, 0, x_zero, width_m, fill='black', tags="axes")
        if 0 <= y_zero <= width_m:
            self.canvas.create_line(0, y_zero, height_m, y_zero, fill='black', tags="axes")

        #подпись осей координат
        for x in range(min_x, max_x + 1):
            if x == 0:
                continue
            x_pixel = (x - min_x) * self.cell
            if 0 <= x_pixel <= width_m:
                self.canvas.create_text(x_pixel, y_zero + 15, text=str(x), fill='gray', font=('Arial', 9))

        for y in range(min_y, max_y + 1):
            if y == 0:
                continue
            y_pixel = (max_y - y) * self.cell
            if 0 <= y_pixel <= height_m:
                self.canvas.create_text(x_zero - 15, y_pixel, text=str(y), fill='gray', font=('Arial', 9))
    
        if 0 <= x_zero <= width_m and 0 <= y_zero <= height_m:
            self.canvas.create_text(x_zero + 5, y_zero + 15, text="0", fill='gray', font=('Arial', 10, 'bold'))

if __name__ == "__main__":
    window = tk.Tk()
    app = Rasterization_section(window)
    window.mainloop()       