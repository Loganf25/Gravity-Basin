
# planet.py
# defines the Planet class extending CelestialBody
# imports base data (mass, radius, texture, etc.) from simulation_data

from simulation.data.simulation_data import get_planet_data
from simulation.models.celestial_body import CelestialBody

class Planet(CelestialBody):
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
        # placeholder for motion/orbit updates
        pass

    def render(self):
        # placeholder for OpenGL draw calls (sphere with texture)
        pass
