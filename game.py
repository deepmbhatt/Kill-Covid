import pygame
from pygame.locals import *
import sys 
from random import randint
import tkinter as tk
import tkinter.messagebox

# Constants for screen dimensions and game properties
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
FPS = 30
GAME_IMAGES = {}
GAME_SOUNDS = {}

# Function to display the welcome screen
def welcomeScreen(i):
    while True:
        # Display background and bird image
        screen.blit(GAME_IMAGES["background"], (0,0))
        screen.blit(GAME_IMAGES["bird"], (playerX,playerY))
        
        # Display message based on value of i
        if i == 3:
            screen.blit(GAME_IMAGES["message"], (messageX, messageY))
       
        pygame.display.update()
        
        # Event handling for quitting or starting game
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if x.type == KEYDOWN and x.key == K_SPACE:
                return
                
# Main game loop
def gameLoop():
    # Initialize pipes for the game
    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()
    newPipe3 = getRandomPipes()

    upperPipes = [ 
        {"x": SCREEN_WIDTH, "y": newPipe1[0]["y"]},
        {"x": SCREEN_WIDTH * 1.33, "y": newPipe2[0]["y"]},
        {"x": SCREEN_WIDTH * 1.66, "y": newPipe3[0]["y"]}
    ]

    lowerPipes = [ 
        {"x": SCREEN_WIDTH, "y": newPipe1[1]["y"]},
        {"x": SCREEN_WIDTH * 1.33, "y": newPipe2[1]["y"]},
        {"x": SCREEN_WIDTH * 1.66, "y": newPipe3[1]["y"]}
    ]

    # Initialize game variables
    score = 0
    pipeSpeedX = -10
    playerSpeedY = -9
    playerFlyingSpeed = -8
    playerMaxSpeed = 10
    playerAccY = 1
    playerFlying = False
    playerY = SCREEN_HEIGHT / 2 
    
    while True:
        # Event handling for quitting or controlling the bird
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if x.type == KEYDOWN and (x.key == K_UP or x.key == K_w or x.key == K_SPACE):
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeed
                    playerFlying = True
                    GAME_SOUNDS["fly"].play()
                
        # Update player's position based on flying status
        playerY = playerY + playerSpeedY
        if playerFlying == True:
            playerFlying = False
          
        # Update player's speed when not flying
        if not playerFlying and playerSpeedY < playerMaxSpeed:
            playerSpeedY = playerSpeedY + playerAccY      
            
        # Update positions of upper and lower pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] = upperPipe["x"] + pipeSpeedX
            lowerPipe["x"] = lowerPipe["x"] + pipeSpeedX

        # Add new pipes when needed and remove old pipes
        if 0 < upperPipes[0]["x"] <= abs(pipeSpeedX):
            newPipe = getRandomPipes()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]["x"] < 0:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Check for collision with pipes and update score
        playerWidth = GAME_IMAGES["bird"].get_width()
        pipeWidth = GAME_IMAGES["pipe"][0].get_width()
        playerCenterX = playerX + playerWidth / 2
        
        for pipe in upperPipes:
            pipeCenterX = pipe["x"] + pipeWidth / 2
            if pipeCenterX < playerCenterX <= abs(pipeSpeedX) + pipeCenterX:
                score = score + 1
                GAME_SOUNDS["point"].play()
                print(score)

        # Check for collision with pipes or ground
        if isHit(playerX, playerY, upperPipes, lowerPipes):
            GAME_SOUNDS["die"].play()
            pygame.time.delay(3000)
            return 

        # Render game elements on screen
        screen.blit(GAME_IMAGES["background"], (0,0))
        screen.blit(GAME_IMAGES["bird"], (playerX, playerY))    
        
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(GAME_IMAGES["pipe"][0], (upperPipe["x"], upperPipe["y"]))        
            screen.blit(GAME_IMAGES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))   

        # Display score on screen
        scoreDigits = [int(x) for x in str(score)]
        scoreX = SCREEN_WIDTH - (GAME_IMAGES["number"][0].get_width() * 3)
        scoreY = baseY - GAME_IMAGES["number"][0].get_height()
        
        for x in scoreDigits:
            screen.blit(GAME_IMAGES["number"][x], (scoreX, scoreY))
            scoreX = scoreX + GAME_IMAGES["number"][0].get_width() + 2
        
        # Display base image at bottom of screen
        screen.blit(GAME_IMAGES["base"], (baseX, baseY))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)     

# Function to check if the bird hits any pipes
def isHit(playerX, playerY, upperPipes, lowerPipes):
    playerHeight = GAME_IMAGES["bird"].get_height()

    for pipe in upperPipes:
        if (pipe["y"] + pipeHeight > playerY) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True

    for pipe in lowerPipes:
        if (pipe["y"] < playerY + playerHeight) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True

    return False

# Function to generate random positions for pipes
def getRandomPipes():
    gap = GAME_IMAGES["bird"].get_height() * 3
    y2 = randint(gap, baseY)
    y1 = y2 - gap - pipeHeight
    pipeX = SCREEN_WIDTH 
    pipe = [
        {"x": pipeX, "y": y1},
        {"x": pipeX, "y": y2}
    ]
    return pipe

# Function to display vaccination status messages
def vac_remaining(i):
    if i == 3:
        root = tk.Tk()
        root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
        root.withdraw()
        tkinter.messagebox.showinfo("Kill-Covid", "You have No vaccine taken\nPress Spacebar to continue")
        root.deiconify()
        root.destroy()
        root.quit()
    elif i == 2:
        root = tk.Tk()
        root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
        root.withdraw()
        tkinter.messagebox.showinfo("Kill-Covid", "1st dose of vaccine successfully taken\nPress Spacebar to continue")
        root.deiconify()
        root.destroy()
        root.quit()
    elif i == 1:
        root = tk.Tk()
        root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
        root.withdraw()
        tkinter.messagebox.showinfo("Kill-Covid", "2nd dose of vaccine successfully taken\nPress Spacebar to continue")
        root.deiconify()
        root.destroy()
        root.quit()

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BIRD GAME')

# Load images and sounds used in the game
GAME_IMAGES["background"] = pygame.image.load("./img/background.png").convert_alpha()
GAME_IMAGES["base"] = pygame.image.load("./img/base.png").convert_alpha()
GAME_IMAGES["bird"] = pygame.image.load("./img/bird.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("./img/message.png").convert_alpha()
GAME_IMAGES["pipe"] = [
    pygame.transform.rotate(pygame.image.load("./img/pipe.png").convert_alpha(), 180),
    pygame.image.load("./img/pipe.png").convert_alpha(),
]
GAME_IMAGES["number"] = (
    pygame.image.load("./img/0.png").convert_alpha(),
    pygame.image.load("./img/1.png").convert_alpha(),
    pygame.image.load("./img/2.png").convert_alpha(),
    pygame.image.load("./img/3.png").convert_alpha(),
    pygame.image.load("./img/4.png").convert_alpha(),
    pygame.image.load("./img/5.png").convert_alpha(),
    pygame.image.load("./img/6.png").convert_alpha(),
    pygame.image.load("./img/7.png").convert_alpha(),
    pygame.image.load("./img/8.png").convert_alpha(),
    pygame.image.load("./img/9.png").convert_alpha()
)    
# Load game sounds
GAME_SOUNDS["fly"] = pygame.mixer.Sound("./sounds/fly.mp3")
GAME_SOUNDS["point"] = pygame.mixer.Sound("./sounds/point.wav")
GAME_SOUNDS["die"] = pygame.mixer.Sound("./sounds/die.mp3")

# Dimensions and positions for game elements
pipeHeight = GAME_IMAGES["pipe"][0].get_height()
pipeWidth = GAME_IMAGES["pipe"][0].get_width()
baseX = 0
baseY = SCREEN_HEIGHT - GAME_IMAGES["base"].get_height()
playerX = SCREEN_WIDTH / 5
playerY = SCREEN_HEIGHT / 2
playerHeight = GAME_IMAGES["bird"].get_height()
playerWidth = GAME_IMAGES["bird"].get_width()
messageX = (SCREEN_WIDTH - GAME_IMAGES["message"].get_width()) / 2
messageY = (SCREEN_HEIGHT - GAME_IMAGES["message"].get_height()) / 2

# Initialize 'i' for vaccination status
i = 3

# Main game loop
while True:
    # Display welcome screen based on vaccination status
    welcomeScreen(i)
    
    # Display vaccination message based on 'i'
    vac_remaining(i)
    
    # Start the game loop
    gameLoop()
    
    # Decrease 'i' after each game iteration
    i = i - 1
    print("value of i:", i)

    # If 'i' reaches 0, show final vaccination message
    if i == 0:
        root = tk.Tk()
        root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
        root.withdraw()
        tkinter.messagebox.showinfo("Kill-Covid", "Booster dose of vaccine successfully taken\nCongratulations, you are successfully vaccinated\nPress Spacebar to continue")
        if tkinter.messagebox.askyesno("Kill-Covid", "Do you want to play again?\nPress Spacebar to continue") == True:
            i = i + 3
        else:
            pygame.quit()
            sys.exit()
        root.deiconify()
        root.destroy()
        root.quit()