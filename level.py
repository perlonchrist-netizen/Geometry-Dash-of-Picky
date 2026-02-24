"""
Gestion des niveaux du jeu.

Ce module contient:
- la bibliotheque de patterns (`LEVEL_LIBRARY`) pour chaque niveau,
- la classe `Level` qui instancie obstacles et portails,
- la mise a jour des objets en defilement,
- la gestion des particules liees au niveau.
"""
from obstacles import Obstacle
from portals import GravityPortal
from particles import Particle

LEVEL_LIBRARY = [
    [
        (["spike"], 280),
        (["cube"], 260),
        (["portal_low"], 190),
        (["spike"], 260),
        (["cube"], 260),
        (["mini_spike"], 170),
        (["spike", "mini_spike"], 190),
        (["cube", "spike"], 220),
        (["portal_normal"], 190),
        (["long_spike"], 260),
        (["cube"], 220),
        (["spike"], 220),
        (["portal_high"], 180),
        (["mini_spike", "spike"], 190),
        (["cube"], 200),
        (["long_spike"], 260),
    ],
    [
        (["spike"], 220),
        (["cube"], 210),
        (["mini_spike", "mini_spike"], 160),
        (["portal_low"], 170),
        (["cube", "spike"], 170),
        (["long_spike"], 220),
        (["cube"], 180),
        (["portal_high"], 170),
        (["spike", "mini_spike"], 150),
        (["cube", "spike"], 180),
        (["portal_normal"], 170),
        (["long_spike"], 200),
        (["cube"], 180),
        (["spike", "cube"], 150),
        (["mini_spike"], 140),
        (["portal_low"], 150),
        (["cube", "mini_spike"], 150),
        (["long_spike"], 190),
        (["portal_high"], 160),
        (["spike"], 170),
    ],
    [
        (["mini_spike", "spike"], 130),
        (["cube"], 140),
        (["portal_high"], 150),
        (["spike", "mini_spike", "spike"], 120),
        (["cube", "cube"], 120),
        (["portal_low"], 140),
        (["long_spike"], 170),
        (["cube", "spike"], 120),
        (["portal_normal"], 130),
        (["mini_spike", "mini_spike", "spike"], 110),
        (["cube"], 130),
        (["portal_high"], 140),
        (["long_spike"], 150),
        (["spike", "cube", "mini_spike"], 110),
        (["portal_low"], 130),
        (["long_spike"], 160),
        (["cube", "spike"], 110),
        (["portal_normal"], 130),
        (["mini_spike", "spike"], 120),
        (["long_spike"], 160),
        (["cube"], 130),
        (["spike", "spike"], 130),
    ],
]


class Level:
    def __init__(self, level_index=0):
        self.level_index = max(0, min(level_index, len(LEVEL_LIBRARY) - 1))
        self.obstacles = []
        self.portals = []
        self.particles = []
        self.generate_level()

    @staticmethod
    def count():
        return len(LEVEL_LIBRARY)

    def generate_level(self):
        x_position = 1200
        patterns = LEVEL_LIBRARY[self.level_index]

        for obstacle_types, spacing in patterns:
            for i, obstacle_type in enumerate(obstacle_types):
                if obstacle_type.startswith("portal_"):
                    portal_key = obstacle_type.replace("portal_", "")
                    self.portals.append(GravityPortal(x_position, portal_key))
                    x_position += 50
                else:
                    self.obstacles.append(Obstacle(x_position, obstacle_type))
                    if i < len(obstacle_types) - 1:
                        x_position += 70
            x_position += spacing

    def update(self, game_speed):
        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update(game_speed)
        self.obstacles = [obs for obs in self.obstacles if obs.x > -100]

        # Update portals
        for portal in self.portals:
            portal.update(game_speed)
        self.portals = [p for p in self.portals if p.x > -100]

        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

        return not self.obstacles and not self.portals

    def draw(self, surface, ground_y):
        for portal in self.portals:
            portal.draw(surface, ground_y)
        for obstacle in self.obstacles:
            obstacle.draw(surface, ground_y)
        for particle in self.particles:
            particle.draw(surface)

    def create_dust_particles(self, x, y):
        for _ in range(8):
            self.particles.append(Particle(x, y))

    def create_portal_particles(self, x, y):
        for _ in range(15):
            self.particles.append(Particle(x, y))