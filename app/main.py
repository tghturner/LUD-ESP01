import machine, neopixel
import time

# Number of LEDs
n = 7

# Pin where NeoPixels are connected
pin = 5

# Create a NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), n)

# Function to set color to all LEDs
def set_color(r, g, b):
    for i in range(n):
        np[i] = (g, r, b)  # GRB format
    np.write()

while True:
    # Example: Set all LEDs to red
    set_color(255, 0, 0)
    # Add a delay to see the color
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < 2000:  # Loop for 1 second
        machine.idle()
    # Example: Turn off all LEDs
    set_color(0, 0, 0)
    # Add a delay to see the color
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < 1000:  # Loop for 1 second
        machine.idle()
