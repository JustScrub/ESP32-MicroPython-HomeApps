from machine import Pin
from neopixel import NeoPixel
import time

class NeoPixelController:
    def __init__(self, pin_number=38, num_pixels=1):
        self.pin = Pin(pin_number, Pin.OUT)
        self.np = NeoPixel(self.pin, num_pixels)

    def set_color(self, r, g, b, index=0):
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            self.np[index] = (g, r, b)
        else:
            raise ValueError("Color values must be between 0 and 255")

    def show(self):
        self.np.write()

    def grad(self, col0, col1, steps):
        r_step = (col1[0] - col0[0]) / steps
        g_step = (col1[1] - col0[1]) / steps
        b_step = (col1[2] - col0[2]) / steps
        return [(int(col0[0] + r_step * i), int(col0[1] + g_step * i), int(col0[2] + b_step * i)) for i in range(steps + 1)]

def show_grad(npc, col0, col1, steps):
    colors = npc.grad(col0, col1, steps)
    for color in colors:
        npc.set_color(*color)
        npc.show()
        time.sleep(0.01)

npc = NeoPixelController()
steps = 100  # Number of steps for the gradient
while True:
    # red to orange
    show_grad(npc, (255, 0, 0), (255, 165, 0), steps)
    # orange to yellow
    show_grad(npc, (255, 165, 0), (255, 255, 0), steps)
    # yellow to green
    show_grad(npc, (255, 255, 0), (0, 255, 0), steps)
    # green to blue
    show_grad(npc, (0, 255, 0), (0, 0, 255), steps)
    # blue to purple
    show_grad(npc, (0, 0, 255), (128, 0, 128), steps)
    # purple to red
    show_grad(npc, (128, 0, 128), (255, 0, 0), steps)