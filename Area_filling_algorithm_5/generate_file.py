import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, filedialog, simpledialog

def select_existing_file(parent):
    filepath = filedialog.askopenfilename(
        title="Выберите файл с данными",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialdir=os.path.join(os.getcwd(), "Area_filling_algorithm_5", "files"),
        parent=parent
    )
    return filepath if filepath else None