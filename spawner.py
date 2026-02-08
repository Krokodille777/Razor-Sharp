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
        self.limit = 0
        self.active = None

        self.group = pygame.sprite.Group()

    def start_round(self, knives_to_throw=None, knives_to_win=None):
        if knives_to_throw is None:
            knives_to_throw = random.randint(6, 16)

        if knives_to_win is None:
            knives_to_win = random.randint(3, knives_to_throw)

        self.remaining = knives_to_throw
        self.limit = min(knives_to_win, knives_to_throw)
        self.group.empty()
        self.active = self._spawn_active_knife()
        self.group.add(self.active)

    def _spawn_active_knife(self):
        knife = Knife((self.screen_width // 2 - 5, self.screen_height - 120), self.log)
        knife.spawner = self
        return knife
    
    def throw_active(self):
        if self.active is None:
            return False

        if self.active.state != "idle":
            return False

        self.active.throw()
        return True

    def update(self):
        if self.active is None:
            return None

        if getattr(self.active, "state", None) == "crashed":
            return "collision"
        
        if getattr(self.active, "state", None) == "stuck":
            
            if not getattr(self.active, "_reported_stuck", False):
                self.active._reported_stuck = True
                self.remaining -= 1
                if self.remaining > 0:
                    self.active = self._spawn_active_knife()
                    self.group.add(self.active)
                    return "stuck"
                else:
                    self.active = None
                    return "empty"

        return None
