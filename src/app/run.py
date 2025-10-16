# -*- coding: utf-8 -*-
"""
Runs program
Created on Thu Oct 16 15:22:12 2025

@author: cassa
"""

import pygame
from OpenGL.GL import *
from OpenGL import *
from util import config
from images import image
import event_handler

def MainLoop(rotation_x, rotation_y, zoom):
    # Main loop
    while True:
        for event in pygame.event.get():
            eventHandler = event_handler.EventHandler(zoom)
            eventHandler.handle_event(event)
                    
    #Clear screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #Apply rotations based on mouse movement
    glRotatef(rotation_x, 1, 0, 0)  
    glRotatef(rotation_y, 0, 1, 0)

    # Draw the textured sphere
    glBindTexture(GL_TEXTURE_2D, earth_texture)
    draw_sphere(earth_texture)

    pygame.display.flip()
    pygame.time.wait(10)



def setup():
    # Initialize Pygame modules
    pygame.init()
    
    # Set up the display
    display = config.DISPLAY_SIZE
    flags = config.FLAGS
    pygame.display.set_mode(size=display, flags=flags)
    pygame.display.set_caption(config.TITLE)
    #Depth testing to ensure correct rendering of overlapping objects
    glEnable(GL_DEPTH_TEST)
    
    #Set up lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 5, 1)) # light position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) # diffuse light
    
    #Set up texturing 
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    
    #Earth texture loading
    # Place the texture loading code here
    planet_images = image.create_images()
    earth_texture = load_texture(planet_images["Earth"].f_path)
    
    #Hide cursor 
    pygame.mouse.set_visible(CURSOR_VISIBILITY)
        
    #Lock cursor to window
    pygame.event.set_grab(CURSOR_LOCK)

def run():
    setup()
    MainLoop()