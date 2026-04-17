import os
import tkinter as tk
from tkinter import messagebox

def show_available_files(parent=None):
    dialog = tk.Toplevel(parent) if parent else tk.Tk()
    dialog.title("Выбор входных данных")
    dialog.geometry("550x450")
    dialog.resizable(False, False)
    
    if parent:
        dialog.grab_set()  # Делаем окно модальным
        dialog.transient(parent)

def choose_or_generate_file():
    num = 1
    while True:
        if not os.path.exists(f"Входные_координаты_{num}.txt"):
            break
        num += 1

    selector = tk.Toplevel()
    selector.title("Выбор входных данных")
    selector.geometry("500x400")

     # Список файлов
    listbox = tk.Listbox(selector, height=15, font=("Courier", 10))
    listbox.pack(fill='both', expand=True, padx=20, pady=10)


if __name__ == "__main__":
    choose_or_generate_file()