"""
settings.py
-----------
This module contains the configuration settings for the platform game.
Dependencies: pygame, random, os.path
"""

import pygame
import random
import os.path

TITLE = "Space Jump"
WIDTH = 600
HEIGHT = 800
FPS = 60
FONT_NAME = 'arial'

img_dir = os.path.join(os.path.dirname(__file__), '..', 'img')

# Player properties
PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.04
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 10
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 1

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# Defined colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLUE