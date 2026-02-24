"""
Effets de particules.

Ce module definit la classe `Particle` utilisee pour:
- la poussiere au contact du sol,
- les effets visuels lors de l'activation des portails,
- une animation simple avec vitesse, gravite locale et fade-out.
"""
import pygame
import random
from settings import *

class Particle:
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)
        self.y = y - 5
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.size = random.randint(2, 5)
        self.lifetime = 30
        self.color = (200, 200, 200)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.lifetime -= 1
        self.size *= 0.98
    
    def draw(self, surface):
        if self.lifetime > 0:
            alpha = min(255, self.lifetime * 8)
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*self.color, alpha), 
                             (self.size, self.size), self.size)
            surface.blit(particle_surf, (self.x - self.size, self.y - self.size))
