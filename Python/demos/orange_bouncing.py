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

# Define the duration you want the loop to run (in seconds)
RUN_DURATION_MS = 10000  # Run for N seconds

# Pixels fall from the top and bounce with friction. Then after some random
# amount of time they rise back to the top.

class VelocityVector:
    def __init__(self, ox: float, oy: float, x: float, y: float, v: float, e: float):
        self.ox = ox    # Original x,y coords
        self.oy = oy
        self.x = x      # Current x,y coords
        self.y = y
        self.v = v      # Velocity
        self.e = e      # Energy

    # v is typically -0.5
    # e is typically 1.0
    def set(self, ox: float, oy: float, x: float, y: float, v: float, e: float):
        self.ox = x
        self.oy = y
        self.x = x      # Current x,y coords
        self.y = y
        self.v = v      # Velocity
        self.e = e      # Energy

# A orange pixel
class Orange:
    def __init__(self, vector: VelocityVector, pen):
        self.vector = vector
        self.pen = pen

    def update(self):
        pass

class Demo:
    # This list only holds oranges that are on the board.
    oranges = []
    velocities = []
    startTicks = time.ticks_ms()
    gravity = 0.003    # Acceleration

    def __init__(self):
        self.generate()

    def generate(self):
        # Generate 32 oranges that can't overlap.
        for o in range(0, 32):
            foundOverlap = True

            # Continue to generate coordinates until a non-overlap occurs
            while foundOverlap:
                xc = random.uniform(0.0, 127.55)
                yc = random.uniform(0.0, 127.55)
                dy = random.uniform(0.01, 0.2)

                # Scan current oranges to see if there is a coordinate already present.
                if (self.checkForOverlap(xc, yc)):
                    continue

                foundOverlap = False

                v = VelocityVector(0.0, 0.0, round(xc), round(yc), dy, 1.0)

                self.oranges.append(Orange(v, ORANGE))

    def reset(self):
        self.oranges = []
        self.velocities = []
        self.generate()

        # Get the starting time
        self.startTicks = time.ticks_ms()

    # Check for overlaps
    def checkForOverlap(self, x: float, y: float):
        for o in self.oranges:
            if (o.vector.x == x and o.vector.y == y):
                return True
        return False

    # Gravity simulation sequence
    def gravitySequence(self):
        while time.ticks_diff(time.ticks_ms(), self.startTicks) < RUN_DURATION_MS:
            # Update velocities
            for o in self.oranges:
                # Gravity influences velocity accelerating it downward.
                o.vector.v += self.gravity
                o.vector.v = min(o.vector.v, 1.0) # Clamp max speed
                # Apply velocity to orange
                o.vector.y += o.vector.v

                if (o.vector.y > WIDTH - 1):
                    # Orange hit the bottom.
                    # Some energy was lost so the upward velocity is reduced.
                    # Or from the opposite perspective gravity influences more.
                    o.vector.y = WIDTH - 1  # Put orange back on board.

                    # Reduce velocity based on energy loss
                    # Increasing this value causes the particles to bounce with
                    # more energy. So smaller is more appropriate.
                    o.vector.v = -random.uniform(0.0, 0.4) / o.vector.e
                    # Increasing "e" causes the oranges to
                    # quickly lose energy and settle to the bottom.
                    # Decreasing causes them to "float" longer.
                    o.vector.e += 0.05

            self.draw()

            # Important: You must allow other things to happen (like the OS checking the clock)
            # A small sleep is often necessary, especially in MicroPython, to prevent the loop
            # from monopolizing the CPU and potentially freezing the system.
            # NOTE: This doesn't seem to have an impact on micropython.
            #time.sleep_ms(1) # Sleep for 2 milliseconds

    def run(self):
        # Loop continuously while the elapsed time is less than the RUN_DURATION
        while True:
            # TODO Determine what sequence to run next
            
            self.gravitySequence()

            self.reset()

    # Draw the oranges
    def draw(self):
        display.set_pen(BLACK)
        display.clear()

        for o in self.oranges:
            o.update()

            display.set_pen(o.pen)
            display.pixel(int(o.vector.x), int(o.vector.y))

        i75.update()

demo = Demo()

# ------------------------- Loop ---------------------------------
while True:

    display.set_pen(BLACK)
    display.clear()

    demo.run()

    # ----------- Update the display --------------------------
    # i75.update()

