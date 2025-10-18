# -*- coding: utf-8 -*-
"""
Defines an image class

Created on Thu Oct 16 15:25:19 2025

@author: cassa
"""

import os
from util import config
from gfx import texture
from app import planet

class image:
    name = None
    f_path = None
    texture_id = None
    
    def __init__(self, name):
        self.name = name.lower()
        self.f_path = os.path.join(config.IMAGE_FOLDER, name + '.jpg')

# create list that has all the planetary images in it
def create_images(planets):
    planet_images = {}
    for planet_ in planets:
        planet_images.setdefault(planet_.name, image(planet_.name))
    return (planet_images)

# loads in the textures for all planet images in the folder
def load_images(planet_images):
    for imag in planet_images.values():
        texture_obj = texture(imag[1].f_path)
        imag[1].texture_id = texture_obj.load_texture()