import os
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, filedialog, simpledialog

def open_file_explorer(subfolder):
    project_path = os.path.join(os.getcwd(), subfolder)
    subprocess.Popen(f'explorer "{project_path}"')

def generate_new_file(parent, subfolder):
    save_folder = os.path.join(os.getcwd(), subfolder)
    os.makedirs(save_folder, exist_ok=True)

    filename = simpledialog.askstring("Создать новый файл", "Введите имя файла:", parent=parent)

    if not filename.endswith('.txt'): filename += '.txt'
    
    filepath = os.path.join(save_folder, filename)
    
    if os.path.exists(filepath):
        overwrite = messagebox.askyesno(
            "Файл существует",
            f"Файл {filename} уже существует.\nПерезаписать его?",
            parent=parent
        )
        if not overwrite:
            return None
    
    # Текст по умолчанию для нового файла
    default_text = \
    """
    Координаты вершин многоугольника :
точка A
X:
Y:

точка B
X:
Y:

точка C
X:
Y:

точка D
X:
Y:


    Координаты концов отрезка
точка V
X:
Y:

точка U:
X:
Y:
"""

    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(default_text)
        
    return filepath
    
