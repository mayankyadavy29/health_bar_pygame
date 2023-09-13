import sys

import pygame

pygame.init()

pygame.display.set_caption("Health bar")
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def draw_health_bar(health):
    health_boundary_width, health_boundary_radius = 5, 10
    health_boundary = pygame.Rect(100, 20, 440, 40)
    pygame.draw.rect(screen, "red", health_boundary, health_boundary_width, health_boundary_radius)
    health_bar = pygame.Rect(health_boundary)
    health_bar.width -= health_boundary_width * 2
    health_bar.height -= health_boundary_width * 2
    health_bar.top += health_boundary_width
    health_bar.left += health_boundary_width
    health_bar.width *= (health/100)
    if health > 0:
        pygame.draw.rect(screen, "blue", health_bar, 0, health_boundary_radius // 2)

def main():
    # Background
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, (width, height))

    # Gun image
    gun = pygame.image.load("gun.png")
    gun = pygame.transform.scale(gun, (150, 100))
    gun_rect = gun.get_rect().move((0, 320))

    # Spaceship image
    spaceship = pygame.image.load("spaceship.png")
    spaceship = pygame.transform.rotate(pygame.transform.scale(spaceship, (150, 200)), 90)
    spaceship_rect = spaceship.get_rect().move((480, 280))

    # Bullet image
    bullet_list = list()
    bullet = pygame.image.load("bullet.png")
    bullet = pygame.transform.scale(bullet, (50, 50))

    # Game Over
    gameover = pygame.font.SysFont("comicsans", 60).render("GAME OVER", True, (242, 232, 198))
    gameover_rect = gameover.get_rect().move((150, 200))

    HIT = pygame.USEREVENT + 1
    GAMEOVER = pygame.USEREVENT + 2
    health = 100

    while True:
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if health > 0:
                if event.type == pygame.MOUSEBUTTONUP:
                    bullet_rect = bullet.get_rect().move(gun_rect.right - 30, gun_rect.top + 5)
                    bullet_list.append(bullet_rect)

                if event.type == HIT:
                    health -= 10
                    if health == 0:
                        pygame.event.post(pygame.event.Event(GAMEOVER))

        if health > 0:
            # Draw assets
            draw_health_bar(health)
            screen.blit(gun, gun_rect)
            screen.blit(spaceship, spaceship_rect)

            # Test whether bullet has collided spaceship rect or not
            for b in bullet_list:
                screen.blit(bullet, b)
                b.x += 2
                if spaceship_rect.colliderect(b):
                    bullet_list.remove(b)
                    pygame.event.post(pygame.event.Event(HIT))
        else:
            screen.blit(gameover, gameover_rect)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
