# Import and set up modules
import pygame
pygame.init ()

from math import sin, cos, radians, acos, asin
from random import randint
from copy import deepcopy
from pygame.locals import *

from Angle import Angle
from Ball import Ball
from Circle import Circle
from Colour import Colour
from Constants import *
from Player import Player
from Sound import Sound
from Wall import Wall

# Create window
window = pygame.display.set_mode (WINDOWSIZE, 0, 32)
pygame.display.set_caption ("Pong")




def update_all (balls, walls, players, clock):
    Ball.time += clock.tick ()
    if Ball.time > Ball.ADD_SPEED:
        balls.append (Ball (Ball.SIZE, Ball.SPEED, balls [:] ) )
        Ball.time = 0
        
    for i, b in enumerate (balls):
        # The ball is out of the window
        if b.rect.right < 0 or b.rect.left > WINDOWSIZE [0]:
            if b.rect.right < 0:
                players [1].score += 1
            if b.rect.left > WINDOWSIZE [0]:
                players [0].score += 1
            # Delete all balls and reset with 1 ball
            for i in range (len (balls)) [::-1]:
                del balls [i]
            balls.append (Ball (Ball.SIZE, Ball.SPEED, [] ) )

            for p in players:
                p.reset ()

            if Sound.isOn:
                Sound.point.play ()
            drawScreen (walls, players, balls)
            pygame.time.wait (1000)
            break

    balls_old = balls [:]
    for b in balls:
        b.update (balls_old [:], walls, players)


def drawScreen (walls, players, balls):
    window.fill ((255, 255, 255))
    pygame.draw.line (window, Colour.BLUE, (WINDOWSIZE [0] / 2, 0), (WINDOWSIZE [0] / 2, WINDOWSIZE [1]) )
    for w in walls:
        pygame.draw.rect (window, Colour.BLACK, w.rect)
    for p in players:
        pygame.draw.rect (window, Colour.YELLOW, p.rect)
    for b in balls:
        pygame.draw.circle (window, Colour.BLUE, b.rect.center, b.rect.width / 2)
        
    scores_surfaces = [players [0].getScoreSurface (), players [1].getScoreSurface ()]
    scores_rects = [scores_surfaces [0].get_rect (), scores_surfaces [1].get_rect ()]
    scores_rects [0].topright = (WINDOWSIZE [0] / 2 - 50, Wall.SIZE)
    scores_rects [1].topleft = scores_rects [1].topleft = (WINDOWSIZE [0] / 2 + 50, Wall.SIZE)
    for i in range (2):
        window.blit (scores_surfaces [i], scores_rects [i])
    pygame.display.update ()




# Create game objects
clock = pygame.time.Clock ()
walls = Wall.createList ()
players = [Player (25, Player.SIZE, 2, 270), Player (775, Player.SIZE, 2, 90)]
balls = [Ball (Ball.SIZE, Ball.SPEED, [])]

if Sound.isOn:
    pygame.mixer.music.set_volume (0.6)
    pygame.mixer.music.play ()

keepGoing = True
while keepGoing:
    for event in pygame.event.get ():
        if event.type == QUIT:
            keepGoing = False

        # Set  players' directions
        elif event.type == KEYDOWN:
            if event.key == ord ("w"):
                players [0].moveUp = True
                players [0].moveDown = False
                
            elif event.key == ord ("s"):
                players [0].moveDown = True
                players [0].moveUp = False

            elif event.key == K_UP:
                players [1].moveUp = True
                players [1].moveDown = False
                
            elif event.key == K_DOWN:
                players [1].moveDown = True
                players [1].moveUp = False

        elif event.type == KEYUP:
            if event.key == ord ("w"):
                players [0].moveUp = False
                
            elif event.key == ord ("s"):
                players [0].moveDown = False
                
            elif event.key == K_UP:
                players [1].moveUp = False
                
            elif event.key == K_DOWN:
                players [1].moveDown = False

    # Update game objects
    for p in players:
        p.update (walls)
    update_all (balls, walls, players, clock)

    # Draw screen:
    drawScreen (walls, players, balls)


pygame.mixer.music.stop ()
pygame.quit ()
