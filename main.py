from helper_file import *
import tkinter as tk
import customtkinter as ctk
import random
import time

# setting standard interface appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Main class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sorting Visualizer")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        # list for storing random values of Data class to be sorted
        self.data = []

        # ---------- INTERFACE ----------
        self.interface_frame = ctk.CTkFrame(self, corner_radius=0)
        self.interface_frame.grid(row=0, column=0, sticky="nsew")

        self.menu_frame = ctk.CTkFrame(self.interface_frame, width=WINDOW_WIDTH*0.3, height=WINDOW_HEIGHT, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

        # canvas for visualisation space
        self.canvas_width = WINDOW_WIDTH * 0.75
        self.canvas_height = WINDOW_HEIGHT * 0.95
        self.canvas = ctk.CTkCanvas(self.interface_frame, width=self.canvas_width, height=self.canvas_height, bg=LIGHT_GRAY)
        self.canvas.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # buttons
        self.buttons_frame = ctk.CTkFrame(self.menu_frame)
        self.buttons_frame.grid(row=0, column=0, padx=15, pady=(20, 0), sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.buttons_frame, text="Menu", font=ctk.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(40, 0), pady=20, sticky="nsew")
        self.generate_button = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="GENERATE", anchor="center",command=self.generate, font=ctk.CTkFont(size=20, weight="bold"))
        self.generate_button.grid(row=1, column=0, padx=(40, 0), pady=10, sticky="nsew")
        self.sort_button = ctk.CTkButton(self.buttons_frame, border_spacing=5, corner_radius=20, text="SORT", command=self.sorting, font=ctk.CTkFont(size=20, weight="bold"))
        self.sort_button.grid(row=2, column=0, padx=(40, 0), pady=10, sticky="nsew")

        # algorithm modes optionmenu
        self.algorithm_type = tk.StringVar()
        self.algorithm_frame = ctk.CTkFrame(self.menu_frame)
        self.algorithm_frame.grid(row=1, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.algorithm_mode_label = ctk.CTkLabel(self.algorithm_frame, text="SORTING ALGORITHM", anchor="center", font=ctk.CTkFont(weight="bold"))
        self.algorithm_mode_label.grid(row=0, column=0, padx=(30, 0), pady=(10, 0), sticky="nsew")
        self.algorithm_mode_optionemenu = ctk.CTkOptionMenu(self.algorithm_frame, variable=self.algorithm_type)
        self.algorithm_mode_optionemenu.grid(row=1, column=0, padx=(30, 0), pady=(10, 10), sticky="nsew")

        # amout of bars segmented button
        self.bars_amount = tk.IntVar()
        self.slider_bars_frame = ctk.CTkFrame(self.menu_frame)
        self.slider_bars_frame.grid(row=2, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.sliders_bars_label = ctk.CTkLabel(master=self.slider_bars_frame, text='NUMBER OF BARS', anchor="center", font=ctk.CTkFont(weight="bold"))
        self.sliders_bars_label.grid(row=0, column=0, padx=(45, 0), pady=(10, 0), sticky="nsew")
        self.seg_button_bars = ctk.CTkSegmentedButton(self.slider_bars_frame, variable=self.bars_amount, command=self.bars_update)
        self.seg_button_bars.grid(row=1, column=0, padx=(40, 0), pady=10, sticky="nsew")

        # speed modes radiobutton
        self.speed_mode = tk.DoubleVar()
        self.speed_radiobtn_frame = ctk.CTkFrame(self.menu_frame)
        self.speed_radiobtn_frame.grid(row=3, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.speed_radiobtn_label = ctk.CTkLabel(master=self.speed_radiobtn_frame, text="VISUALIZATION SPEED", anchor="center", font=ctk.CTkFont(weight="bold"))
        self.speed_radiobtn_label.grid(row=0, column=0, padx=30, pady=(10, 0), sticky="nsew")
        self.slow_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Slow", variable=self.speed_mode, value=SLOW)
        self.slow_radiobtn.grid(row=1, column=0, pady=5, padx=30, sticky="nsew")
        self.normal_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Normal", variable=self.speed_mode, value=NORMAL)
        self.normal_radiobtn.grid(row=2, column=0, pady=5, padx=30, sticky="nsew")
        self.fast_radiobtn = ctk.CTkRadioButton(master=self.speed_radiobtn_frame, text="Fast", variable=self.speed_mode, value=FAST)
        self.fast_radiobtn.grid(row=3, column=0, pady=5, padx=30, sticky="nsew")

        # interface appearance modes option menu
        self.appearance_frame = ctk.CTkFrame(self.menu_frame)
        self.appearance_frame.grid(row=5, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.appearance_mode_label = ctk.CTkLabel(self.appearance_frame, text="APPEARENCE MODE", anchor="center", font=ctk.CTkFont(weight="bold"))
        self.appearance_mode_label.grid(row=0, column=0, padx=(40, 0), pady=(10, 0), sticky="nsew")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.appearance_frame, values=["Dark", "Light"], command=self.change_appearance_mode, anchor="center")
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=(40, 0), pady=(10, 10), sticky="nsew")

        # set default values
        self.algorithm_mode_optionemenu.configure(values=["Bubble", "Merge", "Quick", "Insertion", "Shell", "Tim", "Selection", "Pigeonhole", "Coctail", "Comb"])
        self.algorithm_mode_optionemenu.set('Merge') # select default algorithm - Merge
        self.normal_radiobtn.select() # select default speed - Normal
        self.seg_button_bars.configure(values=[BARS_AMOUNT_SMALL, BARS_AMOUNT_INITIAL, BARS_AMOUNT_HIGH, BAR_AMOUNT_MOST])
        self.seg_button_bars.set(BARS_AMOUNT_INITIAL)
        self.sort_button.configure(state="disabled")

        self.generate()

    def bars_update(self, _):
        self.generate()

    # change appearance of the interface
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    # generate random data
    def generate(self):
        self.data = [Data(random.randint(1, MAX_VALUE), BARS_COLOR) for _ in range(self.bars_amount.get())]
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
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=new_color)    # first initial color upon generation
            elif self.data[i].temp_color:   # checking whether there is assigned temporary color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.data[i].temp_color)
                self.data[i].temp_color = None
            else:   # drawing assigned color in data class
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.data[i].color)

        self.update_idletasks()

    # running selected sort function
    def sorting(self):
        # blocking unwanted buttons
        self.generate_button.configure(state="disabled")
        self.sort_button.configure(state="disabled")
        self.seg_button_bars.configure(state='disabled')
        self.algorithm_mode_optionemenu.configure(state='disabled')

        algorithm_type = self.algorithm_type.get()
        time_sleep = self.speed_mode.get()


        if algorithm_type == 'Bubble':
            self.bubble(time_sleep)
        elif algorithm_type == 'Merge':
            self.merge(0, len(self.data)-1, time_sleep)
        elif algorithm_type == 'Quick':
            self.quick(0, len(self.data)-1, time_sleep)
        elif algorithm_type == 'Insertion':
            self.insertion(0, len(self.data)-1, time_sleep)
        elif algorithm_type == 'Shell':
            self.shell(time_sleep)
        elif algorithm_type == 'Tim':
            self.tim(time_sleep)
        elif algorithm_type == 'Selection':
            self.selection(time_sleep)
        elif algorithm_type == 'Pigeonhole':
            self.pigeonhole(time_sleep)
        elif algorithm_type == 'Coctail':
            self.coctail(time_sleep)
        elif algorithm_type == 'Comb':
            self.comb(time_sleep)

        # enabling buttons
        self.generate_button.configure(state="normal")
        self.sort_button.configure(state="disabled")
        self.seg_button_bars.configure(state="normal")
        self.algorithm_mode_optionemenu.configure(state='normal')

    # ---------- SORTING ALGORITHMS ----------
    # bubble sort
    def bubble(self, time_sleep):
        size = len(self.data)
        for i in range(size-1):
            for j in range(size-i-1):
                if self.data[j].value > self.data[j+1].value:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]

                    # visualisation
                    self.data[j].temp_color = RED
                    self.data[j+1].temp_color = YELLOW
                    self.visualise()
                    time.sleep(time_sleep)

        self.visualise()

    # function for merging
    def mrg(self, left, mid, right, time_sleep):
        i, j, temp = left, mid+1, []
        while (i <= mid and j <= right):
            if self.data[i].value <= self.data[j].value:
                temp.append(self.data[i])
                i += 1
            else:
                temp.append(self.data[j])
                j += 1
        while (i <= mid):
            temp.append(self.data[i])
            i += 1
        while (j <= right):
            temp.append(self.data[j])
            j += 1
        i, k = 0, right-left+1
        while (i < k):
            self.data[left+i] = temp[i]
            i += 1

        # visualisation
        for i, x in enumerate(self.data):
            if i >= left and i < mid:
                x.temp_color = YELLOW
            elif i == mid:
                x.temp_color = RED
            elif i > mid and i <= right:
                x.temp_color = ORANGE
        self.visualise()
        time.sleep(time_sleep+0.1)

    # merge sort
    def merge(self, left, right, time_sleep):
        if left < right:
            mid = (left + right) // 2
            self.merge(left, mid, time_sleep)
            self.merge(mid+1, right, time_sleep)
            self.mrg(left, mid, right, time_sleep)
        self.visualise()

    # quick sort
    def quick(self, left, right, time_sleep):
        i, j = left, right
        p = (left + right) // 2
        pivot = self.data[p].value
        while (i <= j):
            while (self.data[i].value < pivot):
                i += 1
            while (self.data[j].value > pivot):
                j -= 1
            if i <= j:
                self.data[i], self.data[j] = self.data[j], self.data[i]
                i += 1
                j -= 1

                # visualisation
                self.data[i].temp_color = YELLOW
                self.data[j].temp_color = ORANGE
                self.data[p].temp_color = RED
                self.visualise()
                time.sleep(time_sleep)

        if j > left:
            self.quick(left, j, time_sleep)
        if i < right:
            self.quick(i, right, time_sleep)
        self.visualise()

    # insertion sort
    def insertion(self, left, right, time_sleep):
        for i in range(left + 1, right + 1):
            j = i
            while j > left and self.data[j].value < self.data[j-1].value:
                # visualisation
                self.data[j].temp_color = RED
                self.data[j-1].temp_color = YELLOW
                self.visualise()
                time.sleep(time_sleep)

                self.data[j], self.data[j-1] = self.data[j-1], self.data[j]
                j -= 1
            self.visualise()

    # shell sort
    def shell(self, time_sleep):
        n = len(self.data)
        gap = n // 2
        while (gap > 0):
            j = gap
            while (j < n):
                i = j - gap
                while (i >= 0):
                    if self.data[i+gap].value > self.data[i].value:
                        break

                    # visualisation
                    self.data[i+gap], self.data[i] = self.data[i], self.data[i+gap]
                    self.data[i+gap].temp_color = RED
                    self.data[i].temp_color = YELLOW
                    self.visualise()
                    time.sleep(time_sleep)

                    i = i - gap
                j += 1
            gap = gap // 2
        self.visualise()

    # functions for tim sort algorithm
    def minRun(self, n):
        r = 0
        while (n >= 32):
            r |= n & 1
            n >>= 1
        return n + r

    # tim sort
    def tim(self, time_sleep):
        n = len(self.data)
        run = self.minRun(n)
        for left in range(0, n, run):
            right = min(left+run-1, n-1)
            self.insertion(left, right, time_sleep)
        size = run
        while (size < n):
            for left in range(0, n, 2*size):
                mid = min(n-1, left+size-1)
                right = min((left+2*size-1), n-1)
                if mid < right:
                    self.mrg(left, mid, right, time_sleep)
            size = 2*size
        self.visualise()

    # selection sort
    def selection(self, time_sleep):
        for i in range(len(self.data)):
            minimum_idx = i
            for j in range(i+1, len(self.data)):
                if self.data[minimum_idx].value > self.data[j].value:
                    minimum_idx = j

                # visualisation
                self.data[minimum_idx].temp_color = YELLOW
                self.data[j].temp_color = RED
                self.visualise()
                time.sleep(time_sleep)

            self.data[i], self.data[minimum_idx] = self.data[minimum_idx], self.data[i]
        self.visualise()

    # pigeonhole sort
    def pigeonhole(self, time_sleep):
        min_val = min(self.data, key=lambda x: x.value).value
        max_val = max(self.data, key=lambda x: x.value).value
        size = max_val - min_val + 1
        holes = [0]*size
        for x in self.data:
            holes[x.value-min_val] += 1
        i = 0
        for count in range(size):
            while (holes[count] > 0):
                holes[count] -= 1
                self.data[i].value = count + min_val

                # visualisation
                self.data[i].color = rgb_to_hex(change_rgb_brightness(hex_to_rgb(BARS_COLOR), self.data[i].value / MAX_VALUE))  # correcting the color according to value
                self.data[i].temp_color = RED
                self.visualise()
                time.sleep(time_sleep)

                i += 1
        self.visualise()

    # coctail sort
    def coctail(self, time_sleep):
        n = len(self.data)
        swapped = True
        left, right = 0, n-1
        while (swapped == True):
            swapped = False
            for i in range(left, right):
                if self.data[i].value > self.data[i+1].value:
                    self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                    swapped = True

                    # visualisation
                    self.data[i].temp_color = RED
                    self.data[i+1].temp_color = YELLOW
                    self.visualise()
                    time.sleep(time_sleep)

            if swapped == False:
                break
            swapped = False
            right -= 1
            for i in range(right-1, left-1, -1):
                if self.data[i].value > self.data[i+1].value:
                    self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                    swapped = True

                    # visualisation
                    self.data[i].temp_color = YELLOW
                    self.data[i+1].temp_color = RED
                    self.visualise()
                    time.sleep(time_sleep)

            left += 1
        self.visualise()

    # function for finding next gap in comb sort
    def nextGap(self, gap):
        gap = (gap * 10) // 13
        return 1 if gap < 1 else gap

    # comb sort
    def comb(self, time_sleep):
        n = len(self.data)
        gap = n
        swapped = True
        while ((gap != 1) or (swapped == True)):
            gap = self.nextGap(gap)
            swapped = False
            for i in range(n-gap):
                if self.data[i].value > self.data[i+gap].value:
                    self.data[i], self.data[i+gap] = self.data[i+gap], self.data[i]
                    swapped = True

                # visualisation
                self.data[i].temp_color = RED
                self.data[i+gap].temp_color = YELLOW
                self.visualise()
                time.sleep(time_sleep)

        self.visualise()

    # bucket sort # TODO DOKONCZYC
    def bucket(self, time_sleep):
        slot_num = 10
        arr = [[] for _ in range(slot_num)]
        for x in self.data:
            idx_b = int(slot_num * x.value)
            arr[idx_b].append(x)

# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()