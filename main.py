import pygame as pg
import math
import random
from pygame import mixer

# initialize the pygame
pg.init()
# creating a screen
screen = pg.display.set_mode((800, 600))
# Adding a background image
background = pg.image.load('background.png')
# adding background music
mixer.music.load('background.wav')
mixer.music.play(-1)    #-1 is for looping the music

# TITLE AND ICON
pg.display.set_caption("SPACE WAR")  # title
logo = pg.image.load('ufo.png')  # picture of the logo
pg.display.set_icon(logo)  # setting the logo

# PLAYER
playerimg = pg.image.load('player.png')
player_x = 360
player_y = 500
playerXchange = 0  # for the movement of player
playerYchange = 0

# ENEMYS
enemyimg = []
enemy_x = []
enemy_y = []
enemyXchange = []
enemyYchange = []
enemy_strength = random.randint(5, 8)
for i in range(enemy_strength):
    enemyimg.append(pg.image.load('enemy.png'))
    enemy_x.append(random.randint(0, (800 - 64)))  # respawning it in a random location
    enemy_y.append(random.randint(0, 200))
    enemyXchange.append(4)  # for the movement of the enemy
    enemyYchange.append(40)

# BULLET
bulletimg = pg.image.load('bullet.png')
bullet_x = player_x  # -->must use player_x not bullet_x because bullet will launch from player, no matter where ever it is
bullet_y = player_y
bulletXchange = 0  # because bullete does not changes in x-axis it move only in y-axis
bulletYchange = 6  # controls bullet speed
bullet_state = "ready"


# SCORE
score_val = 0
font = pg.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10


# GAME OVER
gameover_font = pg.font.Font('freesansbold.ttf', 64)
overtext_x = 200
overtext_y = 250


# in Player function we will draw a character
def Player(x, y):
    # "blit" means drawing
    screen.blit(playerimg, (player_x, player_y))


def Enemy(x, y, i):
    screen.blit(enemyimg[i], (enemy_x[i], enemy_y[i]))


def Bullet(x, y):
    global bullet_state  # ********
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def Shoot(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 50: return True


def Score_view(x, y):
    score = font.render('Score : ' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def GameOver(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt(math.pow((playerY - enemyY), 2) + math.pow((playerX - enemyX), 2))
    if distance < 50 or enemyY >= (600 - 64): return True


def GameoverText(x, y):
    over_text = gameover_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (overtext_x, overtext_y))
    coll_sound = mixer.Sound('explosion.wav')
    coll_sound.play()
    mixer.Sound.stop(coll_sound)

# game loop
# if anything is persistent in the game then it must be included in the game loop
running = True
while running:
    # background color change of the game window
    screen.fill((0, 0, 150))  # this line will always be at the top as it is the background.
    screen.blit(background, (0, 0))  # setting bg image
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # ******CONTROLS Of THE PLAYER*********

        if event.type == pg.KEYDOWN:  # IT MAINTAINS THE MOVEMENT
            if event.key == pg.K_RIGHT:
                playerXchange = 5
            if event.key == pg.K_LEFT:
                playerXchange = -5
            if event.key == pg.K_UP:
                playerYchange = -5
            if event.key == pg.K_DOWN:
                playerYchange = 5
            elif event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    # bullet_sound = mixer.Sound('laser.wav')
                    # bullet_sound.play()
                    bullet_x = player_x
                    Bullet(bullet_x, bullet_y)

        if event.type == pg.KEYUP:  # IT HELPS TO PAUSE THE MOVEMENT ACCORDING TO OUR CONTROL
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT or event.key == pg.K_UP or event.key == pg.K_DOWN:
                playerXchange = 0
                playerYchange = 0


    # declaring player in the game
    player_x += playerXchange  # these changes the value and helps player to move
    if player_x < 0:
        player_x = 0
    elif player_x > 800 - 64:  # here (800 -64) because the image is of 64 pixel
        player_x = 800 - 64
    player_y += playerYchange
    if player_y < 0:
        player_y = 0
    elif player_y > 600 - 64:
        player_y = 600 - 64
    Player(player_x, player_y)


    # Customizing enemy movements
    for i in range(enemy_strength):
        enemy_x[i] += enemyXchange[i]

        if enemy_x[i] <= 0:
            enemyXchange[i] = 4
            enemy_y[i] += enemyYchange[i]
        elif enemy_x[i] >= 800 - 64:
            enemyXchange[i] = -4
            enemy_y[i] += enemyYchange[i]

        # Collision of the enemy and the bullet
        if Shoot(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = player_y
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, 800 - 64)
            enemy_y[i] = random.randint(0, 200)
            score_val += 1

        # Collision of enemy and player
        if GameOver(player_x, player_y, enemy_x[i], enemy_y[i]):

            for j in range(enemy_strength):
                enemy_y[j] = 2000
            GameoverText(overtext_x, overtext_y)
            break


        Enemy(enemy_x[i], enemy_y[i], i)


    # Bullet movement
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
    if bullet_state == "fire":
        Bullet(bullet_x, bullet_y)
        bullet_y -= bulletYchange


    # SCORE INCREAMENT:
    Score_view(text_x, text_y)


    # ********This line of code is very important. It updates the game window every time we do a change*********
    pg.display.update()  # this line will be there in every games.
