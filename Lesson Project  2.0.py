import pygame
import os
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2 Player Space Game')

red_bullets = []
yellow_bullets = []

movement = False
WalkCount = 0

MOVE = [pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), pygame.image.load(os.path.join(
    'Assets', 'spaceship_red2.png')), pygame.image.load(os.path.join('Assets', 'spaceship_red3.png'))]

SPACESHIP_PARAMETER1, SPACESHIP_PARAMETER2 = 70, 70

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0) 

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128,0,128)

RED_RANGE = [RED, ORANGE, YELLOW]
YELLOW_RANGE = [GREEN, BLUE, PURPLE]

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('timesnewroman', 100)

FPS = 60
VEL = 5
MAX_BULLETS = 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_PARAMETER1, SPACESHIP_PARAMETER2)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png'))

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_PARAMETER1, SPACESHIP_PARAMETER2)), 270)

BACKGROUND = pygame.image.load(os.path.join('Assets', 'SPACE_BACKGROUND.jpg'))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, BULLET_COLOUR_1, BULLET_COLOUR_2):
    global WalkCount

    WINDOW.fill(BLACK)
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        'Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        'Health: ' + str(yellow_health), 1, WHITE)

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    WINDOW.blit(red_health_text,
                (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, BULLET_COLOUR_1, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, BULLET_COLOUR_2, bullet)

    pygame.display.update()


def sprite_movement(keys, yellow, red, VEL):
    if keys[pygame.K_UP] and red.y > 5:
        red.y -= VEL

    if keys[pygame.K_DOWN] and red.y < HEIGHT - SPACESHIP_PARAMETER2 - 10:
        red.y += VEL

    if keys[pygame.K_LEFT] and red.x > BORDER.x + 20:
        red.x -= VEL

    if keys[pygame.K_RIGHT] and red.x < WIDTH - SPACESHIP_PARAMETER1 - 10:
        red.x += VEL

    if keys[pygame.K_w] and yellow.y > 5:
        yellow.y -= VEL

    if keys[pygame.K_s] and yellow.y < HEIGHT - SPACESHIP_PARAMETER2 - 10:
        yellow.y += VEL

    if keys[pygame.K_a] and yellow.x > 10:
        yellow.x -= VEL

    if keys[pygame.K_d] and yellow.x < BORDER.x - SPACESHIP_PARAMETER1 - 10:
        yellow.x += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_health, red_health, BULLET_COLOUR_1, BULLET_COLOUR_2):
    for bullet in yellow_bullets:
        bullet.x += VEL * 2
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet. x > WIDTH:
            yellow_bullets.remove(bullet)

        elif red_health == 1 and red.colliderect(bullet):
            red_health = 0
            pygame.time.delay(100)
            pygame.event.post(pygame.event.Event(RED_HIT))

            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= VEL * 2
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        if bullet.x < 0:
            red_bullets.remove(bullet)

        if yellow_health <= 0:
            for bullet in red_bullets:
                red_bullets.remove(bullet)

            for bullet in yellow_bullets:
                yellow_bullets.remove(bullet)

        if red_health <= 0:
            for bullet in red_bullets:
                red_bullets.remove(bullet)

            for bullet in yellow_bullets:
                yellow_bullets.remove(bullet)


def draw_winner(winner_text):
    winner_message = WINNER_FONT.render(winner_text, 1, WHITE)

    WINDOW.blit(winner_message, (WIDTH // 2 - winner_message.get_width() // 2,
                                 HEIGHT // 2 - winner_message.get_height() // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():

    red = pygame.Rect(WIDTH - 100, 350, SPACESHIP_PARAMETER1,
                      SPACESHIP_PARAMETER2)
    yellow = pygame.Rect(100, 350, SPACESHIP_PARAMETER1, SPACESHIP_PARAMETER2)

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:

        BULLET_COLOUR_1 = random.choice(RED_RANGE)
        BULLET_COLOUR_2 = random.choice(YELLOW_RANGE)

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height // 2),
                                         10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_e and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect((yellow.x + yellow.width,
                                          yellow.y + (yellow.height // 2),
                                          10, 5))
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health == 0:
            winner_text = "YELLOW WINS!"

        if yellow_health == 0:
            winner_text = "RED WINS!"

        if winner_text != "":
            pygame.time.delay(500)
            draw_winner(winner_text)
            for bullet in red_bullets:
                red_bullets.remove(bullet)

            for bullet in yellow_bullets:
                yellow_bullets.remove(bullet)
            break

        keys = pygame.key.get_pressed()
        sprite_movement(keys, yellow, red, VEL)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, BULLET_COLOUR_1, BULLET_COLOUR_2)

        handle_bullets(yellow_bullets, red_bullets, yellow,
                       red, yellow_health, red_health, BULLET_COLOUR_1, BULLET_COLOUR_2)
    
    for bullet in red_bullets:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        yellow_bullets.remove(bullet)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT // 2 - title_label.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()