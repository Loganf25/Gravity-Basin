"""contains basic information for all solar system bodies"""
#mass in kilograms, radius in AU, distance from sun in Astronomical Units

PLANET_DATA = [
    {"name": "Sun",     "mass": 1.9885e30, "radius": 0.00465,   "distance_from_sun": 0.0,   "texture": "sun.jpg",     "color": (1.0, 1.0, 0.0), "axial_tilt": 0.0,   "rot_period": 600.0,  "eccentricity": 0.0},
    {"name": "Mercury", "mass": 3.3011e23, "radius": 0.0000163, "distance_from_sun": 0.39,  "texture": "mercury.jpg", "color": (0.7, 0.7, 0.7), "axial_tilt": 0.03, "rot_period": 1408.0, "eccentricity": 0.205},
    {"name": "Venus",   "mass": 4.8675e24, "radius": 0.0000405, "distance_from_sun": 0.72,  "texture": "venus.jpg",   "color": (1.0, 0.9, 0.6), "axial_tilt": 177.3,"rot_period": 5832.0, "eccentricity": 0.007},
    {"name": "Earth",   "mass": 5.97237e24,"radius": 0.0000426, "distance_from_sun": 1.0,   "texture": "earth.jpg",   "color": (0.2, 0.5, 1.0), "axial_tilt": 23.4, "rot_period": 23.9,   "eccentricity": 0.017},
    {"name": "Mars",    "mass": 6.4171e23, "radius": 0.0000227, "distance_from_sun": 1.52,  "texture": "mars.jpg",    "color": (0.8, 0.3, 0.2), "axial_tilt": 25.2, "rot_period": 24.6,   "eccentricity": 0.094},
    {"name": "Jupiter", "mass": 1.8982e27, "radius": 0.000467,  "distance_from_sun": 5.20,  "texture": "jupiter.jpg", "color": (0.9, 0.8, 0.5), "axial_tilt": 3.1,  "rot_period": 9.9,    "eccentricity": 0.049},
    {"name": "Saturn",  "mass": 5.6834e26, "radius": 0.000389,  "distance_from_sun": 9.58,  "texture": "saturn.jpg",  "color": (1.0, 0.9, 0.7), "axial_tilt": 26.7, "rot_period": 10.7,   "eccentricity": 0.057},
    {"name": "Uranus",  "mass": 8.6810e25, "radius": 0.000169,  "distance_from_sun": 19.22, "texture": "uranus.jpg",  "color": (0.5, 0.8, 1.0), "axial_tilt": 97.8, "rot_period": 17.2,   "eccentricity": 0.046},
    {"name": "Neptune", "mass": 1.02413e26,"radius": 0.000164,  "distance_from_sun": 30.05, "texture": "neptune.jpg", "color": (0.3, 0.5, 1.0), "axial_tilt": 28.3, "rot_period": 16.1,   "eccentricity": 0.011},
    {"name": "Pluto",   "mass": 1.303e22,  "radius": 0.00000794,"distance_from_sun": 39.48, "texture": "pluto.jpg",   "color": (0.8, 0.8, 0.7), "axial_tilt": 119.6,"rot_period": 153.3,  "eccentricity": 0.244}
]


#convert values for better viewing experience
for planet in PLANET_DATA:
    planet["radius"] = planet["radius"] * 1000
    if planet["name"] == "Sun":
        planet["radius"] = planet["radius"] / 10

planet_textures = {
    "sun":     "assets\\images\\sun.jpg",
    "mercury": "assets\\images\\mercury.jpg",
    "venus":   "assets\\images\\venus.jpg",
    "earth":   "assets\\images\\earth.jpg",
    "mars":    "assets\\images\\mars.jpg",
    "jupiter": "assets\\images\\jupiter.jpg",
    "saturn":  "assets\\images\\saturn.jpg",
    "uranus":  "assets\\images\\uranus.jpg",
    "neptune": "assets\\images\\neptune.jpg",
    "pluto":   "assets\\images\\pluto.jpg"
}


def get_planet_data(name):
    """return a single planet's data by name"""
    
    for planet in PLANET_DATA:
        if planet["name"].lower() == name.lower():
            return planet
    return None
