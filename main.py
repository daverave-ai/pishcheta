import random
import math

import pygame
from pygame import mixer

#inicializirane na pygame <3
pygame.init()

# suzdavane na ekranche za igrata
screen = pygame.display.set_mode((800, 600))

#kartinka na background
background = pygame.image.load('8905.jpg')

#zvuk
mixer.music.load('background.wav')
mixer.music.play(-1)

# ime i ikonka na ekran

pygame.display.set_caption("ptichki i pchelichki")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# igracha

playerImg = pygame.image.load('fighter.png')
playerX = 370
playerY = 480
playerX_change = 0

# zloto

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# kurshuma

bulletImg = pygame.image.load('sperm.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

#rekordite
score_value = 0
font = pygame.font.Font('doubleplus.otf', 32)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font('error.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("U R DA FATHER", True, (255, 255, 255))
    screen.blit(over_text, (200, 400))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# loop za igrata
running = True
while running:

    screen.fill((255, 0, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # murdane
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -4
            if event.key == pygame.K_d:
                playerX_change = +4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('istrel.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change

    # granici na ekrana
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('die_sound.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[1], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()