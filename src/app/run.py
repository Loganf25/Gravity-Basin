# -*- coding: utf-8 -*-
"""
Runs program
Created on Thu Oct 16 15:22:12 2025

@author: cassa
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import *
from util import config
from images import image
from gfx import draw, texture
from app import event_handler

def MainLoop(rotation_x, rotation_y, zoom):
    eventHandler = event_handler.EventHandler(zoom)

    # Main loop
    while config.RUN_FLAG:
        for event in pygame.event.get():
            print(event)
            eventHandler.handle_event(event)
                    
        #Clear screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Update projection matrix with new zoom level
        #Changed for more robust
        surface = pygame.display.get_surface()
        if surface:
            display = surface.get_size()
            glViewport(0, 0, display[0], display[1])
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(eventHandler.zoom, (display[0]/display[1]), 0.1, 50.0)
    
        #Reset model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #Apply scale
        glScalef(0.5, 0.5, 0.5)
    
        #Move back to view the sphere
        glTranslatef(0.0, 0.0, -10)
    
        #Apply rotations based on mouse movement
        glRotatef(eventHandler.rotation_y, 0, 1, 0)  
        glRotatef(eventHandler.rotation_x, 1, 0, 0)
    
        #Load all planet image textures
        planet_images = image.create_images(config.SUPPORTED_PLANETS)
        #TODO: Add menu functionality here
        image.load_images(planet_images)
    
        # Draw the textured spherefv
        earth_texture = planet_images["earth"].texture_id
        glBindTexture(GL_TEXTURE_2D, earth_texture)
        draw_obj = draw.Draw()
        draw_obj.draw_sphere(earth_texture)
    
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
    
    #Hide cursor 
    pygame.mouse.set_visible(config.CURSOR_VISIBILITY)
        
    #Lock cursor to window
    pygame.event.set_grab(config.CURSOR_LOCK)

def run():
    setup()
    rotation_x = 0
    rotation_y = 0
    zoom = 45.0
    MainLoop(rotation_x, rotation_y, zoom)