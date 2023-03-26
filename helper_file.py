# window size
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 650

# colors
LIGHT_GRAY = '#cfc9c9'
GRAY = '#2a2b2a'
DIM_GRAY = '#3f403f'
BIT_DIM_GRAY = '#3f403f'
MILD_GREEN = '#4dff4d'
RED = '#ff0000'
YELLOW = '#ffff00'
ORANGE = '#ff9900'
BARS_COLOR = MILD_GREEN

# bars amount
BAR_AMOUNT_MOST = 200
BARS_AMOUNT_HIGH = 150
BARS_AMOUNT_INITIAL = 100
BARS_AMOUNT_SMALL = 50

MAX_VALUE = 200

# speed modes
SLOW = 0.1
NORMAL = 0.03
FAST = 0.01

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

# a class for storing value and color for each bar
class Data:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.temp_color = None