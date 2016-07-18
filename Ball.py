import pygame

from math import sin, cos, radians, acos, asin
from random import randint

from Angle import Angle
from Constants import *
from Sound import Sound

class Ball (object):
    SIZE = 30
    SPEED = 1
    ADD_SPEED = 10 * 1000
    time = 0
    
    def __init__ (self, size, speed, balls):
        '''in - (self, size (diameter), speed, list of balls)'''
        self.rect = pygame.Rect (WINDOWSIZE [0] / 2 - size / 2, randint (100, WINDOWSIZE [1] - 100), size, size)
        self.isColliding_player = False
        self.isColliding_ball = False
        self.speed = speed
        
        if len (balls) >= 1:
            while True:
                for b in balls [:]:
                    if self.rect.colliderect (b.rect):       
                        self.rect.top = randint (100, WINDOWSIZE [1] - 100)
                        break
                else:
                    break
        
        self.direction = randint (0, 359)
        while self.direction < 45:
            self.direction += 45
        while self.direction > 135 and self.direction < 180:
            self.direction -= 45
        while self.direction >= 180 and self.direction < 225:
            self.direction += 45
        while self.direction > 315 and self.direction < 360:
            self.direction -= 45

    def getMoveVector (self):
        '''in - (self)
        Calculates (x, y) vector for movement using direction.
        out - (x, y) tuple of ints'''
        a = Angle.format (self.direction + 90)
        x = int (round (cos (radians (a) ) * self.speed, 0) )
        y = int (round (sin (radians (a) ) * self.speed, 0) )
        return (x, y)

    def getNewDirection (self, b2):
        '''in - (self, collision ball)
        Calculates and implements the ball's new direction after colliding with another ball.'''
        distance_x = abs (self.rect.center [0] - b2.rect.center [0])
        distance_y = abs (self.rect.center [1] - b2.rect.center [1])
        distance_z = float ((distance_x ** 2 + distance_y ** 2) ** 0.5)
        normal1 = acos (distance_x / distance_z)
        normal2 = asin (distance_y / distance_z)
        normal = int (round ((normal1 + normal2) / 2.0, 0))
        self.direction = Angle.format (Angle.opposite (Angle.format (self.direction - 180), normal))

    def update (self, balls, walls, players):
        '''in - (self, list of walls, list of players)
        Updates ball's position, and checks for collisions, changing direction if necessary.'''
        balls_copy = balls [:]
        try:
            del balls_copy [balls_copy.index (self)]
        except:
            pass
        
        for w in walls:
            if self.rect.colliderect (w.rect):
                self.direction = Angle.format (Angle.opposite (Angle.format (self.direction - 180), w.normal) )

        if self.isColliding_player:
            for p in players:
                if self.rect.colliderect (p.rect):
                    break
            else:
                self.isColliding_player = False
                
        else:
            for p in players:
                if self.rect.colliderect (p.rect):
                    self.direction = Angle.format (Angle.opposite (Angle.format (self.direction - 180), p.normal) )
                    self.isColliding_player = True
                    if Sound.isOn:
                        Sound.bounce.play ()

        if self.isColliding_ball:
            for b in balls_copy:
                if self.rect.colliderect (b.rect):
                    break
            else:
                self.isColliding_ball = False
                
        else:
            for b in balls_copy:
                if self.rect.colliderect (b.rect):
                    self.getNewDirection (b)
                    self.isColliding_ball = True
                    if Sound.isOn:
                        Sound.bounce.play ()

        self.rect.move_ip (*self.getMoveVector () )
