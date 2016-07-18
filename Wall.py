import pygame

from Constants import *

class Wall (object):
    SIZE = 10
    
    def __init__ (self, position, size, normal):
        '''in - (self, position (x, y), size (x, y), normal (angle))'''
        self.rect = pygame.Rect (position, size)
        self.normal = normal

    @staticmethod
    def createList ():
        '''Creates top and bottom walls.
        out - list of walls'''
        walls = []
        walls.append (Wall ( (0, 0), (WINDOWSIZE [0],Wall.SIZE), 180) )     # top
        walls.append (Wall ( (0, WINDOWSIZE [1] - Wall.SIZE), (WINDOWSIZE [0],Wall.SIZE), 0) )      # bottom
        return walls
