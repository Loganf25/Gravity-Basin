# -*- coding: utf-8 -*-
"""
Define common file locations and constants
Created on Thu Oct 16 13:02:10 2025

@author: cassa
"""

import os
import pygame
from OpenGL.GL import *
from OpenGL import *
from app import planet

"""
                            PATHS
"""
# getcwd() bc this script is called from main and main is located where all subfolders are
IMAGE_FOLDER = os.path.join(os.getcwd(), "images/")
UTIL_FOLDER = os.path.join(os.getcwd(), "util/")
APP_FOLDER = os.path.join(os.getcwd(), "app/")

"""
                            CONSTANTS
"""
TITLE = "GRAVITY BASIN"
DISPLAY_SIZE = (800, 600)
SCALE = (0.5, 0.5, 0.5)
TRANSLATE = (0.0, 0.0, -50)
SUPPORTED_PLANETS = [planet.Planet("Earth")]




"""
                            INITIAL SETUP/PROGRAM OPTIONS
"""
FLAGS = pygame.DOUBLEBUF | pygame.OPENGL
CURSOR_VISIBILITY = True
CURSOR_LOCK = False
RUN_FLAG = True
