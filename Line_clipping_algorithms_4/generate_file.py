import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, filedialog, simpledialog

def open_file_explorer(subfolder):
    project_path = os.path.join(os.getcwd(), subfolder) # формирует полный путь: текущая директория скрипта + имя папки
    subprocess.Popen(f'explorer "{project_path}"') # запускает проводник с указанным путём

def generate_new_file(parent, subfolder):
    save_folder = os.path.join(os.getcwd(), subfolder) # формирует путь к папке, куда будет сохранён файл

    filename = simpledialog.askstring("Создать новый файл", "Введите имя файла:", parent=parent) # окно ввода строки

    if not filename.endswith('.txt'): filename += '.txt' # проверяет, заканчивается ли файл на .txt, если нет, то добавляет
    
    filepath = os.path.join(save_folder, filename) # полный путь к будущему файлу
    
    if os.path.exists(filepath): # проверяет, существует ли уже файл с таким именем
        overwrite = messagebox.askyesno( 
            "Файл существует",
            f"Файл {filename} уже существует.\nПерезаписать его?",
            parent=parent
        )
        if not overwrite:
            return None
    
    # текст по умолчанию для нового файла
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

    # открывает файл для записи с кодировкой utf-8, with автоматически закрывает файл после записи
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(default_text)
        
    return filepath
    
