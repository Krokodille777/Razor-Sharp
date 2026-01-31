import pygame
from pygame.locals import *

class CircleLog(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        radius = 175
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (139, 69, 19), (radius, radius), radius)  # Brown color for the log
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "circle_log"

class Knife(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 30), pygame.SRCALPHA)
        self.image.fill((192, 192, 192))  # Grey color for the knife
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "knife"
