"""
Logique du joueur.

Ce module gere:
- la physique verticale (gravite/saut),
- les collisions avec le sol et les cubes,
- la rotation visuelle du cube,
- l'etat "au sol" utilise pour certains effets (ex: poussiere).
"""
import pygame
from settings import *

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = PLAYER_X
        self.y = GROUND_Y - self.size
        self.velocity_y = 0
        self.rotation = 0
        self.is_jumping = False
        self.jumps_remaining = MAX_JUMPS
        self.max_jumps = MAX_JUMPS
        self.gravity_effect = "NORMAL"
    
    def jump(self, jump_power):
        if self.jumps_remaining > 0:
            self.velocity_y = jump_power
            self.jumps_remaining -= 1
            self.is_jumping = True
            if self.jumps_remaining == 0:
                self.rotation = 30
    
    def update(self, gravity, obstacles):
        # 1. Appliquer la gravité
        self.velocity_y += gravity
        self.y += self.velocity_y
        
        landed_on_cube = False
        player_rect = self.get_hitbox()

        # 2. Gestion des collisions avec les Cubes (Plateformes)
        for obs in obstacles:
            if obs.type == "cube":
                obs_rect = obs.get_hitbox(GROUND_Y)
                if player_rect.colliderect(obs_rect):
                    # Si on tombe sur le dessus du cube
                    if self.velocity_y >= 0 and (self.y + self.size) <= (obs_rect.top + self.velocity_y + 10):
                        self.y = obs_rect.top - self.size
                        self.velocity_y = 0
                        self.is_jumping = False
                        self.jumps_remaining = self.max_jumps
                        landed_on_cube = True

        # 3. Vérifier le sol
        was_in_air = self.y < GROUND_Y - self.size
        if self.y >= GROUND_Y - self.size:
            self.y = GROUND_Y - self.size
            self.velocity_y = 0
            self.is_jumping = False
            self.jumps_remaining = self.max_jumps

        # 4. ---  ROTATION  ---
        if self.is_jumping or self.y < GROUND_Y - self.size:
            # Si on est posé (sur un cube ou au sol), on arrête la rotation
            if self.velocity_y == 0:
                self.rotation %= 360
                if self.rotation != 0:
                    self.rotation = 0 
            else:
                # Sinon on tourne selon le nombre de sauts
                if self.jumps_remaining == 0:
                    self.rotation -= 8
                else:
                    self.rotation -= 6
        else:
            self.rotation = 0
        
        # Retourne True si on vient d'atterrir (pour les particules dans main.py)
        return (was_in_air and self.velocity_y > 2) or landed_on_cube
    
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_on_ground(self, obstacles):
        if self.y >= GROUND_Y - self.size - 0.1:
            return True

        player_rect = self.get_hitbox()
        feet_rect = pygame.Rect(
            player_rect.left + 4,
            player_rect.bottom - 1,
            player_rect.width - 8,
            3,
        )

        for obs in obstacles:
            if obs.type != "cube":
                continue
            obs_rect = obs.get_hitbox(GROUND_Y)
            if feet_rect.colliderect(obs_rect) and abs(player_rect.bottom - obs_rect.top) <= 6:
                return True
        return False
    
    def reset(self):
        self.y = GROUND_Y - self.size
        self.velocity_y = 0
        self.jumps_remaining = self.max_jumps
        self.gravity_effect = "NORMAL"
    
    def draw(self, surface, gravity_color):
        player_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Dessiner le cube
        pygame.draw.rect(player_surface, BLACK, (0, 0, self.size, self.size))
        
        # Ajuster la couleur selon les sauts restants
        if self.jumps_remaining == 2:
            color = gravity_color
        elif self.jumps_remaining == 1:
            color = tuple(min(255, c + 50) for c in gravity_color)
        else:
            color = tuple(min(255, c + 100) for c in gravity_color)
        
        padding = 4
        pygame.draw.rect(
            player_surface,
            color,
            (padding, padding, self.size - padding*2, self.size - padding*2)
        )
        
        inner_padding = self.size // 3
        pygame.draw.rect(
            player_surface,
            BLACK,
            (inner_padding, inner_padding, self.size - inner_padding*2, self.size - inner_padding*2)
        )
        
        core_padding = int(self.size / 2.5)
        pygame.draw.rect(
            player_surface,
            color,
            (core_padding, core_padding, self.size - core_padding*2, self.size - core_padding*2)
        )
        
        # Rotation
        rotated_surface = pygame.transform.rotate(player_surface, self.rotation)
        rect = rotated_surface.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        surface.blit(rotated_surface, rect.topleft)
        
        # Afficher les sauts restants
        for i in range(self.jumps_remaining):
            circle_x = self.x + 10 + i * 15
            circle_y = self.y - 10
            pygame.draw.circle(surface, color, (circle_x, circle_y), 5)
            pygame.draw.circle(surface, BLACK, (circle_x, circle_y), 5, 1)