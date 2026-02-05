import pygame
from pygame.locals import *
from objects import CircleLog, Knife
from spawner import KnifeSpawner

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

screen_centerX = screen.get_width() // 2
screen_centerY = screen.get_height() // 2


log = CircleLog((screen_centerX - 175, screen_centerY - 175))
spawner = KnifeSpawner(screen.get_width(), screen.get_height(), log)
spawner.star_round()

knife = Knife((screen_centerX - 5, screen_centerY + 205), log)

all_sprites = pygame.sprite.Group(log)
knives = spawner.group

running = True
while running:
   
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        #When the game starts, information about the number of knives is displayed in the console before throwing the first knife
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                    print(f"Knives left to throw: {spawner.remaining}")
                    spawner.throw_active()
    log.update()
    knives.update()
    spawner.update()

    screen.fill((0, 0, 0))
    screen.blit(log.image, log.rect)
    knives.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
