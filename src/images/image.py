# -*- coding: utf-8 -*-
"""
Defines an image class

Created on Thu Oct 16 15:25:19 2025

@author: cassa
"""

import os
from util import config
from gfx import texture

class image:
    name = None
    f_path = None
    texture_id = None
    
    def __init__(self, name):
        self.name = name
        self.f_path = os.path.join(config.IMAGE_FOLDER, name + '.jpg')

# create list that has all the planetary images in it
def create_images():
                        # jpg files should follow this convention (lowercase)
    planet_images = {"Earth": image("earth"),
                     "Moon": image("moon"),
                     "Jupiter": image("jupiter")}
    return (planet_images)

# loads in the textures for all planet images in the folder
def load_images(planet_images):
    for imag in planet_images.items():
        texture_obj = texture(imag.f_path)
        imag.texture_id = texture_obj.load_texture()