from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X128
from picovector import ANTIALIAS_BEST, PicoVector, Transform, Polygon

i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X128)
display = i75.display

WIDTH = i75.width
HEIGHT = i75.height

# Couple of colors for use later
ORANGE = display.create_pen(255, 128, 0)
BLACK = display.create_pen(0, 0, 0)

# ------------------------- Loop ---------------------------------
while True:

    # Clear the display
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(ORANGE)
    display.pixel((WIDTH) // 2,(HEIGHT) // 2)

    # Update the display
    i75.update()

