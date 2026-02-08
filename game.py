import pygame
from pygame.locals import K_ESCAPE, K_SPACE, KEYDOWN, QUIT
from objects import CircleLog
from rounds import RoundManager


pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Razor-Sharp")
clock = pygame.time.Clock()

hud_font = pygame.font.SysFont(None, 28)
message_font = pygame.font.SysFont(None, 36)

TEXT_WHITE = (240, 240, 240)
TEXT_GREEN = (90, 240, 120)
TEXT_RED = (240, 90, 90)

log = CircleLog((50, 150))
round_manager = RoundManager(400, 600, log)
knife_spawner = round_manager.spawner

score = 0
status_text = "Round 1: press SPACE to throw."
status_color = TEXT_WHITE
game_state = "playing"
running = True

if not round_manager.start_next_round():
    game_state = "victory"
    status_text = "Victory! No rounds configured."
    status_color = TEXT_GREEN
else:
    status_text = (
        f"Round {round_manager.current_round}: hit {round_manager.round_limit} knives."
    )


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE and game_state == "playing":
                knife_spawner.throw_active()

    if game_state == "playing":
        log.update()
        knife_spawner.group.update()
        update_event = knife_spawner.update()

        if update_event == "collision":
            game_state = "defeat"
            status_text = "Defeat: you hit a stuck knife."
            status_color = TEXT_RED
        elif update_event == "stuck":
            round_manager.on_knife_stuck()
            if round_manager.has_round_won():
                gained = round_manager.calculate_round_score()
                score += gained
                if round_manager.start_next_round():
                    status_text = f"Round {round_manager.current_round}: +{gained} score."
                    status_color = TEXT_GREEN
                else:
                    game_state = "victory"
                    status_text = f"Victory! Final score: {score}"
                    status_color = TEXT_GREEN
        elif update_event == "empty" and not round_manager.has_round_won():
            game_state = "defeat"
            status_text = "Defeat: knives ended before target."
            status_color = TEXT_RED

    screen.fill((14, 14, 20))
    screen.blit(log.image, log.rect)
    knife_spawner.group.draw(screen)

    hud_lines = [
        f"Round: {round_manager.current_round}/{round_manager.total_rounds}",
        f"Rotation speed: {log.rotation_speed:.2f}",
        f"Knives in round: {round_manager.round_knives_total}",
        f"Knives left: {max(knife_spawner.remaining, 0)}",
        f"Target hits: {round_manager.round_hits}/{round_manager.round_limit}",
        f"Score: {score}",
    ]

    y = 10
    for line in hud_lines:
        text_surface = hud_font.render(line, True, TEXT_WHITE)
        screen.blit(text_surface, (10, y))
        y += 24

    message_surface = message_font.render(status_text, True, status_color)
    message_rect = message_surface.get_rect(center=(screen.get_width() // 2, 565))
    screen.blit(message_surface, message_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
