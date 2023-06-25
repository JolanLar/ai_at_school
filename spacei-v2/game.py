import time

import pygame
import random
import math
from pygame import mixer
from openCamer import Cap

# initializing pygame
pygame.init()

# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Welcome to Space Invaders Game by:- styles")

# Score
score_val = 0
score2_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Points - J1 : " + str(score_val) + " - J2 : " + str(score2_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


# Background Sound
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# player
playerImage = pygame.image.load('data/spaceship.png')
player_X = 390
player_Y = 523
player_Xchange = 0

# player 2
player2Image = pygame.image.load('data/ufo.png')
player2_X = 340
player2_Y = 523
player2_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8
for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('data/alien.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"

# Bullet 2
# rest - bullet is not moving
# fire - bullet is moving
bullet2Image = pygame.image.load('data/bullet.png')
bullet2_X = 0
bullet2_Y = 500
bullet2_Xchange = 0
bullet2_Ychange = 3
bullet2_state = "rest"


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def player2(x, y):
    screen.blit(player2Image, (x - 16, y + 10))


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


def bullet2(x, y):
    global bullet2_state
    screen.blit(bulletImage, (x, y))
    bullet2_state = "fire"


# game loop

cap = Cap()

counter = 0
threshold = 10

running = True
while running:

    if counter == threshold:
        counter = 0
    if counter == 0:
        predictions = cap.predict()

        # Player 1 cam
        if predictions['p1']['fire'] == 0:
            if bullet_state is "rest":
                bullet_X = player_X
                bullet(bullet_X, bullet_Y)

        if predictions['p1']['move'] == 0:
            player_Xchange = -1.7
        elif predictions['p1']['move'] == 1:
            player_Xchange = 1.7
        else:
            player_Xchange = 0

        # Player 2 cam
        if predictions['p2']['fire'] == 0:
            if bullet2_state is "rest":
                bullet2_X = player2_X
                bullet2(bullet2_X, bullet2_Y)

        if predictions['p2']['move'] == 0:
            player2_Xchange = -1.7
        elif predictions['p2']['move'] == 1:
            player2_Xchange = 1.7
        else:
            player2_Xchange = 0
    counter += 1

    # RGB
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controling the player movement from the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange -= 1.7
            if event.key == pygame.K_RIGHT:
                player_Xchange += 1.7
            if event.key == pygame.K_KP_ENTER:
                # Fixing the change of direction of bullet
                if bullet_state is "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('data/bullet.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_Xchange += 1.7
            elif event.key == pygame.K_RIGHT:
                player_Xchange -= 1.7

        # Controling the player movement from the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player2_Xchange -= 1.7
            if event.key == pygame.K_d:
                player2_Xchange += 1.7
            if event.key == pygame.K_SPACE:
                # Fixing the change of direction of bullet
                if bullet_state is "rest":
                    bullet2_X = player2_X
                    bullet2(bullet2_X, bullet2_Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                player2_Xchange += 1.7
            elif event.key == pygame.K_d:
                player2_Xchange -= 1.7

    # adding the change in the player position
    player_X += player_Xchange
    player2_X += player2_Xchange

    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # bullet 2 movement
    if bullet2_Y <= 0:
        bullet2_Y = 600
        bullet2_state = "rest"
    if bullet2_state is "fire":
        bullet2(bullet2_X, bullet2_Y)
        bullet2_Y -= bullet2_Ychange

    # movement of the invader
    for i in range(no_of_invaders):

        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('data/explosion.wav')
                    explosion_sound.play()
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]
        # Collision
        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
        collision2 = isCollision(bullet2_X, invader_X[i], bullet2_Y, invader_Y[i])
        if collision2:
            score2_val += 1
            bullet2_Y = 600
            bullet2_state = "rest"
        if collision or collision2:
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    # restricting the spaceship so that it doesn't go out of screen
    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750
    if player2_X <= 16:
        player2_X = 16
    elif player2_X >= 750:
        player2_X = 750

    player(player_X, player_Y)
    player2(player2_X, player2_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()
