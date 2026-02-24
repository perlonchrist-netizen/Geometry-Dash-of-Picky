"""
Portails de gravite.

Ce module fournit la classe `GravityPortal`:
- apparence et animation du portail,
- hitbox de declenchement,
- transport de l'effet de gravite applique au joueur,
- deplacement dans le decor defilant.
"""
import pygame
import math
from settings import *

class GravityPortal:
    def __init__(self, x, portal_type):
        self.x = x
        self.width = 40
        self.height = 60
        self.portal_type = portal_type
        self.gravity_multiplier = PORTAL_TYPES[portal_type]["multiplier"]
        self.color = PORTAL_TYPES[portal_type]["color"]
        self.effect = PORTAL_TYPES[portal_type]["name"]
        self.activated = False
        self.animation_offset = 0
    
    def draw(self, surface, ground_y):
        self.animation_offset = (self.animation_offset + 0.2) % (2 * math.pi)
        portal_y = ground_y - self.height//2 - 20
        
        # Corps du portail
        pygame.draw.ellipse(surface, self.color, 
                          (self.x, portal_y, self.width, self.height))
        pygame.draw.ellipse(surface, BLACK, 
                          (self.x, portal_y, self.width, self.height), 2)
        
        # Anneau intérieur tournant
        inner_width = self.width - 10
        inner_height = self.height - 10
        inner_x = self.x + 5
        inner_y = portal_y + 5
        
        num_points = 8
        for i in range(num_points):
            angle = (2 * math.pi * i / num_points) + self.animation_offset
            point_x = inner_x + inner_width//2 + math.cos(angle) * (inner_width//3)
            point_y = inner_y + inner_height//2 + math.sin(angle) * (inner_height//3)
            pygame.draw.circle(surface, BLACK, (int(point_x), int(point_y)), 3)
        
        # Texte d'effet
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(self.effect, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width//2, portal_y - 15))
        surface.blit(text, text_rect)
    
    def get_hitbox(self, ground_y):
        return pygame.Rect(self.x, ground_y - self.height - 20, self.width, self.height)
    
    def apply_effect(self):
        self.activated = True
    
    def update(self, game_speed):
        self.x -= game_speed