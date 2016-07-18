import pygame

from copy import deepcopy

from Colour import Colour
from Constants import *

class Player (object):
    SIZE = (15, 75)
    
    def __init__ (self, x_position, size, speed, normal):
        '''in - (self, position (x), size (x, y), speed, normal (angle))'''
        global WINDOWSIZE

        self.rect_original = pygame.Rect ( (0, 0), size)
        self.rect_original.centerx = x_position
        self.rect_original.centery = WINDOWSIZE [1] / 2
        self.rect = deepcopy (self.rect_original)
        
        self.moveUp = False
        self.moveDown = False
        self.speed = speed
        self.normal = normal
        self.score = 0

    def reset (self):
        '''in - (self)
        Reset's player's position and movement variables.'''
        self.rect = deepcopy (self.rect_original)
        self.moveUp = False
        self.moveDown = False

    def getScoreSurface (self):
        '''in - (self)
        Creates surface object of player's score.
        out - Surface'''
        return pygame.font.SysFont (None, 100).render (str (self.score), True, Colour.YELLOW)

    def update (self, walls):
        '''in - (self, list of walls)
        Updates player's position.'''
        test = None
        if self.moveUp:
            test = self.rect.move (0, -self.speed)
        if self.moveDown:
            test = self.rect.move (0, self.speed)

        if test != None:
            for w in walls:
                if test.colliderect (w.rect):
                    break
            else:
                self.rect = test

    @staticmethod
    def update_all (players, walls):
        '''in - (list of players, list of walls)
        Calls update () on all players.'''
        for p in players:
            p.update (walls)
