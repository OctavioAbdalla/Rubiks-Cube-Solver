class Hsv_values: 
    @staticmethod
    def hsv_to_color(hsv):
        h, s, v = hsv[:3]
        if h <= 9 and s >= 100 and v >= 30:
            return "red"
        elif h <= 20 and s >= 100 and v >= 50:
            return "orange"
        elif h <= 40 and s >= 100 and v >= 80:
            return "yellow"
        elif h <= 90 and s >= 85 and v <= 200:
            return "green"
        elif h <= 125 and s >= 160 and v >= 40:
            return "blue"
        elif h <= 150 and s <= 90 and v >= 100:
            return "white"
        else:
            return False

    @staticmethod
    def color_to_rgb(color):
        if color == 'red':
            return (0, 0, 255)
        elif color == 'orange':
            return (0, 140, 255)
        elif color == 'yellow':
            return (0, 255, 255)
        elif color == 'green':
            return (0, 255, 0)
        elif color == 'blue':
            return (255, 0, 0)
        elif color == 'white':
            return (255, 255, 255)

