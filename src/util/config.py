# -*- coding: utf-8 -*-
"""
Define common file locations and constants
Created on Thu Oct 16 13:02:10 2025

@author: cassa
"""

import os
import pygame
from OpenGl.GL import *

"""
                            PATHS
"""
# getcwd() bc this script is called from main and main is located where all subfolders are
IMAGE_FOLDER = os.path.join(os.getcwd(), "images/")
UTIL_FOLDER = os.path.join(os.getcwd(), "util/")

"""
                            CONSTANTS
"""
TITLE = "GRAVITY BASIN"
DISPLAY_SIZE = (800, 600)
SCALE = (0.5, 0.5, 0.5)
TRANSLATE = (0.0, 0.0, -50)




"""
                            INITIAL SETUP/PROGRAM OPTIONS
"""
FLAGS = pygame.DOUBLEBUF | pygame.OPENGL

def setup():    
    # Initialize Pygame modules
    pygame.init()
    
    # Set up the display
    display = DISPLAY_SIZE
    flags = FLAGS
    pygame.display.set_mode(size=display, flags=flags)
    pygame.display.set_caption(TITLE)
    #Depth testing to ensure correct rendering of overlapping objects
    pygame.glEnable(GL_DEPTH_TEST)
    
    #Set up lighting
    gl.glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 5, 1)) # light position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) # diffuse light
    
    #Set up texturing 
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    
    #Earth texture loading
    # Place the texture loading code here
    earth_texture = pygame.load_texture(os.path.join(IMAGE_FOLDER, "earth.jpg"))
    
    #Hide cursor 
    pygame.mouse.set_visible(True)
        
    #Lock cursor to window
    pygame.event.set_grab(True)


