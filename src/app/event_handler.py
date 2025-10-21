# -*- coding: utf-8 -*-
"""
Define events for use in the program

Created on Thu Oct 16 15:47:48 2025

@author: cassa
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import *
from util import config

class EventHandler:
    zoom = 45.0
    rotation_x = 0.0
    rotation_y = 0.0
    
    def __init__(self, zoom):
        self.zoom = float(zoom)
        self.rotation_x = 0.0
        self.rotation_y = 0.0

    def __quit_program(self):
        pygame.quit()
        config.RUN_FLAG = False
        return
    
    def __zoom(self, event):
        if event.button == 4: #Scroll up
            self.zoom += 0.5
        if event.button == 5: #Scroll down
            self.zoom -= 0.5
    
        #Clamp zoom level
        if self.zoom < 10: zoom = 10
        if self.zoom > 1000: zoom = 100
    
    
    def __handle_mouse(self, event):
        if event.type != pygame.MOUSEMOTION:
            return
        if pygame.mouse.get_pressed()[0]:
            #Get relative mouse movement
            mouse_motion_x, mouse_motion_y = event.rel
    
            #Update rotation angles based on mouse movement
            sensitivity = 0.2
            self.rotation_x += mouse_motion_y * sensitivity
            self.rotation_y += mouse_motion_x * sensitivity
    
            #Clamp vertical rotation to avoid flipping
            if self.rotation_y > 90: self.rotation_y = 90
            if self.rotation_y < -90: self.rotation_y = -90

    
    def handle_event(self, event):
        type_ = event.type
        
        if type_ == pygame.QUIT:
           self.__quit_program() 
        elif type_ == pygame.MOUSEBUTTONDOWN:
            self.__zoom(event)
        elif type_ == pygame.MOUSEMOTION:
            self.__handle_mouse(event)
            