import pygame
from pygame.locals import *
from objects import CircleLog
from spawner import KnifeSpawner

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

screen_centerX = screen.get_width() // 2
screen_centerY = screen.get_height() // 2


log = CircleLog((screen_centerX - 175, screen_centerY - 175))
spawner = KnifeSpawner(screen.get_width(), screen.get_height(), log)
spawner.start_round()

def score_ui(score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def you_win_ui():
    font = pygame.font.SysFont(None, 72)
    text = font.render("You Win!", True, (255, 215, 0))
    rect = text.get_rect(center=(screen_centerX, screen_centerY))
    screen.blit(text, rect)

all_sprites = pygame.sprite.Group(log)
knives = spawner.group

score = 0
running = True

while running:
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
        #When the game starts, information about the number of knives is displayed in the console before throwing the first knife
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if spawner.throw_active():
                    print(f"Knives left to throw: {spawner.remaining}")
                    score += 1
                    score_ui(score)
    log.update()
    knives.update()
    spawner.update()

    if spawner.remaining == -1 and spawner.active is None:
        you_win_ui()
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    screen.fill((0, 0, 0))
    screen.blit(log.image, log.rect)
    knives.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
