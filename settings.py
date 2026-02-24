"""
Configuration globale du jeu.

Ce module centralise:
- dimensions et cadence d'affichage,
- palette de couleurs,
- constantes physiques (gravite, saut, vitesse),
- definitions des types d'obstacles et de portails.
"""
import pygame

# Initialisation pygame pour les couleurs
pygame.init()

# Dimensions
WIDTH, HEIGHT = 900, 400
GROUND_Y = 320
FPS = 60

# Couleurs
BG_COLOR = (30, 30, 40)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (20, 20, 20)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_PURPLE = (75, 0, 130)

# Paramètres du jeu
BASE_GRAVITY = 0.8
BASE_JUMP_POWER = -12
GAME_SPEED = 6
PLAYER_SIZE = 40
PLAYER_X = 100
MAX_JUMPS = 2

# Types d'obstacles
OBSTACLE_TYPES = {
    "spike": {"width": 40, "height": 40, "color": RED},
    "cube": {"width": 40, "height": 40, "color": GREEN},
    "long_spike": {"width": 80, "height": 40, "color": YELLOW},
    "mini_spike": {"width": 20, "height": 30, "color": ORANGE}
}

# Types de portails
PORTAL_TYPES = {
    "low": {"multiplier": 0.5, "color": LIGHT_BLUE, "name": "LOW GRAVITY"},
    "high": {"multiplier": 2.0, "color": DARK_PURPLE, "name": "HIGH GRAVITY"},
    "normal": {"multiplier": 1.0, "color": WHITE, "name": "NORMAL"}
}
