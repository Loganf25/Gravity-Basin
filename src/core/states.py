# -*- coding: utf-8 -*-
"""Simple class for storing preset states"""
from enum import Enum

class States(Enum):
    MENU = 1
    SIMULATION = 2
    PAUSE = 3
    EXIT = 4
    CREDITS = 5