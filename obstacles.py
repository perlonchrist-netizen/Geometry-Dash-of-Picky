"""
Definition et rendu des obstacles.

Ce module implemente la classe `Obstacle`:
- selection des dimensions/couleurs selon le type,
- dessin des formes (pics, cube),
- hitbox adaptee pour les collisions de gameplay,
- deplacement horizontal avec la vitesse du jeu.
"""
import pygame
from settings import *

class Obstacle:
    def __init__(self, x, obstacle_type):
        self.x = x
        self.type = obstacle_type
        self.width = OBSTACLE_TYPES[obstacle_type]["width"]
        self.height = OBSTACLE_TYPES[obstacle_type]["height"]
        self.color = OBSTACLE_TYPES[obstacle_type]["color"]
    
    def draw(self, surface, ground_y):
        if self.type in ["spike", "long_spike", "mini_spike"]:
            points = [(self.x + self.width//2, ground_y - self.height), 
                     (self.x, ground_y), 
                     (self.x + self.width, ground_y)]
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, BLACK, points, 2)
        
        elif self.type == "cube":
            pygame.draw.rect(surface, self.color, 
                           (self.x, ground_y - self.height, self.width, self.height))
            pygame.draw.rect(surface, BLACK, 
                           (self.x, ground_y - self.height, self.width, self.height), 2)
    
    def get_hitbox(self, ground_y):
        # Hitboxes ajustées pour être plus permissives
        if self.type == "spike":
            return pygame.Rect(self.x + 10, ground_y - self.height + 15, 
                             self.width - 20, self.height - 15)
        elif self.type == "cube":
            return pygame.Rect(self.x, ground_y - self.height, 
                             self.width, self.height)
        elif self.type == "long_spike":
            return pygame.Rect(self.x + 15, ground_y - self.height + 10, 
                             self.width - 30, self.height - 10)
        elif self.type == "mini_spike":
            return pygame.Rect(self.x + 5, ground_y - self.height + 10, 
                             self.width - 10, self.height - 10)
    
    def update(self, game_speed):
        self.x -= game_speed