from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X128

i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X128)
display = i75.display

WIDTH, HEIGHT = display.get_bounds()

# Couple of colors for use later
ORANGE = display.create_pen(255, 128, 0)
BLACK = display.create_pen(0, 0, 0)

x1 = 0
y1 = HEIGHT // 2

x2 = WIDTH // 2
y2 = 0

incX = 0.25   # Speed control
accX = 0.0

incY = 0.1   # Speed control
accY = 0.0

# ------------------------- Loop ---------------------------------
while True:

    # Clear the display
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(ORANGE)
    display.pixel(x1, y1)
    display.pixel(x2, y2)

    if x1 > WIDTH:
        incX = -incX
        x1 = WIDTH
    elif x1 < 0:
        x1 = 0
        incX = -incX

    if y2 > HEIGHT:
        incY = -incY
        y2 = HEIGHT
    elif y2 < 0:
        y2 = 0
        incY = -incY

    accX += incX
    accY += incY

    x1 = int(accX)
    y2 = int(accY)

    # ----------- Update the display --------------------------
    i75.update()

