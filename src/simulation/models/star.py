
# star.py
# defines the Star class extending CelestialBody
# mostly identical to Planet for now (later may add light emission logic)

from simulation.data.simulation_data import get_planet_data
from simulation.models.celestial_body import CelestialBody

class Star(CelestialBody):
    def __init__(self, name="Sun"):
        data = get_planet_data(name)
        if data is None:
            raise ValueError("Star data not found for: " + str(name))

        super().__init__(
            name=data["name"],
            mass=data["mass"],
            radius=data["radius"],
            distance=data["distance_from_sun"],
            color=data["color"],
            texture=data["texture"]
        )

    def update(self, delta_time):
        # stars typically static in center for this simulation
        pass

    def render(self):
        # placeholder for OpenGL draw calls (emissive sphere)
        pass
