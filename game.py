import pygame
from pygame.locals import *
from objects import CircleLog, Knife

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

screen_centerX = screen.get_width() // 2
screen_centerY = screen.get_height() // 2

log = CircleLog((screen_centerX - 175, screen_centerY - 175))
knife = Knife((screen_centerX - 5, screen_centerY + 205), log)

all_sprites = pygame.sprite.Group(log, knife)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            knife.throw()

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
