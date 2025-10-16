# -*- coding: utf-8 -*-
"""
Define events for use in the program

Created on Thu Oct 16 15:47:48 2025

@author: cassa
"""

import pygame
from OpenGL.GL import *
from OpenGL import *

class EventHandler:
    zoom = 0
    
    def __init__(self, zoom):
        self.zoom = zoom

    def __quit_program():
        pygame.quit()
        return
    
    def __zoom():
        if event.button == 4: #Scroll up
            self.zoom += 0.5
        if event.button == 5: #Scroll down
            self.zoom -= 0.5
    
        #Clamp zoom level
        if self.zoom < 10: zoom = 10
        if self.zoom > 1000: zoom = 100
    
        #Update projection matrix with new zoom level
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.zoom, (display[0]/display[1]), 0.1, 50.0)
    
        #Reset model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
        #Apply scale
        glScalef(0.5, 0.5, 0.5)
    
        #Move back to view the sphere
        glTranslatef(0.0, 0.0, -10)
    
    def __handle_mouse():
        if pygame.mouse.get_pressed()[0]:
            #Get relative mouse movement
            mouse_motion_x, mouse_motion_y = event.rel
    
            #Update rotation angles based on mouse movement
            rotation_x += mouse_motion_y * 0.01
            rotation_y += mouse_motion_x * 0.01
    
            #Clamp vertical rotation to avoid flipping
            if rotation_y > 90: rotation_y = 90
            if rotation_y < -90: rotation_y = -90

    
    def handle_event(event):
        type_ = event.type
        
        if type_ == pygame.QUIT:
           __quit_program() 
        elif type_ == pygame.MOUSEBUTTONDOWN:
            __zoom()
        elif type_ == pygame.MOUSEMOTION:
            __handle_mouse()
            