"""
Gestion des niveaux du jeu.

Ce module charge les niveaux depuis `levels/*.json`.
Chaque fichier contient un nom et des patterns de jeu editables sans toucher au code.
"""
import json
from pathlib import Path
from obstacles import Obstacle
from portals import GravityPortal
from particles import Particle
from settings import OBSTACLE_TYPES, PORTAL_TYPES

DEFAULT_LEVEL_LIBRARY = [
    {
        "name": "Niveau 1 - Decouverte",
        "patterns": [
            {"items": ["spike"], "spacing": 280},
            {"items": ["cube"], "spacing": 260},
            {"items": ["portal_low"], "spacing": 190},
            {"items": ["spike"], "spacing": 260},
            {"items": ["cube"], "spacing": 260},
            {"items": ["mini_spike"], "spacing": 170},
            {"items": ["spike", "mini_spike"], "spacing": 190},
            {"items": ["cube", "spike"], "spacing": 220},
            {"items": ["portal_normal"], "spacing": 190},
            {"items": ["long_spike"], "spacing": 260},
            {"items": ["cube"], "spacing": 220},
            {"items": ["spike"], "spacing": 220},
            {"items": ["portal_high"], "spacing": 180},
            {"items": ["mini_spike", "spike"], "spacing": 190},
            {"items": ["cube"], "spacing": 200},
            {"items": ["long_spike"], "spacing": 260},
        ],
    },
    {
        "name": "Niveau 2 - Cadence",
        "patterns": [
            {"items": ["spike"], "spacing": 220},
            {"items": ["cube"], "spacing": 210},
            {"items": ["mini_spike", "mini_spike"], "spacing": 160},
            {"items": ["portal_low"], "spacing": 170},
            {"items": ["cube", "spike"], "spacing": 170},
            {"items": ["long_spike"], "spacing": 220},
            {"items": ["cube"], "spacing": 180},
            {"items": ["portal_high"], "spacing": 170},
            {"items": ["spike", "mini_spike"], "spacing": 150},
            {"items": ["cube", "spike"], "spacing": 180},
            {"items": ["portal_normal"], "spacing": 170},
            {"items": ["long_spike"], "spacing": 200},
            {"items": ["cube"], "spacing": 180},
            {"items": ["spike", "cube"], "spacing": 150},
            {"items": ["mini_spike"], "spacing": 140},
            {"items": ["portal_low"], "spacing": 150},
            {"items": ["cube", "mini_spike"], "spacing": 150},
            {"items": ["long_spike"], "spacing": 190},
            {"items": ["portal_high"], "spacing": 160},
            {"items": ["spike"], "spacing": 170},
        ],
    },
    {
        "name": "Niveau 3 - Pression",
        "patterns": [
            {"items": ["mini_spike", "spike"], "spacing": 130},
            {"items": ["cube"], "spacing": 140},
            {"items": ["portal_high"], "spacing": 150},
            {"items": ["spike", "mini_spike", "spike"], "spacing": 120},
            {"items": ["cube", "cube"], "spacing": 120},
            {"items": ["portal_low"], "spacing": 140},
            {"items": ["long_spike"], "spacing": 170},
            {"items": ["cube", "spike"], "spacing": 120},
            {"items": ["portal_normal"], "spacing": 130},
            {"items": ["mini_spike", "mini_spike", "spike"], "spacing": 110},
            {"items": ["cube"], "spacing": 130},
            {"items": ["portal_high"], "spacing": 140},
            {"items": ["long_spike"], "spacing": 150},
            {"items": ["spike", "cube", "mini_spike"], "spacing": 110},
            {"items": ["portal_low"], "spacing": 130},
            {"items": ["long_spike"], "spacing": 160},
            {"items": ["cube", "spike"], "spacing": 110},
            {"items": ["portal_normal"], "spacing": 130},
            {"items": ["mini_spike", "spike"], "spacing": 120},
            {"items": ["long_spike"], "spacing": 160},
            {"items": ["cube"], "spacing": 130},
            {"items": ["spike", "spike"], "spacing": 130},
        ],
    },
]


def _normalize_patterns(raw_patterns):
    patterns = []
    for entry in raw_patterns:
        if isinstance(entry, dict):
            items = entry.get("items", [])
            spacing = entry.get("spacing", 200)
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            items, spacing = entry
        else:
            continue

        if not isinstance(items, list):
            continue
        try:
            spacing = int(spacing)
        except (TypeError, ValueError):
            spacing = 200

        clean_items = []
        for item in items:
            if not isinstance(item, str):
                continue
            if item.startswith("portal_"):
                portal_key = item.replace("portal_", "")
                if portal_key in PORTAL_TYPES:
                    clean_items.append(item)
            elif item in OBSTACLE_TYPES:
                clean_items.append(item)
        if clean_items:
            patterns.append({"items": clean_items, "spacing": max(0, spacing)})
    return patterns


def _load_level_file(path_obj):
    with path_obj.open("r", encoding="utf-8") as f:
        data = json.load(f)
    patterns = _normalize_patterns(data.get("patterns", []))
    if not patterns:
        return None
    return {
        "name": str(data.get("name") or path_obj.stem),
        "patterns": patterns,
    }


def _load_text_level_file(path_obj):
    lines = path_obj.read_text(encoding="utf-8").splitlines()
    name = path_obj.stem
    raw_patterns = []

    for line in lines:
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        if clean.lower().startswith("name:"):
            name = clean.split(":", 1)[1].strip() or name
            continue

        # Format: item1,item2|spacing
        # Exemple: spike,mini_spike|180
        if "|" in clean:
            left, right = clean.split("|", 1)
            spacing = right.strip()
        else:
            left = clean
            spacing = "200"

        items = [item.strip() for item in left.split(",") if item.strip()]
        raw_patterns.append({"items": items, "spacing": spacing})

    patterns = _normalize_patterns(raw_patterns)
    if not patterns:
        return None
    return {"name": name, "patterns": patterns}


def load_levels():
    base_dir = Path(__file__).resolve().parent
    levels_dir = base_dir / "levels"
    loaded = []

    if levels_dir.exists():
        level_files = list(levels_dir.glob("*.json")) + list(levels_dir.glob("*.txt"))
        for level_path in sorted(level_files):
            try:
                if level_path.suffix.lower() == ".txt":
                    level_data = _load_text_level_file(level_path)
                else:
                    level_data = _load_level_file(level_path)
                if level_data:
                    loaded.append(level_data)
            except (OSError, json.JSONDecodeError):
                continue

    if loaded:
        return loaded
    return DEFAULT_LEVEL_LIBRARY


LEVEL_LIBRARY = load_levels()


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

    @staticmethod
    def get_name(level_index):
        safe_index = max(0, min(level_index, len(LEVEL_LIBRARY) - 1))
        return LEVEL_LIBRARY[safe_index]["name"]

    def generate_level(self):
        x_position = 1200
        patterns = LEVEL_LIBRARY[self.level_index]["patterns"]

        for entry in patterns:
            obstacle_types = entry["items"]
            spacing = entry["spacing"]
            for i, obstacle_type in enumerate(obstacle_types):
                if obstacle_type.startswith("portal_"):
                    portal_key = obstacle_type.replace("portal_", "")
                    if portal_key in PORTAL_TYPES:
                        self.portals.append(GravityPortal(x_position, portal_key))
                        x_position += 50
                else:
                    if obstacle_type in OBSTACLE_TYPES:
                        self.obstacles.append(Obstacle(x_position, obstacle_type))
                        if i < len(obstacle_types) - 1:
                            x_position += 70
            x_position += spacing

    def update(self, game_speed):
        for obstacle in self.obstacles:
            obstacle.update(game_speed)
        self.obstacles = [obs for obs in self.obstacles if obs.x > -100]

        for portal in self.portals:
            portal.update(game_speed)
        self.portals = [p for p in self.portals if p.x > -100]

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

    def create_dust_particles(self, x, y, color=None, intensity=1.0):
        count = max(2, int(5 * max(0.5, intensity)))
        for _ in range(count):
            self.particles.append(
                Particle(x, y, color=color, kind="dust", intensity=intensity)
            )

    def create_portal_particles(self, x, y, color=None, intensity=1.0):
        count = max(8, int(12 * max(0.5, intensity)))
        for _ in range(count):
            self.particles.append(
                Particle(x, y, color=color, kind="portal", intensity=intensity)
            )
