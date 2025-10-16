# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 12:51:15 2025

Main file for gravity basin

@author: cassa
"""

import pygame
from OpenGL import *
from util.config import setup
from util import config


def MainLoop(rotation_x, rotation_y, zoom):
    # Main loop
    while True:
        for event in pygame.event.get():
            #Quit event handling
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #Zoom handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: #Scroll up
                    zoom += 0.5
                if event.button == 5: #Scroll down
                    zoom -= 0.5
    
                #Clamp zoom level
                if zoom < 10: zoom = 10
                if zoom > 1000: zoom = 100
    
                #Update projection matrix with new zoom level
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(zoom, (display[0]/display[1]), 0.1, 50.0)
    
                #Reset model view matrix
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
    
                #Apply scale
                glScalef(0.5, 0.5, 0.5)
    
                #Move back to view the sphere
                glTranslatef(0.0, 0.0, -10)
    
            #Mouse movement handling
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    #Get relative mouse movement
                    mouse_motion_x, mouse_motion_y = event.rel
    
                    #Update rotation angles based on mouse movement
                    rotation_x += mouse_motion_y * 0.01
                    rotation_y += mouse_motion_x * 0.01
    
                    #Clamp vertical rotation to avoid flipping
                    if rotation_y > 90: rotation_y = 90
                    if rotation_y < -90: rotation_y = -90
                    
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


if __name__ == "__main__":
    #Setup canvas
    setup()
    
    #Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, (display[0]/display[1]), 0.1, 50.0)
    
    #Model Matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    #Apply scale
    glScalef(config.SCALE)
    
    #Move back to view the sphere
    glTranslatef(config.TRANSLATE)
    
    
    # Main loop
    #Enable mouse look variables (set to zero)
    rotation_x, rotation_y, zoom = 0  

    MainLoop(rotation_x, rotation_y, zoom)