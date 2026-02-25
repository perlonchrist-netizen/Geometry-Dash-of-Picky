"""
Effets de particules.

Ce module definit la classe `Particle` utilisee pour:
- la poussiere au contact du sol,
- les effets visuels lors de l'activation des portails,
- une animation simple avec vitesse, gravite locale et fade-out.
"""
import pygame
import random


class Particle:
    def __init__(self, x, y, color=None, kind="dust", intensity=1.0):
        self.kind = kind
        self.intensity = max(0.5, float(intensity))

        if self.kind == "portal":
            self.x = x + random.randint(-14, 14)
            self.y = y + random.randint(-12, 12)
            self.vx = random.uniform(-2.6, 2.6) * self.intensity
            self.vy = random.uniform(-2.6, 2.6) * self.intensity
            self.gravity = 0.03
            self.size = random.uniform(2, 5) * min(1.8, self.intensity)
            self.lifetime = int(34 * self.intensity)
            self.color = color if color is not None else (220, 220, 220)
        else:
            # Poussiere: emission derriere le joueur, vers la gauche.
            self.x = x + random.randint(-6, 2)
            self.y = y + random.randint(-3, 2)
            self.vx = random.uniform(-3.2, -0.6) * self.intensity
            self.vy = random.uniform(-1.7, -0.2) * self.intensity
            self.gravity = 0.09
            self.size = random.uniform(1.8, 4.0) * min(1.6, self.intensity)
            self.lifetime = int(24 * self.intensity)
            self.color = color if color is not None else (170, 170, 170)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        self.size *= 0.97

    def draw(self, surface):
        if self.lifetime > 0 and self.size > 0.2:
            alpha = min(255, self.lifetime * 10)
            radius = max(1, int(self.size))
            particle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surf,
                (*self.color, alpha),
                (radius, radius),
                radius,
            )
            surface.blit(particle_surf, (self.x - radius, self.y - radius))
