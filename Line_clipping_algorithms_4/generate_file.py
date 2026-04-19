import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, filedialog, simpledialog

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

    default_text = ''' '''

    # открывает файл для записи с кодировкой utf-8, with автоматически закрывает файл после записи
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(default_text)
    
    os.startfile(filepath)
    
    return filepath
    
def select_existing_file(parent):
    filepath = filedialog.askopenfilename(
        title="Выберите файл с данными",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialdir=os.path.join(os.getcwd(), "Line_clipping_algorithms_4", "files"),
        parent=parent
    )
    return filepath if filepath else None