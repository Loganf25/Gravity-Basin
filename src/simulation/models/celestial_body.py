"""base class for all astronomical bodies"""
import math

class CelestialBody:
    """Base class for celestial bodies in the simulation."""
    def __init__(self, name, mass, radius, distance, color, texture, axial_tilt):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.distance = distance
        self.color = color
        self.texture = texture
        self.axial_tilt = axial_tilt
        # placeholder attributes for simulation (units scaled later by Engine)
        self.position = [distance, 0.0, 0.0]  # starting on X-axis
        self.velocity = [0.0, 0.0, 0.0]

        # visual rotation (degrees)
        self.rotation_angle = 0.0
        self.rotation_speed = 5.0  # degrees per second, visual only

    #setters and getters for manipulated attributes
    def get_name(self):
        return self.name
    def get_mass(self):
        return self.mass
    def get_volume(self):
        return self.calc_volume()
    def get_density(self):
        return self.calc_density()

    def calc_volume(self):
        return (4/3) * 3.1415926 * (self.radius ** 3)
    
    def calc_density(self):
        return self.mass / self.calc_volume()
    
    def calc_radius(self, volume):
        return math.pow(((3/(4*3.1415926))*volume),1/3)

    # essentially just calulates how the relationship of mass = density * volume values changes when locking one variable and modifying another
    def recalculate(self, lock, modifier, attribute):
        density = self.calc_density()
        volume = self.calc_volume()

        match lock:

            case 0:
                pass
            case 1: #mass locked
                match attribute:
                    case 1: #modifying volume
                        volume = volume * modifier
                        density = self.mass / volume
                        self.radius = self.calc_radius(volume)
                    case 2: #modifying density
                        density = density * modifier
                        volume = self.mass / density
                        self.radius = self.calc_radius(volume)
            case 2: #volume locked
                match attribute:
                    case 0: #modifying mass
                        self.mass = self.mass * modifier
                        density = self.mass / volume
                    case 2: #modifying density
                        density = density * modifier
                        self.mass = density * volume
            case 3: #density locked
                match attribute:
                    case 0: #modifying mass
                        self.mass = self.mass * modifier
                        volume = self.mass / density
                        self.radius = self.calc_radius(volume)
                    case 1: #modifying volume
                        volume = volume * modifier
                        self.mass = density * volume
                        self.radius = self.calc_radius(volume)

    def update(self, delta_time):
        """Update celestial body state"""
        # override in subclass; call tick_rotation for visual spinning
        self.tick_rotation(delta_time)

    def tick_rotation(self, delta_time):
        """Update rotation angle for visual effect."""
        # increment rotation angle for visual effect
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * delta_time) % 360.0

    def render(self):
        """Render the celestial body"""
        # override in subclass
