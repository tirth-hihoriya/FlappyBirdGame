import random
import sys   # sys.exit
import pygame
from pygame.locals import *  # basic pygame imports

# Some Global variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))   # initialize screen or window for diaplay
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES  = {}
GAME_SOUNDS = {}
PLAYER = './sprites/fb4.png'
BACKGROUND = './sprites/bg_flappy_bird.png'
PIPE = './sprites/pipe.png'

def welcomeScreen():
    """
    shows welcome screen(img) 
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for  event in pygame.event.get():
            #if user clicks on cross button , close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            #if the user presses space or up key, start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0, 0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'],(messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

               
def maingame():
    score=0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # create 2 pipes for botting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipes
    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
    ]
    #my list of lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
    ]

    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  #velocity while flapping
    playerFlapped =  False  # it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type ==QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    # GAME_SOUNDS['wing'].play()
                
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # this function will return true if  the player is  crashed
        if crashTest:
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos < pipeMidPos +4 :
                score += 1
                print(f"Your score is {score}")
            # GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,GROUNDY - playery - playerHeight)

        # nove pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx
        
        # add a new pipe  when the first is about to cross to the leftmost part of the screen/
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if  the pipe is out o f the screen, remove it
        if upperPipes[0]['x'] / -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # let's blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits  = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    return False

def getRandomPipe():
    """
    generate positionss of two pipes(on bottom straight and one top rotated) for bitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2/offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight = y2 + offset
    pipe = [
        {'x':pipeX,'y':-y1},  #upper  pipe
        {'x':pipeX,'y': y2}  #lower  pipe
    ]
    return pipe




if __name__=="__main__":
    # Game will start from here
    pygame.init() # Initialize all pygame's module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Tirth Hihoriya')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('./sprites/zero.png').convert_alpha(),  
        pygame.image.load('./sprites/one.png').convert_alpha(),  
        pygame.image.load('./sprites/two.png').convert_alpha(),  
        pygame.image.load('./sprites/three.png').convert_alpha(),  
        pygame.image.load('./sprites/four.png').convert_alpha(),  
        pygame.image.load('./sprites/five.png').convert_alpha(),  
        pygame.image.load('./sprites/six.png').convert_alpha(),  
        pygame.image.load('./sprites/seven.png').convert_alpha(),  
        pygame.image.load('./sprites/eight.png').convert_alpha(),  
        pygame.image.load('./sprites/nine.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load('./sprites/msg.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('./sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
# Game sounds

# GAME_SOUNDS['die'] = pygame.mixer.Sound('./sprites/die.mp3')
# GAME_SOUNDS['hit'] = pygame.mixer.Sound('./sprites/die.mp3')
# GAME_SOUNDS['point'] = pygame.mixer.Sound('./sprites/flap2.mp3')
# GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('./sprites/flap2.mp3')
# GAME_SOUNDS['wing'] = pygame.mixer.Sound('./sprites/flap.mp3')

GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen()   # shows welcome screen to user until he presses a button
    maingame()  # this is maingame function
