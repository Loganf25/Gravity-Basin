"""Module to handle the orbits of celestial bodies."""
import math
from simulation.services.physics_service import G, AU_IN_METERS

class OrbitService:
    """Service to manage and compute orbits of celestial bodies."""
    def __init__(self):
        pass


    def compute_orbit(self, body1, body2, AU_VISUAL_SCALE):
        """
        Compute the orbital parameters of body1 around body2.
        Inputs:
            body1: The celestial body to compute the orbit for (e.g., a satellite)
            body2: The central celestial body (e.g., a planet)
        Returns:
            A dictionary with orbital parameters such as distance and orbital velocity.
        """
        au_dist = body1.distance
        eccen = body1.eccentricity

        #Handle either the sun or itself
        if au_dist == 0:
            return None
        
        #Get perihelion distance to the star
        peri_au = au_dist * (1 - eccen)
        peri_meters = peri_au * AU_IN_METERS

        #Put the body in its initial position
        #The perilhelion point from its star
        body1.position = [peri_au * AU_VISUAL_SCALE, 0.0, 0.0]

        #Calculate Velocity to push body around its sun
        #Based on Visviva Equation at the closest point
        #v = sqrt( (GM/a) * ((1+e)/(1-e)) )

        GM = G * body2.mass
        a_meters = au_dist * AU_IN_METERS
        
        vel_mag = math.sqrt((GM/a_meters) * ((1 + eccen) / (1 - eccen)))
        body1.velocity = [0.0, 0.0, vel_mag]

        return {
            "distance": peri_meters,
            "orbital_velocity": vel_mag
        }
