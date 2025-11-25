"""defines the Planet class extending CelestialBody"""

from simulation.data.simulation_data import get_planet_data
from simulation.models.celestial_body import CelestialBody

class Planet(CelestialBody):
    """Class representing a planet in the simulation, extending CelestialBody."""
    def __init__(self, name):

        data = get_planet_data(name)

        if data is None:
            raise ValueError("Planet data not found for: " + str(name))
        
        super().__init__(
            name=data["name"],
            mass=data["mass"],
            radius=data["radius"],
            distance=data["distance_from_sun"],
            color=data["color"],
            texture=data["texture"],
            axial_tilt=data["axial_tilt"],
        )
        # Additional planet-specific attributes
        #Rotation period in hours to seconds
        period_hours = data.get("rot_period", 24.0)
        if period_hours != 0:
            self.rotation_speed = 360.0 / (period_hours * 3600.0)  # degrees per second
        else:
            self.rotation_speed = 0.0

        self.eccentricity=data["eccentricity"]


    def update(self, delta_time):
        """Update planet state"""
        # Apply rotation
        self.tick_rotation(delta_time)

    def render(self):
        """Render the planet"""
        # placeholder for OpenGL draw calls (sphere with texture)

    #Setters and Getters
    def change_name(self, name):
        """Change the name of the planet."""
        self.name = name
    def get_name(self):
        """Get the name of the planet."""
        return self.name
    def change_mass(self, mass):
        """Change the mass of the planet."""
        self.mass = mass
    def get_mass(self):
        """Get the mass of the planet."""
        return self.mass
    def change_radius(self, radius):
        """Change the radius of the planet."""
        self.radius = radius
    def get_radius(self):
        """Get the radius of the planet."""
        return self.radius
    def change_distance(self, distance):
        """Change the distance of the planet."""
        self.distance = distance
    def get_distance(self):
        """Get the distance of the planet."""
        return self.distance
    def change_color(self, color):
        """Change the color of the planet."""
        self.color = color
    def get_color(self):
        """Get the color of the planet."""
        return self.color
    def change_texture(self, texture):
        """Change the texture of the planet."""
        self.texture = texture
    def get_texture(self):
        """Get the texture of the planet."""
        return self.texture
