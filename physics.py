import pygame




def rotate_log(log):
    center = log.rect.center
    log.image = pygame.transform.rotate(log.original_image, log.angle)
    log.rect = log.image.get_rect(center=center)
    log.mask = pygame.mask.from_surface(log.image)


def move_knife(knife, log):
    # двигаем нож каждый кадр (никаких while!)
    knife.rect.y += knife.speed

    # если улетел вверх — можно сбросить (или считать промахом)
    if knife.rect.bottom < 0:
        knife.state = "idle"
        return

    if knife.spawner is not None and knife_collides_with_stuck_knives(knife, knife.spawner):
        knife.hit_stuck_knife = True
        knife.state = "crashed"
        return

    if pygame.sprite.collide_mask(knife, log):
        # откатим шаг назад, чтобы не "залипнуть" глубоко
        knife.rect.y -= knife.speed
        stick_knife(knife, log)


def stick_knife(knife, log):
    knife.state = "stuck"
    knife.stick_vec = pygame.math.Vector2(knife.rect.center) - log.rect.center
    knife.stick_log_angle = log.angle


def knife_collides_with_stuck_knives(knife, spawner):
    for other in spawner.group:
        if other.state == "stuck" and pygame.sprite.collide_mask(knife, other):
            return True
    return False

def update_stuck_knife(knife, log):
    # насколько провернулось бревно с момента "втыкания"
    delta = log.angle - knife.stick_log_angle

    rotated = knife.stick_vec.rotate(-delta)  # если будет крутиться "не туда" — уберите минус
    knife.rect.center = (log.rect.centerx + rotated.x, log.rect.centery + rotated.y)

    # поворачиваем нож только на дельту с момента "втыкания",
    # чтобы при попадании он не делал мгновенный "лишний" наклон
    knife.image = pygame.transform.rotate(knife.original_image, -delta)
    knife.rect = knife.image.get_rect(center=knife.rect.center)
    knife.mask = pygame.mask.from_surface(knife.image)
