"""Module to handle the orbits of celestial bodies."""
import math
import numpy as np
from simulation.services.physics_service import G

class OrbitService:
    """Service to manage and compute orbits of celestial bodies."""
    def __init__(self, physics_service):
        self.physics_service = physics_service

    def compute_orbit(self, body1, body2):
        """
        Compute the orbital parameters of body1 around body2.
        Inputs:
            body1: The celestial body to compute the orbit for (e.g., a satellite)
            body2: The central celestial body (e.g., a planet)
        Returns:
            A dictionary with orbital parameters such as distance and orbital velocity.
        """
        dx = body2.position[0] - body1.position[0]
        dy = body2.position[1] - body1.position[1]
        dz = body2.position[2] - body1.position[2]

        distance = body1.distance  # Use the unscaled distance for physics calculation
        visual_distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if visual_distance == 0:
            return None

        # Compute orbital velocity
        orbital_velocity = math.sqrt(G * body2.mass / distance)

        # Direction vector from body1 to body2
        direction = np.array([dx, dy, dz]) / visual_distance

        # Perpendicular vector for velocity direction (simple cross product with arbitrary vector)
        arbitrary_vector = np.array([0.0, 1.0, 0.0])
        velocity_direction = np.cross(direction, arbitrary_vector)
        velocity_direction /= np.linalg.norm(velocity_direction)

        # Set the velocity of body1 for a circular orbit
        body1.velocity = (orbital_velocity * velocity_direction).tolist()

        return {
            "distance": distance,
            "orbital_velocity": orbital_velocity
        }
