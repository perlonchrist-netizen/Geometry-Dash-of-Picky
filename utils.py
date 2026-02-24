"""
Fonctions utilitaires du gameplay et du rendu.

Ce module propose:
- le dessin du sol avec effet de defilement,
- le calcul gravite/saut selon le multiplicateur de portail,
- la couleur associee a l'etat de gravite courant.
"""
import pygame
from settings import *

def draw_floor(surface):
    """Dessine le sol avec effet de défilement"""
    pygame.draw.rect(surface, DARK_GREY, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(surface, CYAN, (0, GROUND_Y, WIDTH, 4))
    
    # Motifs décoratifs
    for i in range(0, WIDTH, 100):
        x = (i + pygame.time.get_ticks() // 10) % (WIDTH + 100) - 100
        pygame.draw.line(surface, (40, 40, 40), 
                        (x, GROUND_Y + 10), (x + 50, HEIGHT), 3)

def update_gravity_and_jump(gravity_multiplier, base_gravity, base_jump_power):
    """Calcule la nouvelle gravité et force de saut"""
    gravity = base_gravity * gravity_multiplier
    
    if gravity_multiplier < 1:
        jump_power = base_jump_power * 0.8
        effect = "LOW GRAVITY"
    elif gravity_multiplier > 1:
        jump_power = base_jump_power * 1.5
        effect = "HIGH GRAVITY"
    else:
        jump_power = base_jump_power
        effect = "NORMAL"
    
    return gravity, jump_power, effect

def get_gravity_color(effect):
    """Retourne la couleur associée à l'effet de gravité"""
    if effect == "LOW GRAVITY":
        return LIGHT_BLUE
    elif effect == "HIGH GRAVITY":
        return DARK_PURPLE
    else:
        return CYAN