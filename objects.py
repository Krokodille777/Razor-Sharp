import pygame
from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
LOG_SPRITE_PATHS = (
    ASSETS_DIR / "log.png",
    ASSETS_DIR / "Log.png",
    ASSETS_DIR / "LOG.png",
)
KNIFE_SPRITE_PATHS = (
    ASSETS_DIR / "knife.png",
    ASSETS_DIR / "Knife.png",
    ASSETS_DIR / "KNIFE.png",
)

# Set to None to use the image's native size.
LOG_SIZE = (350, 350)
KNIFE_SIZE = (30, 80)


def _load_sprite(path: Path, size):
    if not path.exists():
        return None

    image = pygame.image.load(str(path)).convert_alpha()
    if size is not None and image.get_size() != size:
        image = pygame.transform.smoothscale(image, size)
    return image


def _load_first_sprite(paths, size):
    for path in paths:
        image = _load_sprite(path, size)
        if image is not None:
            return image
    return None


class CircleLog(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        fallback_radius = 175
        fallback = pygame.Surface(
            (fallback_radius * 2, fallback_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            fallback,
            (139, 69, 19),
            (fallback_radius, fallback_radius),
            fallback_radius,
        )

        self.original_image = _load_first_sprite(LOG_SPRITE_PATHS, LOG_SIZE) or fallback

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image, 1)

        self.type = "circle_log"
        self.angle = 0
        self.rotation_speed = 4.0

    def update(self):
        from physics import rotate_log

        self.angle = (self.angle + self.rotation_speed) % 360
        rotate_log(self)


class Knife(pygame.sprite.Sprite):
    def __init__(self, pos, log: CircleLog, *, anchor="topleft"):
        super().__init__()
        fallback = pygame.Surface((10, 50), pygame.SRCALPHA)
        fallback.fill((192, 192, 192))

        self.original_image = (
            _load_first_sprite(KNIFE_SPRITE_PATHS, KNIFE_SIZE) or fallback
        )

        self.image = self.original_image.copy()
        rect = self.image.get_rect()
        if anchor == "midbottom":
            rect.midbottom = pos
        else:
            rect.topleft = pos
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image, 1)

        self.type = "knife"
        self.log = log

        self.state = "idle"  # idle / flying / stuck / crashed
        self.speed = -12  # летим вверх (y уменьшается)

        self.stick_vec = None
        self.stick_log_angle = 0
        self.spawner = None
        self.hit_stuck_knife = False

        self.tip_local = self._calculate_tip_local()

    def _calculate_tip_local(self):
        original_rect = self.original_image.get_rect()
        bounds = self.original_image.get_bounding_rect()
        tip = pygame.math.Vector2(bounds.midtop)
        return tip - pygame.math.Vector2(original_rect.center)

    def tip_world(self, image_angle_degrees=0):
        return (
            pygame.math.Vector2(self.rect.center)
            + self.tip_local.rotate(image_angle_degrees)
        )

    def throw(self):
        if self.state == "idle":
            self.state = "flying"

    def update(self):
        from physics import move_knife, update_stuck_knife

        if self.state == "flying":
            move_knife(self, self.log)
        elif self.state == "stuck":
            update_stuck_knife(self, self.log)

