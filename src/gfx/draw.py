# -*- coding: utf-8 -*-
"""
Defines a class for drawing commonly used shapes and textures (may be too large)
Created on Fri Oct 17 12:19:18 2025

@author: cassa
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Draw:    
    def __init__(self): # this is needed for class but class has no variables
        self=self
    
    def draw_sphere(self, texture_id):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, texture_id)
    
        #Create sphere object
        #A quadric object is used to define properties for rendering quadric shapes (spheres, cylinders, etc.)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
    
        #Draw sphere with radius 1, 32 slices and 32 stacks
        gluSphere(quadric, 1, 32, 32)
    
        # Clean up
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
