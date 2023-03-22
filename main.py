import tkinter
import tkinter.messagebox
import customtkinter
from colors import *
import random

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sorting Visualizer")
        self.geometry(f"{1000}x{700}")


if __name__ == "__main__":
    app = App()
    app.mainloop()