"""defines the Planet class extending CelestialBody"""

from src.simulation.data.simulation_data import get_planet_data
from src.simulation.models.celestial_body import CelestialBody

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
            texture=data["texture"]
        )

    def update(self, delta_time):
        """Update planet state"""
        # placeholder for motion/orbit updates

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
