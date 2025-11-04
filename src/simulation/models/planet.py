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
