from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import filedialog

load_dotenv()

FILE_DIR = os.getenv('FILE_DIR')

def file_dir():
    home = os.path.expanduser('~')
    file_dir = FILE_DIR
    return os.path.join(home, file_dir)


def open_filedialog(path: str=None) -> str:
    dir_path = file_dir() if path is None else path

    root = tk.Tk()
    root.lift()
    root.withdraw()

    filename = filedialog.askopenfilename(
        initialdir=dir_path,
        title='Choose Excel-file',
        filetypes=[('Excel files', '.xlsx')]
        )

    root.quit()

    # End application if file is not chosen, i.e. str is empty (false)
    if not filename:
        exit()

    return filename

