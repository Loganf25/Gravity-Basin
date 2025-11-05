"""contains basic information for all solar system bodies"""
#distances in AU (astronomical units), mass in kg, radius in km

PLANET_DATA = [
    {"name": "Sun",     "mass": 1.9885e30, "radius": 0.46,    "distance_from_sun": 0.0,   "texture": "sun.jpg",     "color": (1.0, 1.0, 0.0)},
    {"name": "Mercury", "mass": 3.3011e23, "radius": 0.0016,  "distance_from_sun": 0.39,  "texture": "mercury.jpg", "color": (0.7, 0.7, 0.7)},
    {"name": "Venus",   "mass": 4.8675e24, "radius": 0.0040,  "distance_from_sun": 0.72,  "texture": "venus.jpg",   "color": (1.0, 0.9, 0.6)},
    {"name": "Earth",   "mass": 5.97237e24,"radius": 0.0042,  "distance_from_sun": 1.0,   "texture": "earth.jpg",   "color": (0.2, 0.5, 1.0)},
    {"name": "Mars",    "mass": 6.4171e23, "radius": 0.0023,  "distance_from_sun": 1.52,  "texture": "mars.jpg",    "color": (0.8, 0.3, 0.2)},
    {"name": "Jupiter", "mass": 1.8982e27, "radius": 0.0466,  "distance_from_sun": 5.20,  "texture": "jupiter.jpg", "color": (0.9, 0.8, 0.5)},
    {"name": "Saturn",  "mass": 5.6834e26, "radius": 0.0387,  "distance_from_sun": 9.58,  "texture": "saturn.jpg",  "color": (1.0, 0.9, 0.7)},
    {"name": "Uranus",  "mass": 8.6810e25, "radius": 0.0168,  "distance_from_sun": 19.22, "texture": "uranus.jpg",  "color": (0.5, 0.8, 1.0)},
    {"name": "Neptune", "mass": 1.02413e26,"radius": 0.0163,  "distance_from_sun": 30.05, "texture": "neptune.jpg", "color": (0.3, 0.5, 1.0)},
    {"name": "Pluto",   "mass": 1.303e22,  "radius": 0.0008,  "distance_from_sun": 39.48, "texture": "pluto.jpg",    "color": (0.8, 0.8, 0.7)}
]


planet_textures = {
    "sun": "assets/images/sun.jpg",
    "mercury": "assets/images/mercury.jpg",
    "venus": "assets/images/venus.jpg",
    "earth": "assets/images/earth.jpg",
    "mars": "assets/images/mars.jpg",
    "jupiter": "assets/images/jupiter.jpg",
    "saturn": "assets/images/saturn.jpg",
    "uranus": "assets/images/uranus.jpg",
    "neptune": "assets/images/neptune.jpg",
    "pluto": "assets/images/pluto.jpg"
}


def get_planet_data(name):
    """return a single planet's data by name"""
    for planet in PLANET_DATA:
        if planet["name"].lower() == name.lower():
            return planet
    return None
