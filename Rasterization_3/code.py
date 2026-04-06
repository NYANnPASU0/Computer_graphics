import tkinter as tk
from tkinter import ttk, simpledialog
import math

#1
class Section:
    def __init__(self, root):
        self.root = root
        self.root.title("Растеризация отрезка")
        self.root.geometry("900x900")
        
        self.cell = 20 
        self.width = 900
        self.height = 900

        self.offset_x = 500 
        self.offset_y = 350

        self.draw_grid(self.width, self.height, self.cell)


    def draw_grid(self, width_m, height_m, cell_m):
        main_place = ttk.Frame(self.root)
        main_place.pack(fill=tk.BOTH, expand=False)

        main_field = ttk.LabelFrame(main_place, padding=5)
        main_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        self.canvas = tk.Canvas(main_field, width=width_m, height=height_m, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        for i in range(0, width_m):
            if i % 35 == 0:
                self.canvas.create_line(0, i, height_m, i, fill='azure3', tags="axes")

        for i in range(0, height_m):
            if i % 35 == 0:
                self.canvas.create_line(i, 0, i, width_m, fill='azure3', tags="axes")

if __name__ == "__main__":
    window = tk.Tk()
    app = Section(window)
    window.mainloop()       