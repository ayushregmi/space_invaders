import random
import math
import os

try:
    import pygame
    from pygame import mixer
except:
    os.system("pip install pygame")
    # os.system("cmd /k pip install pygame")
    import pygame
    from pygame import mixer


# Initialization of pygame
pygame.init()
mixer.init()

mixer.music.load("space_invaders/boom.mp3")

# Setting the screen
screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space_invaders/icon.png")
pygame.display.set_icon(icon)

# Player
player1 = pygame.image.load("space_invaders/player.png")
player2 = pygame.image.load("space_invaders/player1.png")
playerImg = random.choice([player1, player2])
playerX = 378
playerY = 500
player_speed = 0


# Enemy
enemy_0 = pygame.image.load("space_invaders/ufo.png")
enemy_1 = pygame.image.load("space_invaders/ufo1.png")
enemy_2 = pygame.image.load("space_invaders/ufo2.png")
enemies_num = 5
enemy_list = [enemy_0, enemy_1, enemy_2]
enemyY_list = [0, 32*2, 32*2*2]

# Background
back_ground_1 = pygame.image.load("space_invaders/Background.jpg")
back_ground_2 = pygame.image.load("space_invaders/Background1.jpg")
back_ground = random.choice([back_ground_1, back_ground_2])


# Enemy List

enemyImg = []
enemyX = []
enemyY = []
enemy_speed = []

# Creating Multiples enemies
for i in range(enemies_num):
    enemyImg.append(random.choice(enemy_list))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.choice(enemyY_list))
    enemy_speed.append(random.choice([-0.3, 0.3]))

# Bullet

bulletImg = pygame.image.load("space_invaders/bullet1.png")
bulletY = playerY
bulletX = playerX + 16
bullet_speed = 2
bullet_state = "ready"

# Explosion

expImg = pygame.image.load("space_invaders/explosion.png")
exp_X = 0
exp_y = 0

# Score board
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_X = 10
text_Y = 610

# High score board

# Importing High score
file = open("space_invaders/score.txt", "r")
high_score = 0
for score in file:
    if int(score) > high_score:
        high_score = int(score)
file.close()
high_score_font = pygame.font.Font("freesansbold.ttf", 32)
high_score_X = 500
high_score_Y = 610

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 50)
game_over = False

#Fucntions
def explosion(x, y):
    screen.blit(expImg, (x, y))


def show_high_score(a, y):
    high_score_display = high_score_font.render("High Score : " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_display, (a, y))


def show_score(a, y):
    score_display = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score_display, (a, y))


def player(a, y):
    screen.blit(playerImg, (a, y))


def enemy(b, y, a):
    screen.blit(enemyImg[a], (b, y))


def fire_bullet(a, y):
    global bullet_state
    screen.blit(bulletImg, (a+16, y))
    bullet_state = "fire"


def is_collision(x1, y1, x2, y2):
    return math.sqrt((pow(x2 - x1, 2) + pow(y2 - y1, 2)))


def game_over_function():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 270))


def info():
    info_text = info_font.render(inform, True, (255, 255, 255))
    screen.blit(info_text, (55, 10))


info_font = pygame.font.Font("freesansbold.ttf", 25)
inform = "USE THE ARROW KEYS TO MOVE AND SPACE TO FIRE"
n = 1
num = 1
t = 0
e = 200
if back_ground == back_ground_1:
    color = (104, 0, 52)
elif back_ground == back_ground_2:
    color = (9, 0, 43)

# Main game loop
run = True
down = 0
inc = 0
while run:
    t += inc
    if score_value == n * e:
        enemyImg.append(random.choice(enemy_list))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.choice(enemyY_list))
        enemy_speed.append(random.choice([-0.3, 0.3]))
        enemies_num += 1
        t = num * 300
        n += 1
        e -= 5
        if e <= 70:
            e = 70

    if t == num*300:
        num += 1
    if num >= len(enemyImg):
        num = len(enemyImg)

    if len(enemyImg) >= 10:
        num = 10

    # Color (R, B, G)

    if back_ground == back_ground_1:
        screen.fill((104, 0, 52))
    elif back_ground == back_ground_2:
        screen.fill((9, 0, 43))

    screen.blit(back_ground, (0, 0))
    show_high_score(high_score_X, high_score_Y)
    show_score(text_X, text_Y)
    # Keyboard Binding
    for event in pygame.event.get():

        # Quit
        if event.type == pygame.QUIT:
            run = False
        # Functions Of Player
        if event.type == pygame.KEYDOWN:
            inform = ""
            down  = 64
            inc = 1
            # Moving Left
            if event.key == pygame.K_LEFT:
                player_speed = -2

            # Moving Right
            if event.key == pygame.K_RIGHT:
                player_speed = 2

            # Fire
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed = 0

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_speed

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY

    # Player Movement

    playerX += player_speed

    if playerX >= 736:
        playerX = 736
    if playerX < 0:
        playerX = 1
    player(playerX, playerY)

    # Enemy Movement
    for i in range(num):
        enemyX[i] += enemy_speed[i]
        if enemyX[i] >= 736 or enemyX[i] < 0:
            enemy_speed[i] *= -1
            enemyY[i] += down
        enemy(enemyX[i], enemyY[i], i)

        # Collision between Bullet and Enemy
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY) <= 32:
            explosion(enemyX[i], enemyY[i])
            # mixer.music.play()
            bullet_state = "ready"
            score_value += 10
            bulletX = playerX
            bulletY = playerY
            screen.blit(expImg, (enemyX[i], enemyY[i]))
            enemyImg[i] = random.choice(enemy_list)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.choice(enemyY_list)
            # enemy_speed[i] = random.choice([-2, 2])
            for j in range(num):
                if is_collision(enemyX[i], enemyY[i], enemyX[j], enemyY[j]) <= 64:
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.choice(enemyY_list)
                    # enemy_speed[i] = random.choice([-0.5, 0.5])
            if enemy_speed[i] > 0:
                enemy_speed[i] += 0.01
            if enemy_speed[i] < 0:
                enemy_speed[i] -= 0.01

        # Collision between Enemy and Player
        if is_collision(enemyX[i], enemyY[i], playerX, playerY) <= 64:
            screen.blit(expImg, (playerX, playerY))
            for j in range(num):
                enemyY[j] = -2000
                enemyY[j] = -2000
            game_over = True
            playerY = 2000
            playerX = 2000
            bulletY = 2000
            bullet_state = "not ready"
            file = open("space_invaders/score.txt", "a+")
            file.write(str(score_value)+"\n")
            file.close()
            enemyImg.clear()
            break
    info()
    if game_over:
        game_over_function()
    pygame.display.update()
