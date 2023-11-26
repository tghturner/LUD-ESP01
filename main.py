import machine, neopixel
import time

# Number of LEDs
n = 7

# Pin where NeoPixels are connected
pin = 1

# Create a NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), n)

# Function to set color to all LEDs
def set_color(r, g, b):
    for i in range(n):
        np[i] = (g, r, b)  # GRB format
    np.write()

# Example: Set all LEDs to red
set_color(255, 0, 0)

# Add a delay to see the color
time.sleep(5)

# Example: Turn off all LEDs
set_color(0, 0, 0)
