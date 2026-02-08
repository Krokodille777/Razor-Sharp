import random
from spawner import KnifeSpawner


class RoundManager:
    def __init__(self, screen_width, screen_height, log):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.log = log
    

        self.current_round = 0
        self.total_rounds = 3
        self.spawner = KnifeSpawner(screen_width, screen_height, log)
        self.round_hits = 0
        self.round_knives_total = 0
        self.round_limit = 0

    def _set_random_rotation_speed(self):
        self.log.rotation_speed = random.uniform(2, 6)
        self.log.angle = 0

    def _set_round_rules(self):
        knives_to_throw = random.randint(6, 16)
        knives_to_win = random.randint(4, knives_to_throw)
        self.round_knives_total = knives_to_throw
        self.round_limit = knives_to_win
        self.spawner.start_round(knives_to_throw, knives_to_win)

    def start_next_round(self):
        if self.current_round >= self.total_rounds:
            return False

        self.current_round += 1
        self.round_hits = 0
        self._set_random_rotation_speed()
        self._set_round_rules()
        return True

    def on_knife_stuck(self):
        self.round_hits += 1

    def has_round_won(self):
        return self.round_hits >= self.round_limit

    def calculate_round_score(self):
        extra_knives = max(0, self.round_knives_total - self.round_limit)
        multiplier = max(1, extra_knives)
        return self.round_hits * multiplier
