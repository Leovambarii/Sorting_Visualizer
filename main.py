import tkinter as tk
import customtkinter as ctk
import random
import time

# colors
DARK_BLUE_GRAY = '#52527a'
LIGHT_BLUE_GRAY = '#8585ad'
MILD_GREEN = '#4dff4d'
RED = '#ff0000'
BARS_COLOR = MILD_GREEN
# speed modes
SLOW = 0.05
NORMAL = 0.01
FAST = 0.001

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def change_rgb_brightness(color, height):
    r, g, b = color
    r = int(r * height)
    g = int(g * height)
    b = int(b * height)
    return (r, g, b)

def rgb_to_hex(rgb):
    r, g, b = rgb
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# class Data:
#     def __init__(self, value, color):
#         self.value = value
#         self.color = color

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sorting Visualizer")
        self.geometry(f"{1100}x{700}")
        self.resizable(False, False)

        # list for storing random values of Data class to be sorted
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
        self.sidebar_button_1 = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="GENERATE", command=self.generate, font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="SORT", command=self.sorting, font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # algorithm modes radiobutton
        self.algorithm_type = tk.StringVar(value="Bubble")
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
        self.speed_mode = tk.DoubleVar(value=NORMAL)
        self.speed_radiobtn_frame = ctk.CTkFrame(self.menu_frame)
        self.speed_radiobtn_frame.grid(row=2, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")
        self.speed_radiobtn_group = ctk.CTkLabel(master=self.speed_radiobtn_frame, text="VISUALIZATION SPEED")
        self.speed_radiobtn_group.grid(row=0, column=0, columnspan=2, padx=10, pady=3)
        self.slow_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Slow", variable=self.speed_mode, value=SLOW)
        self.slow_radiobtn.grid(row=1, column=0, pady=5, padx=10, sticky='n')
        self.normal_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Normal", variable=self.speed_mode, value=NORMAL)
        self.normal_radiobtn.grid(row=2, column=0, pady=5, padx=10, sticky='n')
        self.fast_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Fast", variable=self.speed_mode, value=FAST)
        self.fast_radiobtn.grid(row=3, column=0, pady=5, padx=10, sticky='n')

    # generate random data
    def generate(self):
        # self.data = [[random.randint(1, 200), BARS_COLOR] for _ in range(100)]
        self.data = [random.randint(1, 200) for _ in range(100)]
        self.colors = [BARS_COLOR for _ in range(len(self.data))]
        self.visualise(sort_flag=False)

    # draw data as vertical bars
    def visualise(self, sort_flag):
        self.canvas.delete("all")
        x_width = self.canvas_width / (len(self.data)+1)
        offset = 5
        # if sort_flag:
        #     data_norm = self.data   # TODO - niech może przechowuje tuple typu [data value, color]
        # else:
        #     data_norm = [x / max(self.data) for x in self.data]

        data_norm = [x / max(self.data) for x in self.data]

        for i, height in enumerate(data_norm):
            x0 = i * x_width + offset
            y0 = self.canvas_height - height * (self.canvas_height - 10)
            x1 = (i + 1) * x_width + offset
            y1 = self.canvas_height

            # convert hex color to rgb to change brightness depending on height
            color_rgb = hex_to_rgb(self.colors[i])
            new_rgb_color = change_rgb_brightness(color_rgb, height)
            new_color = rgb_to_hex(new_rgb_color)

            # drawing vertical bar
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=new_color)

        self.update_idletasks()

    # sort the data
    def sorting(self):
        algorithm_type = self.algorithm_type.get()

        if algorithm_type == 'Bubble':
            self.bubble()
        elif algorithm_type == 'Merge':
            self.merge(0, len(self.data)-1)

    # bubble sort
    def bubble(self):
        time_sleep = self.speed_mode.get()
        size = len(self.data)
        for i in range(size-1):
            for j in range(size-i-1):
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                    self.visualise(sort_flag=True)
                    time.sleep(time_sleep)
        self.visualise(sort_flag=True)

    # merge sort
    def mrg(self, start, mid, end):
        p, q = start, mid+1
        temp = []
        for i in range(start, end+1):
            if p > mid:
                temp.append(self.data[q])
                q += 1
            elif q > end:
                temp.append(self.data[p])
            elif self.data[p] < self.data[q]:
                temp.append(self.data[p])
                p += 1
            else:
                temp.append(self.data[q])
                q += 1

        for i in range(len(temp)):
            self.data[start] = temp[i]
            start += 1

    def merge(self, start, end):
        if start < end:
            time_sleep = self.speed_mode.get()
            mid = (start + end) // 2
            self.merge(start, mid)
            self.merge(mid+1, end)

            self.mrg(start, mid, end)
            self.visualise(sort_flag=True)
            time.sleep(time_sleep)

        self.visualise(sort_flag=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()