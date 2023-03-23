import tkinter as tk
import customtkinter as ctk
from colors import *
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sorting Visualizer")
        self.geometry(f"{1100}x{700}")
        self.resizable(False, False)

        # list for storing random values to be sorted
        self.data = []

        # ---------- INTERFACE ----------
        self.interface_frame = ctk.CTkFrame(self, corner_radius=0)
        self.interface_frame.grid(row=0, column=0, sticky="nsew")

        self.menu_frame = ctk.CTkFrame(self.interface_frame, width=140, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

        # canvas for visualisation space
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = ctk.CTkCanvas(self.interface_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=1, padx=10, pady=5)

        # buttons
        self.buttons_frame = ctk.CTkFrame(self.menu_frame)
        self.buttons_frame.grid(row=0, column=0, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.buttons_frame, text="Menu", font=ctk.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="GENERATE", command=self.generate(self.data), font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="SORT", command=self.sorting, font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # algorithm modes radiobutton
        self.algorithm_type = tk.StringVar(value="Bubble Sort")
        self.algorithm_radiobtn_frame = ctk.CTkFrame(self.menu_frame)
        self.algorithm_radiobtn_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.algorithm_radiobtn_group = ctk.CTkLabel(master=self.algorithm_radiobtn_frame, text="SORTING ALGORITHM")
        self.algorithm_radiobtn_group.grid(row=0, column=0, columnspan=2, padx=10, pady=3)
        self.bubble_radiobtn = ctk.CTkRadioButton(master=self.algorithm_radiobtn_frame, text="Bubble Sort", variable=self.algorithm_type, value="Bubble")
        self.bubble_radiobtn.grid(row=1, column=0, pady=5, padx=10, sticky='n')
        self.merge_radiobtn = ctk.CTkRadioButton(master=self.algorithm_radiobtn_frame, text="Merge Sort", variable=self.algorithm_type, value="Merge")
        self.merge_radiobtn.grid(row=2, column=0, pady=5, padx=10, sticky='n')
        self.quicksort_radiobtn = ctk.CTkRadioButton(master=self.algorithm_radiobtn_frame, text="Quick Sort", variable=self.algorithm_type, value="Quick")
        self.quicksort_radiobtn.grid(row=3, column=0, pady=5, padx=10, sticky='n')
        self.insertion_radiobtn = ctk.CTkRadioButton(master=self.algorithm_radiobtn_frame, text="Isnertion Sort", variable=self.algorithm_type, value="Insertion")
        self.insertion_radiobtn.grid(row=4, column=0, pady=5, padx=10, sticky='n')

        # speed modes radiobutton
        self.speed_mode = tk.StringVar(value="Normal")
        self.speed_radiobtn_frame = ctk.CTkFrame(self.menu_frame)
        self.speed_radiobtn_frame.grid(row=2, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")
        self.speed_radiobtn_group = ctk.CTkLabel(master=self.speed_radiobtn_frame, text="VISUALIZATION SPEED")
        self.speed_radiobtn_group.grid(row=0, column=0, columnspan=2, padx=10, pady=3)
        self.slow_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Slow", variable=self.speed_mode, value="Slow")
        self.slow_radiobtn.grid(row=1, column=0, pady=5, padx=10, sticky='n')
        self.normal_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Normal", variable=self.speed_mode, value="Normal")
        self.normal_radiobtn.grid(row=2, column=0, pady=5, padx=10, sticky='n')
        self.fast_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Fast", variable=self.speed_mode, value="Fast")
        self.fast_radiobtn.grid(row=3, column=0, pady=5, padx=10, sticky='n')
        self.instant_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Instant", variable=self.speed_mode, value="Instant")
        self.instant_radiobtn.grid(row=4, column=0, pady=5, padx=10, sticky='n')

    # generate random data
    def generate(self, data): ##TODO Naprwić generowanie przy każdym kliknięciu
        data = [random.randint(1, 200) for i in range(100)]
        colors = [LIGHT_BLUE_GRAY if i % 2 == 0 else DARK_BLUE_GRAY for i in range(len(data))]
        self.visualise(data, colors)
        print("Generated\n")

    # draw data as vertical bars
    def visualise(self, data, colors):
        self.canvas.delete("all")
        x_width = self.canvas_width / (len(data)+1)
        offset = 5
        data_norm = [x / max(data) for x in data]

        for i, height in enumerate(data_norm):
            x0 = i * x_width + offset
            y0 = self.canvas_height - height * (self.canvas_height - 10)
            x1 = (i + 1) * x_width + offset
            y1 = self.canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])

        self.update_idletasks()

    # sort the data
    def sorting(self):
        pass

    # change speed of animation
    def set_visualization_speed(self):
        speed_option = self.speed_mode.get()
        if speed_option == "Slow":
            return 0.3
        elif speed_option == "Normal":
            return 0.1
        elif speed_option == "Fast":
            return 0.05
        else:
            return 0.001


if __name__ == "__main__":
    app = App()
    app.mainloop()