import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Description:
# A demo to test a simple particle system with different colors.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Define a global flag
IS_MICROPYTHON = sys.implementation.name == 'micropython'

if IS_MICROPYTHON:
    # import machine # For Pin control, hardware I/O
    import utime as time # Use utime for time functions
else:
    import time # Use standard time module
    
import random
import math

if IS_MICROPYTHON:
    from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X128

    i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X128)
    display = i75.display

    WIDTH, HEIGHT = display.get_bounds()

    # Couple of colors for use later
    ORANGE = display.create_pen(255, 128, 0)
    BLACK = display.create_pen(0, 0, 0)

    # Universal Time Abstraction
    def get_monotonic_ms() -> any:
        # MicroPython uses ticks_ms() for its monotonic clock
        return time.ticks_ms()
    
    def universal_sleep_s(seconds):
        time.sleep_ms(int(seconds * 1000))

    def universal_sleep_ms(milliseconds: int):
        time.sleep_ms(milliseconds)
else:
    display = None
    WIDTH, HEIGHT = 128, 128

    ORANGE = None
    BLACK = None
    simFrameCount: int = 0

    # Universal Time Abstraction
    def get_monotonic_ms() -> int:
        global simFrameCount
        # Desktop Python uses time.monotonic() and converts to milliseconds
        sfc = simFrameCount 
        simFrameCount += 16.7
        return sfc #time.monotonic() * 1000
    
    def universal_sleep_s(seconds):
        time.sleep(seconds)

    def universal_sleep_ms(milliseconds: int):
        time.sleep(int(milliseconds) / 1000)

# Define the duration you want the loop to run (in seconds)
RUN_DURATION_MS = 10000  # Run for N seconds

MAX_PARTICLE_LIFETIME = 1.5
MAX_PARTICLE_SPEED = 1.0
MAX_EXPLOSIVE_PARTICLES = 100

COLORS = [
    display.create_pen(255, 0, 0), # red
    display.create_pen(0, 255, 0), # green
    display.create_pen(0, 0, 255), # blue
    display.create_pen(255, 255, 0), # yellow
    display.create_pen(255, 0, 255), # magenta
    display.create_pen(0, 255, 255), # cyan
    display.create_pen(255, 255, 255), # white
    display.create_pen(128, 128, 128), # gray
    display.create_pen(128, 0, 0), # dark red
    display.create_pen(0, 128, 0), # dark green
    display.create_pen(0, 0, 128), # dark blue
    display.create_pen(128, 128, 0), # dark yellow
    display.create_pen(128, 0, 128), # dark magenta
    display.create_pen(0, 128, 128), # dark cyan
    display.create_pen(192, 192, 192), # light gray
    display.create_pen(192, 0, 0), # light red
    display.create_pen(0, 192, 0), # light green
    display.create_pen(0, 0, 192), # light blue
    display.create_pen(192, 192, 0), # light yellow
    display.create_pen(192, 0, 192), # light magenta
    display.create_pen(0, 192, 192), # light cyan
]

# ------------------------------------------------------------------------
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def setByAngle(self, angleRadians: float):
        self.x = math.cos(angleRadians)
        self.y = math.sin(angleRadians)

v1 = Vector(0.0, 0.0)
v2 = Vector(0.0, 0.0)
v3 = Vector(0.0, 0.0)

def Add(v1: Vector, v2: Vector, v3: Vector):
    v3.x = v1.x + v2.x
    v3.y = v1.y + v2.y

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
        v2.x = point.x
        v2.y = point.y
        Add(v1, v2, v3)
        point.x = v3.x
        point.y = v3.y

# ------------------------------------------------------------------------
# A particle is a Node from Ranger
class Particle:
    died: bool = False
    color: any = None

    def __init__(self, elapsed: float, lifespan: float, active: bool, position: Point, velocity: Point):
        self.elapsed = elapsed
        self.lifespan = lifespan
        self.active = active
        self.position = position
        self.velocity = velocity

    def update(self, dt: float):
        self.elapsed += dt
        self.active = self.elapsed < self.lifespan

    def reset(self):
        self.elapsed = 0.0
        self.active = False
        self.died = False

    def setVelocity(self, angleRadians: float, speed: float):
        self.velocity.setDirectionByAngle(angleRadians)
        self.velocity.magnitude = speed

    def evaluate(self, dt: float) -> bool:
        self.update(dt)
        # Update particle's position as long as it is active.
        if (self.active):
            self.velocity.applyToPoint(self.position)

        return self.active

# ------------------------------------------------------------------------
# Activator
class Emitter:
    def __init__(self, direction: float, speed: float):
        self.direction = direction
        self.speed = speed

# ------------------------------------------------------------------------
class Emitter360(Emitter):
    def __init__(self, maxLifespan=MAX_PARTICLE_LIFETIME, maxSpeed=MAX_PARTICLE_SPEED):
        super().__init__(0.0, 0.0)
        self.maxLifespan = maxLifespan
        self.maxSpeed = maxSpeed

    def activate(self, particle: Particle, epiCenter: Point):
        self.direction =  random.uniform(0.0, 1.0) * math.pi * 2.0
        self.speed  =  0.05 + random.uniform(0.0, self.maxSpeed)

        particle.lifespan = (random.uniform(0.1, self.maxLifespan)) * 1000.0
        particle.reset()
        particle.position.x = epiCenter.x
        particle.position.y = epiCenter.y
        particle.active = True
        particle.velocity.setDirectionByAngle(self.direction)
        particle.velocity.magnitude = self.speed


class EmitterPlusX(Emitter):
    def __init__(self, maxLifespan=MAX_PARTICLE_LIFETIME, maxSpeed=MAX_PARTICLE_SPEED):
        super().__init__(
            0.0, # +X axis
            maxSpeed)
        self.maxLifespan = maxLifespan
        self.maxSpeed = maxSpeed

    def activate(self, particle: Particle, epiCenter: Point):
        self.direction =  0.0
        self.speed  =  random.uniform(0.0, 1.0) * self.maxSpeed

        particle.lifespan = random.uniform(0.0, 1.0) * self.maxLifespan * 1000.0
        particle.reset()
        particle.position.x = epiCenter.x
        particle.position.y = epiCenter.y
        particle.active = True

# ------------------------------------------------------------------------
class ParticleSystem:
    def __init__(self, numberOfParticles: int, autoTrigger: bool, emitter: Emitter):
        self.numberOfParticles = numberOfParticles
        self.autoTrigger = autoTrigger
        self.emitter = emitter
        self.particles: Particle = []
        # This counts how many particles are active
        self.particleCount = 0
        self.epiCenter: Point = Point(0.0, 0.0)
        self.active = False
        self.initialTrigger = True
    
    def addParticle(self, particle: Particle):
        self.particles.append(particle)

    def update(self, dt: float) -> bool:
        return False

    def isActive(self) -> bool:
        return self.particleCount > 0

    def generate(self):
        pass

    def resetToInitial(self):
        self.initialTrigger = True
        self.reset()

    def reset(self):
        for p in self.particles:
            p.reset()

    def draw(self):
        if IS_MICROPYTHON:
            for p in self.particles:
                if (p.active):
                    display.set_pen(p.color)
                    display.pixel(int(p.position.x), int(p.position.y))
        else:
            print("DRAW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            for p in self.particles:
                if (p.active):
                    print(f"pos: {p.position.x}, {p.position.y}")
                print(f"ela: E:{p.elapsed}, L:{p.lifespan}, A:{p.active}, D:{p.died}")

# ------------------------------------------------------------------------
# If autotrigger is On then we only want to trigger another explosion if
# all particles are dead. Each time a particle dies we decrement the count.
# When we trigger we set the count back.
class ExplosiveParticleSystem(ParticleSystem):

    def __init__(self, numberOfParticles: int, autoTrigger: bool, emitter: Emitter):
        super().__init__(numberOfParticles, autoTrigger, emitter)

    def generate(self):
        super().generate()
        for i in range(0, self.numberOfParticles):
            particle = Particle(
                    0.0, MAX_PARTICLE_LIFETIME, False, 
                    Point(0.0, 0.0), 
                    Velocity(MAX_PARTICLE_SPEED, 0.0, 1.0, Vector(1.0, 0.0), False)
                )
            particle.color = COLORS[random.randint(0, len(COLORS)-1)]
            self.addParticle(particle)

    def update(self, dt: float) -> bool:
        if (self.initialTrigger):
            # The system is starting.
            self.initialTrigger = False
            self.trigger()
        else:
            # The system is active. Evaluate current particles
            for p in self.particles:
                active = p.evaluate(dt)
                if (not active and not p.died): # Did it die AND not died already
                    self.particleCount -= 1
                    # We have recognized its death. Now it can officially die!
                    p.died = True
                self.active = self.isActive()
                if (not self.active):
                    # The system has become in-active.
                    if (self.autoTrigger):
                        self.trigger()                

        return self.active

    def trigger(self):
        self.reset()
        self.active = True

        for p in self.particles:
            self.emitter.activate(p, self.epiCenter)
            # Inc count because a new particle has become active
            self.particleCount += 1

# ------------------------------------------------------------------------
class OneshotParticleSystem(ParticleSystem):

    def __init__(self, numberOfParticles: int, autoTrigger: bool, emitter: Emitter):
        super().__init__(numberOfParticles, autoTrigger, emitter)

    def generate(self):
        super().generate()
        self.addParticle(
            Particle(
                0.0, 5.0, False, 
                Point(0.0, 0.0), 
                Velocity(MAX_PARTICLE_SPEED, 0.0, 1.0, Vector(1.0, 0.0), False)
            )
        )

    def update(self, dt: float) -> bool:
        # The system is either actively evaluating particles or all particles have
        # died which deactivates the system. The system can reactivate by
        # activating particles via the trigger if autoTrigger is set.

        if (self.initialTrigger):
            # The system is starting.
            self.initialTrigger = False
            self.trigger()
        else:
            # The system is active. Evaluate current particle
            for p in self.particles:
                active = p.evaluate(dt)
                if (not active): # Did it die
                    self.particleCount -= 1
                self.active = self.isActive()
                if (not self.active):
                    # The system has become in-active.
                    if (self.autoTrigger):
                        self.trigger()
                break
        
        return self.active

    def trigger(self):
        # print("============ Triggering ==================")
        self.reset()
        self.active = True

        for p in self.particles:
            self.emitter.activate(p, self.epiCenter)
            # Inc count because a new particle has become active
            self.particleCount += 1
            break

# ------------------------------------------------------------------------

class Demo:
    prevTicks = get_monotonic_ms()
    particleSystem: ParticleSystem = None

    def __init__(self):
        self.generate()

    def generate(self):
        self.particleSystem = ExplosiveParticleSystem(MAX_EXPLOSIVE_PARTICLES, True, Emitter360())
        self.particleSystem.epiCenter = Point(WIDTH / 2.0, HEIGHT / 2.0)
        self.particleSystem.generate()

    def reset(self):
        # Get the starting time
        self.prevTicks = 0

    def run(self):
        active = True
        while active:
            # Calc dt
            currentTicks = get_monotonic_ms()

            dt = currentTicks - self.prevTicks

            active = self.update(dt)
            self.draw()

            self.prevTicks = currentTicks

            if not IS_MICROPYTHON:
                universal_sleep_ms(17)
            
    def update(self, dt: float) -> bool:
        return self.particleSystem.update(dt)


    # Draw the particles
    def draw(self):
        if IS_MICROPYTHON:
            display.set_pen(BLACK)
            display.clear()

        self.particleSystem.draw()

        if IS_MICROPYTHON:
            i75.update()

demo = Demo()
demo.run()

print("==== Done ======")
