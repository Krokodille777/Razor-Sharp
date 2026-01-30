import pygame

from pygame.locals import *
from objects import CircleLog, Knife

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

screen_centerX = screen.get_width() // 2
screen_centerY = screen.get_height() // 2

log = CircleLog((screen_centerX - 200, screen_centerY - 200))
knife = Knife((screen_centerX-25, screen_centerY + 205))


all_sprites = pygame.sprite.Group()
all_sprites.add(log, knife)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0, 0, 0))  # Clear screen with black
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()