import pygame
from pygame.locals import *
import sys 
from random import randint 

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
FPS = 30
GAME_IMAGES = {}
GAME_SOUNDS = {}


def welcomeScreen():
    while True:
        screen.blit(GAME_IMAGES["background"], (0,0))
        screen.blit(GAME_IMAGES["bird"], (playerX,playerY))
        screen.blit(GAME_IMAGES["message"], (messageX,messageY))
        pygame.display.update()
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if x.type == KEYDOWN and x.key == K_SPACE:
                return
                
def gameLoop():
    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()
    newPipe3 = getRandomPipes()

    upperPipes = [ 
        {"x": SCREEN_WIDTH, "y":newPipe1[0]["y"]},
        {"x": SCREEN_WIDTH * 1.33, "y":newPipe2[0]["y"]},
        {"x": SCREEN_WIDTH * 1.66, "y":newPipe3[0]["y"]}
    ]

    lowerPipes = [ 
        {"x": SCREEN_WIDTH, "y":newPipe1[1]["y"]},
        {"x": SCREEN_WIDTH * 1.33, "y":newPipe2[1]["y"]},
        {"x": SCREEN_WIDTH * 1.66, "y":newPipe3[1]["y"]}
    ]

    score = 0
    pipeSpeedX = -10
    playerSpeedY = -9
    playerFlyingSpeed = -8
    playerMaxSpeed = 10
    playerAccY = 1
    playerFlying = False
    playerY = SCREEN_HEIGHT/2 
    while True:
       
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if x.type == KEYDOWN and (x.key == K_UP or x.key == K_w):
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeed
                    playerFlying = True
                    GAME_SOUNDS["fly"].play()
                
        playerY = playerY + playerSpeedY
        if playerFlying == True:
           playerFlying = False
          

        if not playerFlying and playerSpeedY < playerMaxSpeed:
            playerSpeedY = playerSpeedY + playerAccY      
            
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] = upperPipe["x"] + pipeSpeedX
            lowerPipe["x"] = lowerPipe["x"] + pipeSpeedX

        if 0 < upperPipes[0]["x"] <= abs(pipeSpeedX):
            newPipe = getRandomPipes()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]["x"] < 0:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        playerWidth = GAME_IMAGES["bird"].get_width()
        pipeWidth = GAME_IMAGES["pipe"][0].get_width()
        playerCenterX = playerX + playerWidth/2
        for pipe in upperPipes:
            pipeCenterX = pipe["x"] + pipeWidth/2
            if pipeCenterX < playerCenterX <= abs(pipeSpeedX)+pipeCenterX:
                score = score + 1
                GAME_SOUNDS["point"].play()
                print(score)

        if isHit(playerX, playerY, upperPipes, lowerPipes):
            GAME_SOUNDS["die"].play()
            pygame.time.delay(3000)
            return 

        screen.blit(GAME_IMAGES["background"], (0,0))
        screen.blit(GAME_IMAGES["bird"], (playerX,playerY))    
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(GAME_IMAGES["pipe"][0], (upperPipe["x"], upperPipe["y"]))        
            screen.blit(GAME_IMAGES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))   

        scoreDigits = [int(x) for x in str(score)]
        scoreX = SCREEN_WIDTH - (GAME_IMAGES["number"][0].get_width() * 3)
        scoreY = baseY - GAME_IMAGES["number"][0].get_height()
        for x in scoreDigits:
            screen.blit(GAME_IMAGES["number"][x], (scoreX, scoreY))
            scoreX = scoreX + GAME_IMAGES["number"][0].get_width() + 2
        screen.blit(GAME_IMAGES["base"], (baseX,baseY))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)     

def isHit(playerX, playerY, upperPipes, lowerPipes):
    playerHeight = GAME_IMAGES["bird"].get_height()
    if (playerY + playerHeight - 15) > baseY or playerY < 0:
        return True

    for pipe in upperPipes:
        if (pipe["y"] + pipeHeight > playerY) and (pipe["x"]-playerWidth<playerX<pipe["x"]+pipeWidth):
            return True

    for pipe in lowerPipes:
            if (pipe["y"] < playerY+playerHeight) and (pipe["x"]-playerWidth<playerX<pipe["x"]+pipeWidth):
                return True

    return False

def getRandomPipes():
    gap = GAME_IMAGES["bird"].get_height() * 3
    y2 = randint(gap, baseY)
    y1 = y2 - gap - pipeHeight
    pipeX = SCREEN_WIDTH 
    pipe = [
        {"x":pipeX, "y":y1},
        {"x":pipeX, "y":y2}
     ]
    return pipe

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('BIRD GAME')
GAME_IMAGES["background"] = pygame.image.load("img/background.png").convert_alpha()
GAME_IMAGES["base"] = pygame.image.load("img/base.png").convert_alpha()
GAME_IMAGES["bird"] = pygame.image.load("img/bird.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("img/message.png").convert_alpha()
GAME_IMAGES["pipe"] = [
    pygame.transform.rotate(pygame.image.load("img/pipe.png").convert_alpha(),180),
    pygame.image.load("img/pipe.png").convert_alpha(),
    ]
GAME_IMAGES["number"] = (
    pygame.image.load("img/0.png").convert_alpha(),
    pygame.image.load("img/1.png").convert_alpha(),
    pygame.image.load("img/2.png").convert_alpha(),
    pygame.image.load("img/3.png").convert_alpha(),
    pygame.image.load("img/4.png").convert_alpha(),
    pygame.image.load("img/5.png").convert_alpha(),
    pygame.image.load("img/6.png").convert_alpha(),
    pygame.image.load("img/7.png").convert_alpha(),
    pygame.image.load("img/8.png").convert_alpha(),
    pygame.image.load("img/9.png").convert_alpha()
)    
GAME_SOUNDS["fly"] = pygame.mixer.Sound("sounds/fly.wav")
GAME_SOUNDS["point"] = pygame.mixer.Sound("sounds/point.wav")
GAME_SOUNDS["die"] = pygame.mixer.Sound("sounds/die.wav")
 
pipeHeight = GAME_IMAGES["pipe"][0].get_height()
pipeWidth = GAME_IMAGES["pipe"][0].get_width()
baseX = 0
baseY = SCREEN_HEIGHT - GAME_IMAGES["base"].get_height()
playerX = SCREEN_WIDTH/5
playerY = SCREEN_HEIGHT/2
playerHeight = GAME_IMAGES["bird"].get_height()
playerWidth = GAME_IMAGES["bird"].get_width()
messageX = (SCREEN_WIDTH - GAME_IMAGES["message"].get_width())/2
messageY = (SCREEN_HEIGHT - GAME_IMAGES["message"].get_width())/2

while True:
    welcomeScreen()
    gameLoop()