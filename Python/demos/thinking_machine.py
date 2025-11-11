import time
import random

from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X128

i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X128)
display = i75.display

WIDTH, HEIGHT = display.get_bounds()
VIRTUAL_WIDTH = WIDTH // 4
VIRTUAL_HEIGHT = HEIGHT // 4

# Couple of colors for use later
ORANGE = display.create_pen(255, 128, 0)
BLACK = display.create_pen(0, 0, 0)

# We want to scale the pixel up to a 2x2 square.
# The upper left is the coordinate of a pixel.
# Mapping from Scale 1 to 2:
# 0,0 => 0,0
# 1,1 => 2,2
# 2,2 => 4,4

# Create the 2D array of size 32x32 because each virtual pixel is
# 2x2 pixels in dimensions. This will span the 128x128 pixel area.
N_ROWS = VIRTUAL_WIDTH
N_COLS = VIRTUAL_HEIGHT
initial_value = 0

buf = [[initial_value for col in range(N_COLS)] for row in range(N_ROWS)]

x = 0
y = 0

# What we want is to randomly choose a pixel that is on and turn it off.
# This means we need to "scan" for an On pixel.
# 
# Another way is to random attempt to turn Off more pixels than On.
#
# ++++ TOOK THIS APPROACH ++++
# Another approach is to randomly choose if we are turing On more than
# we are turning Off.
# ------------------------- Loop ---------------------------------
while True:

    # We don't clear the display because we have a chance of clearing
    # individual pixels.
    # display.set_pen(BLACK)
    # display.clear()

    # An occasional burst of 4 pixels on
    block  = random.random()

    if (random.random() > 0.25):
        if (block > 0.9):
            for i in range(4): # Block of N
                col = random.randint(0, VIRTUAL_WIDTH-1)
                row = random.randint(0, VIRTUAL_HEIGHT-1)
                buf[col][row] = 1
        else:
            col = random.randint(0, VIRTUAL_WIDTH-1)
            row = random.randint(0, VIRTUAL_HEIGHT-1)
            # Turn on pixel at x,y
            buf[col][row] = 1

    for i in range(10):
        col = random.randint(0, VIRTUAL_WIDTH-1)
        row = random.randint(0, VIRTUAL_HEIGHT-1)
        if (random.random() > 0.25):
            # Turn off pixel at x,y
            buf[col][row] = 0

    # -------- Draw pixels --------
    x = 0
    y = 0
    for row in buf:
        y = 0
        for col in row:
            if col == 1:
                display.set_pen(ORANGE)
            else:
                display.set_pen(BLACK)

            xx = x * 4
            yy = y * 4

            # Fastest
            display.rectangle(xx, yy, 4, 4)

            # Slow: 4 lines
            # display.pixel_span(xx, yy, 4)
            # display.pixel_span(xx, yy+1, 4)
            # display.pixel_span(xx, yy+2, 4)
            # display.pixel_span(xx, yy+3, 4)

            # Slowest: individual pixels
            # display.pixel(xx, yy)
            # display.pixel(xx+1, yy)
            # display.pixel(xx+2, yy)
            # display.pixel(xx+3, yy)
            
            # display.pixel(xx, yy+1)
            # display.pixel(xx+1, yy+1)
            # display.pixel(xx+2, yy+1)
            # display.pixel(xx+3, yy+1)

            # display.pixel(xx, yy+2)
            # display.pixel(xx+1, yy+2)
            # display.pixel(xx+2, yy+2)
            # display.pixel(xx+3, yy+2)

            # display.pixel(xx, yy+3)
            # display.pixel(xx+1, yy+3)
            # display.pixel(xx+2, yy+3)
            # display.pixel(xx+3, yy+3)

            y += 1
        x += 1
    
    
    # ----------- Update the display --------------------------
    i75.update()
    # time.sleep(0.1)

