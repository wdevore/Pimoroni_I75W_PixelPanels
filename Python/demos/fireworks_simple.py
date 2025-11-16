import time
import random
import math

from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X128

i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X128)
display = i75.display

WIDTH, HEIGHT = display.get_bounds()

# Couple of colors for use later
ORANGE = display.create_pen(255, 128, 0)
BLACK = display.create_pen(0, 0, 0)

# Define the duration you want the loop to run (in seconds)
RUN_DURATION_MS = 10000  # Run for N seconds

MAX_PARTICLE_LIFETIME = 1.0
MAX_PARTICLE_SPEED = 10.0

# A demo to test a simple particle system. The emitter sits in the middle
# and spews particles.

# ------------------------------------------------------------------------
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def setByAngle(self, angleRadians: float):
        self.x = math.cos(angleRadians)
        self.y = math.sin(angleRadians)

# ------------------------------------------------------------------------
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# ------------------------------------------------------------------------
# Velocity represents the direction and magnitude of a vector
# Velocity's direction is alway defined relative to the +X axis.
# Default direction is +X axis.
class Velocity:
    magnitude: float
    minMag: float
    maxMag: float
    direction: Vector
    limitMag: bool

    def __init__(self, magnitude: float, minMag: float, maxMag: float, direction: Vector, limitMag: bool):
        self.magnitude = magnitude
        self.minMag = minMag
        self.maxMag = maxMag
        self.direction = direction
        self.limitMag = limitMag

    def setDirectionByVector(self, vector: Point):
        pass

    def setDirectionByAngle(self, angleRadians: float):
        self.direction.setByAngle(angleRadians)

    def constrainMagnitude(self, constrain: bool):
        self.limitMag = constrain

    def applyToPoint(self, point: Point):
        v1.x = self.direction.x * self.magnitude
        v1.y = self.direction.y * self.magnitude


        pass
# ------------------------------------------------------------------------
# A particle is a Node from Ranger
class Particle:
    velocity: Velocity
    position: Point

    def __init__(self, elapsed: float, lifespan: float, active: bool, position: Point, velocity: Point):
        self.elapsed = elapsed
        self.lifespan = lifespan
        self.active = active

    def update(self, dt: float):
        self.elapsed += dt
        self.active = self.elapsed < self.lifespan

    def reset(self):
        self.elapsed = 0.0
        self.active = True

    def setVelocity(self, angleRadians: float, speed: float):
        self.velocity.setDirectionByAngle(angleRadians)
        self.velocity.magnitude = speed

    def evaluate(self, dt: float):
        self.elapsed += dt
        self.active = self.elapsed < self.lifespan

        # Update particle's position as long as it is active.
        if (self.active):
            self.velocity.applyToPoint(self.position)


v1 = Vector()
v2 = Vector()
v3 = Vector()

# ------------------------------------------------------------------------
class Emitter:
    def __init__(self, direction: float, speed: float):
        self.direction = direction
        self.speed = speed

# ------------------------------------------------------------------------
class Emitter360(Emitter):
    def __init__(self, maxLifespan=MAX_PARTICLE_LIFETIME, maxSpeed=MAX_PARTICLE_SPEED):
        super().__init__(
            random.uniform(0.0, 1.0) * 360.0,
            random.uniform(0.0, 1.0) * maxSpeed)
        self.maxLifespan = maxLifespan
        self.maxSpeed = maxSpeed

# ------------------------------------------------------------------------
class ParticleSystem:
    particles: Particle = []
    epiCenter: Point = Point(0.0, 0.0)

    def __init__(self, active: bool, autoTrigger: bool, activator: Emitter):
        self.active = active
        self.autoTrigger = autoTrigger
        self.activator = activator
       
# ------------------------------------------------------------------------

class Demo:
    prevTicks = time.ticks_ms()

    def __init__(self, particleSystem: ParticleSystem):
        self.generate()

    def generate(self):
        pass

    def reset(self):
        # Get the starting time
        self.startTicks = time.ticks_ms()

    def run(self):
        while True:
            # Calc dt
            currentTicks = time.ticks_ms()

            dt = time.ticks_diff(currentTicks, self.prevTicks)

            self.update(dt)
            self.draw()

            self.prevTicks = currentTicks
            
    def update(self, dt: float):
        pass

    # Draw the oranges
    def draw(self):
        display.set_pen(BLACK)
        display.clear()

        # for o in self.oranges:
        #     o.update()

        #     display.set_pen(o.pen)
        #     display.pixel(int(o.vector.x), int(o.vector.y))

        i75.update()

demo = Demo()

# ------------------------- Loop ---------------------------------
while True:

    display.set_pen(BLACK)
    display.clear()

    demo.run()

    # ----------- Update the display --------------------------
    # i75.update()

