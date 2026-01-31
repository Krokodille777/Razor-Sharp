import pygame
from pygame.locals import *
from objects import CircleLog, Knife
import math
import random




# def spin_log(angle, speed):
#     radians  = math.radians(angle)
#     circleLog.image = pygame.transform.rotate(circleLog.original_image, angle)
#     circleLog.rect = circleLog.image.get_rect(center = circleLog.rect.center)
#     #speed stands for how fast the log spins. No acceleration!
#     angle += speed
#     print(angle)
#     return angle, circleLog.rect