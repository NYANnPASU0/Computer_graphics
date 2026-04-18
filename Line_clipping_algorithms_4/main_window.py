import tkinter as tk
from tkinter import ttk
import os
import math
from generate_file import open_file_explorer,  generate_new_file

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы отсечения отрезка")
        self.root.geometry("950x700")

        self.cell = 30
        self.canvas_width = 700
        self.canvas_height = 900

        self.select_file = None

        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_fields()
        self.create_menu()

        self.canvas_container = ttk.Frame(self.root)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.draw_grid()


    def input_fields(self):
        button_frame = ttk.Frame(self.info_frame)
        button_frame.pack(pady=20, padx=10)


    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        #подзаголовок - файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Создать новый файл", command = lambda: generate_new_file(self.root, os.path.join("Line_clipping_algorithms_4", "files")))
        file_menu.add_command(label="Выбрать существущий файл   >", command = lambda: open_file_explorer(os.path.join("Line_clipping_algorithms_4", "files")))
        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Выход", command=self.root.quit) #выход
        


    '''def coords_to_screen(self, x, y):
        w_center_x, w_center_y, screen_center_x, screen_center_y = self.get_center()
        
        screen_x = screen_center_x + (x - w_center_x) * self.cell
        screen_y = screen_center_y - (y - w_center_y) * self.cell
        
        return screen_x, screen_y '''
    
    def draw_grid(self):
        for widget in self.canvas_container.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.canvas_container, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=False)

        ''' for x in range(-self.canvas_height, self.canvas_height):
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
                self.canvas.create_line(0, screen_y, self.canvas_width, screen_y, fill=color) '''
        
    

if __name__ == "__main__":
    window = tk.Tk()
    app = Window(window)
    window.mainloop()