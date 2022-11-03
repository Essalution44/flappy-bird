import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'D:\\fluffy bird project\\images\\imgs\\imgs\\flappy_bird\gallery\\sprites/bird.png'
BACKGROUND = 'D:\\fluffy bird project\\images\\imgs\\imgs\\flappy_bird\gallery\\sprites/background.png'
PIPE = 'D:\\fluffy bird project\\images\\imgs\\imgs\\flappy_bird\gallery\\sprites/pipe.png'


def welcome_screen():
    player_x = int(SCREENWIDTH / 5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    message_x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    message_y = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def main_game():
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENWIDTH / 2)
    basex = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(player_x, player_y, upperPipes,
                              lowerPipes)
        if crashTest:
            return

        playerMidPos = player_x + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(playerVelY, GROUNDY - player_y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in my_digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Codehub')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/0.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/1.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/2.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/3.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/4.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/5.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/6.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/7.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/8.png').convert_alpha(),
        pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('D:\\fluffy bird project\\images\imgs\\imgs\\flappy_bird\\gallery\\sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('D:\\fluffy bird project\images\\imgs\\imgs\\flappy_bird\\gallery\\audio\\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('D:\\fluffy bird project\images\\imgs\\imgs\\flappy_bird\\gallery\\audio\\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('D:\\fluffy bird project\images\\imgs\\imgs\\flappy_bird\\gallery\\audio\\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('D:\\fluffy bird project\images\\imgs\\imgs\\flappy_bird\\gallery\\audio\\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('D:\\fluffy bird project\images\\imgs\\imgs\\flappy_bird\\gallery\\audio\\wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_screen()
        main_game()

# Essalution44
