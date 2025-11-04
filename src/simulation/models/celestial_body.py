
# celestial_body.py
# base class for all astronomical bodies

class CelestialBody:
    def __init__(self, name, mass, radius, distance, color, texture):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.distance = distance
        self.color = color
        self.texture = texture

        # placeholder attributes for simulation (units scaled later by Engine)
        self.position = [distance, 0.0, 0.0]  # starting on X-axis
        self.velocity = [0.0, 0.0, 0.0]

        # visual rotation (degrees)
        self.rotation_angle = 0.0
        self.rotation_speed = 5.0  # degrees per second, visual only

    def update(self, delta_time):
        # override in subclass; call tick_rotation for visual spinning
        self.tick_rotation(delta_time)

    def tick_rotation(self, delta_time):
        # increment rotation angle for visual effect
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * delta_time) % 360.0

    def render(self):
        # override in subclass
        pass
