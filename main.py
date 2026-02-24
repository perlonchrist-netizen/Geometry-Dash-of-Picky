"""
Projet: Geometry Dash (version Pygame 2D).

Resume du projet:
- Jeu de plateforme type runner avec saut, collisions et gravite dynamique.
- Le joueur controle un cube qui avance dans des niveaux a obstacles.
- Les portails changent la gravite (low/high/normal) et adaptent le saut.
- Une interface d'accueil permet de choisir un niveau avant de jouer.
- Le jeu gere les etats principaux: menu, partie, game over, fin de niveau,
  et fin de campagne.

Architecture:
- `settings.py`: constantes et configuration globale.
- `player.py`: logique du joueur (mouvement, saut, rotation, etat au sol).
- `level.py`: generation et cycle de niveaux.
- `obstacles.py`/`portals.py`: objets interactifs du decor.
- `particles.py`: effets visuels (poussiere, portail).
- `utils.py`: fonctions utilitaires de rendu et de gameplay.
"""
import pygame
import sys
from settings import *
from player import Player
from level import Level
from utils import draw_floor, update_gravity_and_jump, get_gravity_color

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_LEVEL_COMPLETE = "LEVEL_COMPLETE"
STATE_CAMPAIGN_COMPLETE = "CAMPAIGN_COMPLETE"

selected_level = 0
current_level_index = selected_level
total_levels = Level.count()
game_state = STATE_MENU

gravity = BASE_GRAVITY
jump_power = BASE_JUMP_POWER
current_gravity_effect = "NORMAL"
score = 0
dust_timer = 0

player = Player()
level = Level(current_level_index)


def start_level(level_index):
    global player
    global level
    global current_level_index
    global gravity
    global jump_power
    global current_gravity_effect
    global score
    global dust_timer
    global game_state

    current_level_index = level_index
    gravity = BASE_GRAVITY
    jump_power = BASE_JUMP_POWER
    current_gravity_effect = "NORMAL"
    score = 0
    dust_timer = 0
    player = Player()
    level = Level(current_level_index)
    game_state = STATE_PLAYING


def draw_menu():
    title = big_font.render("GEOMETRY DASH", True, CYAN)
    subtitle = font.render("Selection du niveau", True, WHITE)
    level_text = big_font.render(
        f"Niveau {selected_level + 1}/{total_levels}",
        True,
        GREEN,
    )
    hint_1 = font.render("Gauche/Droite : changer de niveau", True, WHITE)
    hint_2 = font.render("Entree/Espace : lancer", True, WHITE)
    hint_3 = font.render("ECHAP : quitter", True, WHITE)

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    hint_1_rect = hint_1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    hint_2_rect = hint_2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    hint_3_rect = hint_3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))

    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    screen.blit(level_text, level_rect)
    screen.blit(hint_1, hint_1_rect)
    screen.blit(hint_2, hint_2_rect)
    screen.blit(hint_3, hint_3_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == STATE_MENU:
                if event.key == pygame.K_LEFT:
                    selected_level = (selected_level - 1) % total_levels
                elif event.key == pygame.K_RIGHT:
                    selected_level = (selected_level + 1) % total_levels
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    start_level(selected_level)

            elif game_state == STATE_PLAYING:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    player.jump(jump_power)
                elif event.key == pygame.K_r:
                    start_level(current_level_index)

            elif game_state == STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    start_level(current_level_index)
                elif event.key == pygame.K_RETURN:
                    game_state = STATE_MENU

            elif game_state == STATE_LEVEL_COMPLETE:
                if event.key == pygame.K_r:
                    start_level(current_level_index)
                elif event.key in (pygame.K_RETURN, pygame.K_n):
                    if current_level_index < total_levels - 1:
                        selected_level = current_level_index + 1
                        start_level(selected_level)
                    else:
                        game_state = STATE_CAMPAIGN_COMPLETE

            elif game_state == STATE_CAMPAIGN_COMPLETE:
                if event.key == pygame.K_r:
                    selected_level = 0
                    start_level(selected_level)
                elif event.key == pygame.K_RETURN:
                    game_state = STATE_MENU

    if game_state == STATE_PLAYING:
        score += 1

        player.update(gravity, level.obstacles)
        if player.is_on_ground(level.obstacles) and abs(player.velocity_y) < 0.1:
            dust_timer += 1
            if dust_timer >= 6:
                level.create_dust_particles(player.x + player.size // 2, player.y + player.size)
                dust_timer = 0
        else:
            dust_timer = 0

        if level.update(GAME_SPEED):
            game_state = STATE_LEVEL_COMPLETE

        player_hitbox = player.get_hitbox()
        for obstacle in level.obstacles:
            obs_hitbox = obstacle.get_hitbox(GROUND_Y)
            if player_hitbox.colliderect(obs_hitbox):
                if obstacle.type == "cube":
                    if player.y + player.size > obs_hitbox.top + 5:
                        game_state = STATE_GAME_OVER
                else:
                    game_state = STATE_GAME_OVER

        for portal in level.portals:
            if player_hitbox.colliderect(portal.get_hitbox(GROUND_Y)) and not portal.activated:
                gravity, jump_power, current_gravity_effect = update_gravity_and_jump(
                    portal.gravity_multiplier,
                    BASE_GRAVITY,
                    BASE_JUMP_POWER,
                )
                portal.apply_effect()
                level.create_portal_particles(
                    portal.x + portal.width // 2,
                    GROUND_Y - portal.height // 2 - 20,
                )

    screen.fill(BG_COLOR)
    draw_floor(screen)

    if game_state == STATE_MENU:
        draw_menu()
    else:
        level.draw(screen, GROUND_Y)
        gravity_color = get_gravity_color(current_gravity_effect)
        player.draw(screen, gravity_color)

        score_text = font.render(f"Score: {score}", True, CYAN)
        level_text = font.render(
            f"Niveau: {current_level_index + 1}/{total_levels}",
            True,
            CYAN,
        )
        jumps_text = font.render(
            f"Sauts: {player.jumps_remaining}/{player.max_jumps}",
            True,
            CYAN,
        )
        gravity_text = font.render(f"Gravite: {current_gravity_effect}", True, CYAN)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(jumps_text, (10, 70))
        screen.blit(gravity_text, (10, 100))

        if game_state == STATE_GAME_OVER:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            game_over_text = big_font.render("GAME OVER", True, RED)
            restart_text = font.render("R: recommencer | Entree: menu", True, WHITE)

            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

            screen.blit(game_over_text, text_rect)
            screen.blit(restart_text, restart_rect)

        elif game_state == STATE_LEVEL_COMPLETE:
            complete_text = big_font.render("NIVEAU COMPLETE!", True, GREEN)
            score_text_end = font.render(f"Score final: {score}", True, WHITE)
            next_hint = font.render("Entree/N: niveau suivant | R: rejouer", True, WHITE)

            text_rect = complete_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            score_rect = score_text_end.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            next_rect = next_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

            screen.blit(complete_text, text_rect)
            screen.blit(score_text_end, score_rect)
            screen.blit(next_hint, next_rect)

        elif game_state == STATE_CAMPAIGN_COMPLETE:
            complete_all = big_font.render("CAMPAGNE TERMINEE!", True, GREEN)
            end_hint = font.render("R: recommencer | Entree: menu", True, WHITE)

            complete_rect = complete_all.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            hint_rect = end_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

            screen.blit(complete_all, complete_rect)
            screen.blit(end_hint, hint_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()