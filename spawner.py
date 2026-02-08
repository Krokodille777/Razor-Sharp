#This file is responsible for spawning knives, depending on random amount (4 -  13)


import random
from objects import Knife
import pygame


class KnifeSpawner:
    def __init__(self, screen_width, screen_height, log):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.log = log

        self.remaining = random.randint(6, 16)
        self.active = None

        self.group = pygame.sprite.Group()

    def start_round(self):
        self.remaining = random.randint(6, 16)
        self. group.empty()
        self.active = self._spawn_active_knife()
        self.group.add(self.active)

    def _spawn_active_knife(self):

        return Knife((self.screen_width // 2 - 5, self.screen_height - 120), self.log)
    
    def throw_active(self):
        if self.active is None:
            return False

        if self.active.state != "idle":
            return False

        self.active.throw()
        return True

    def update(self):
        if self.active is None:
            return
        
        if getattr(self.active, "state", None) == "stuck":
            
            if not getattr(self.active, "_reported_stuck", False):
                self.active._reported_stuck = True
                self.remaining -= 1
                # By the end of the round, no knives should be left to throw, and the player should see a "You Win!" message. If the player tries to throw a knife when there are no knives left, nothing should happen.
                if self.remaining > -1:
                    self.active = self._spawn_active_knife()
                    self.group.add(self.active)
                else:
                    self.active = None
