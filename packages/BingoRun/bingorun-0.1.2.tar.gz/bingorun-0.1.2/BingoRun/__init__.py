from .module import my_function, MyClass
from tkinter import Tk, filedialog

# 1. delete ./dist
# 2. python -m build
# 3. upload package: python -m twine upload dist/*

VERSION = "1.0.0"

def greet():
    print(f"Welcome to my_package, version {VERSION}!")

def get_folder_path(self, folder_path: str = "") -> str:
    if not isinstance(folder_path, str):
        raise TypeError("folder_path must be a string")
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        selected_folder = filedialog.askdirectory(initialdir=folder_path or ".")
        root.destroy()
        return selected_folder or folder_path
    except Exception as e:
        raise RuntimeError(f"Error initializing folder dialog: {e}") from e