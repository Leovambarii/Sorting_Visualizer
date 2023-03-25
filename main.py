import tkinter as tk
import customtkinter as ctk
import random
import time

# colors
DARK_BLUE_GRAY = '#52527a'
LIGHT_BLUE_GRAY = '#8585ad'
MILD_GREEN = '#4dff4d'
RED = '#ff0000'
YELLOW = '#ffff00'
ORANGE = '#ff9900'
BARS_COLOR = MILD_GREEN

# bars
MAX_VALUE = 200
BARS_AMOUNT = 100

# speed modes
# SLOW = 0.05
SLOW = 0.1
NORMAL = 0.01
FAST = 0

# convert hex color to rgv
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

# change rgb brightness
def change_rgb_brightness(color, height):
    r, g, b = color
    r = int(r * height)
    g = int(g * height)
    b = int(b * height)
    return (r, g, b)

# convert rgb color to hex
def rgb_to_hex(rgb):
    r, g, b = rgb
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# setting standard interface appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# a class for storing value and color for each bar
class Data:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.temp_color = None

# Main class
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
        self.generate_button = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="GENERATE", command=self.generate, font=ctk.CTkFont(size=20, weight="bold"))
        self.generate_button.grid(row=1, column=0, padx=20, pady=10)
        self.sort_button = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="SORT", command=self.sorting, font=ctk.CTkFont(size=20, weight="bold"))
        self.sort_button.grid(row=2, column=0, padx=20, pady=10)

        # algorithm modes radiobutton
        self.algorithm_type = tk.StringVar()
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
        self.speed_mode = tk.DoubleVar()
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

        # interface appearance modes oprion menu
        self.appearance_mode_label = ctk.CTkLabel(self.menu_frame, text="APPEARENCE MODE", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.menu_frame, values=["Dark", "Light"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # set default values
        self.bubble_radiobtn.select() # select defalut algorithm - Bubble
        self.normal_radiobtn.select() # select default speed - Normal
        self.sort_button.configure(state="disabled")

    # change appearance of the interface
    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # generate random data
    def generate(self):
        self.data = [Data(random.randint(1, MAX_VALUE), BARS_COLOR) for _ in range(100)]
        self.visualise(generate_flag=True)
        self.sort_button.configure(state="normal")

    # draw data as vertical bars
    def visualise(self, generate_flag=False):
        self.canvas.delete("all")
        x_width = self.canvas_width / (len(self.data)+1)
        offset = 5
        data_norm = [x.value / MAX_VALUE for x in self.data]

        for i, height in enumerate(data_norm):
            x0 = i * x_width + offset
            y0 = self.canvas_height - height * (self.canvas_height - 10)
            x1 = (i + 1) * x_width + offset
            y1 = self.canvas_height

            # convert hex color to rgb to change brightness depending on height
            if generate_flag:
                color_rgb = hex_to_rgb(self.data[i].color)
                new_rgb_color = change_rgb_brightness(color_rgb, height)
                new_color = rgb_to_hex(new_rgb_color)
                self.data[i].color = new_color

            # drawing vertical bar
            # first initial color upon generation
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=new_color)
            # checking whether there is assigned temporary color
            elif self.data[i].temp_color:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.data[i].temp_color)
                self.data[i].temp_color = None
            # drawing assigned color in data class
            else:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.data[i].color)

        self.update_idletasks()

    # running selected sort function
    def sorting(self):
        # blocking unwanted buttons
        self.generate_button.configure(state="disabled")
        self.sort_button.configure(state="disabled")

        algorithm_type = self.algorithm_type.get()
        if algorithm_type == 'Bubble':
            self.bubble()
        elif algorithm_type == 'Merge':
            self.merge(0, len(self.data)-1)
        elif algorithm_type == 'Quick':
            self.quick(0, len(self.data)-1)

        self.generate_button.configure(state="normal")
        self.sort_button.configure(state="disabled")

    # ---------- SORTING ALGORITHMS ----------
    # bubble sort
    def bubble(self, i=0):
        time_sleep = self.speed_mode.get()
        size = len(self.data)
        for i in range(size-1):
            for j in range(size-i-1):
                if self.data[j].value > self.data[j+1].value:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                    # assigning temporal colors
                    self.data[j].temp_color = RED
                    self.data[j+1].temp_color = YELLOW

                    self.visualise()
                    time.sleep(time_sleep)
        self.visualise()


    # merge sort
    def mrg(self, left, mid, right):
        i, j, temp = left, mid+1, []
        while i <= mid and j <= right:
            if self.data[i].value <= self.data[j].value:
                temp.append(self.data[i])
                i += 1
            else:
                temp.append(self.data[j])
                j += 1
        while i <= mid:
            temp.append(self.data[i])
            i += 1
        while j <= right:
            temp.append(self.data[j])
            j += 1
        i, k = 0, right-left+1
        while i < k:
            self.data[left+i] = temp[i]
            i += 1

    def merge(self, left, right):
        time_sleep = self.speed_mode.get()
        if left < right:
            mid = (left + right) // 2
            self.merge(left, mid)
            self.merge(mid+1, right)

            self.mrg(left, mid, right)
            for i, x in enumerate(self.data):
                if i >= left and i < mid:
                    x.temp_color = YELLOW
                elif i == mid:
                    x.temp_color = RED
                elif i > mid and i <= right:
                    x.temp_color = ORANGE

            self.visualise()
            time.sleep(time_sleep)
        self.visualise()

    # quick sort
    def quick(self, left, right):
        time_sleep = self.speed_mode.get()
        i, j = left, right
        pivot = self.data[(left + right) // 2].value
        while i <= j:
            while self.data[i].value < pivot:
                i += 1
            while self.data[j].value > pivot:
                j -= 1
            if i <= j:
                self.data[i], self.data[j] = self.data[j], self.data[i]
                i += 1
                j -= 1
                self.visualise()
                time.sleep(time_sleep)
        if j > left:
            self.quick(left, j)
        if i < right:
            self.quick(i, right)
        self.visualise()

# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()