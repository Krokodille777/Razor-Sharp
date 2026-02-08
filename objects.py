import pygame


class CircleLog(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        radius = 175
        self.original_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, (139, 69, 19), (radius, radius), radius)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.type = "circle_log"
        self.angle = 0
        self.rotation_speed = 4.0

    def update(self):
        from physics import rotate_log

        self.angle = (self.angle + self.rotation_speed) % 360
        rotate_log(self)


class Knife(pygame.sprite.Sprite):
    def __init__(self, pos, log: CircleLog):
        super().__init__()
        self.original_image = pygame.Surface((10, 50), pygame.SRCALPHA)
        self.original_image.fill((192, 192, 192))

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.type = "knife"
        self.log = log

        self.state = "idle"   # idle / flying / stuck
        self.speed = -12      # летим вверх (y уменьшается)

        self.stick_vec = None
        self.stick_log_angle = 0
        self.spawner = None
        self.hit_stuck_knife = False

    def throw(self):
        if self.state == "idle":
            self.state = "flying"

    def update(self):
        from physics import move_knife, update_stuck_knife
        if self.state == "flying":
            move_knife(self, self.log)
        elif self.state == "stuck":
            update_stuck_knife(self, self.log)


