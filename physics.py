import pygame
from pygame.locals import *
from objects import CircleLog, Knife
import math
import random

circlelog = CircleLog((300, 200))

def throw_knife(knife_pos): 
    #To throw the knife we should change its y position until it collides with the log. #Randomly choose how many knives the player has to throw at the log.

    collidesWithLog = False
    log_components = pygame.sprite.Group()
    log_components.add(circlelog)

    while not collidesWithLog and knife_pos.rect.y !=425:
        knife_pos.rect.y += 5  # Move the knife downwards
        collidesWithLog = pygame.sprite.spritecollide(knife_pos, log_components, False, pygame.sprite.collide_mask)
    if collidesWithLog:
        knife_pos.rect.y = 425  # Stop the knife at the collision point  
    return knife_pos


