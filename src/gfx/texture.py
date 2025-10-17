# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 12:39:17 2025

@author: cassa
"""

import pygame
from OpenGL.GL import *

class texture():
    fname = None
    texture_id = None
    def __init__(self, fname):
        self.fname=fname
    
    def load_texture(self):
        #Load an image file as a texture
        texture_surface = pygame.image.load(self.fname)
        #Convert the image to a string format suitable for OpenGL
        texture_data = pygame.image.tostring(texture_surface, "RGB", True)
        #Get image dimensions
        width = texture_surface.get_width()
        height = texture_surface.get_height()
    
        #Generate a texture ID and bind it
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    
        #Set texture parameters for wrapping and filtering
        # Repeat the texture in both directions
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
        # Use linear filtering for magnification and mipmap linear filtering for minification
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        return(self.texture_id)
    
    