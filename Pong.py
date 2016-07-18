# Import and set up modules
import pygame
from math import sin, cos, radians, acos, asin
from random import randint
from copy import deepcopy
from pygame.locals import *
pygame.init ()

# Create constants
WINDOWSIZE = (800, 600)

# Create window
window = pygame.display.set_mode (WINDOWSIZE, 0, 32)
pygame.display.set_caption ("Pong")




class Colour (object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)




class Sound (object):
    isOn = True
    pygame.mixer.music.load ("bg_music.mp3")
    bounce = pygame.mixer.Sound ("funny-bounce.wav")
    point = pygame.mixer.Sound ("point.wav")




class Angle (object):
    @staticmethod
    def format (a):
        '''in - (angle)
        Formats angle to a number from 0 to 359.
        out - angle (int/float)'''
        while a < 0:
            a += 360
        while a >= 360:
            a -= 360
        return a

    @staticmethod
    def opposite (a, n):
        '''in - (angle, normal)
        Calculates the opposite (reflected) angle of the given angle.
        out - angle (int/float)'''
        return Angle.format (2 * n - a)        # n - (a - n)




class Circle (object):
    def __init__ (self, center, radius):
        '''in - (self, position (center), radius)'''
        self.center = center
        self.radius = radius

    @staticmethod
    def getCircle (rect):
        '''in - (Rect)
        Returns a Circle object of the given Rect.
        out - Circle'''
        return Circle (rect.center, (rect.width + rect.height) / 4)

    def isColliding_player (self, c2):
        '''in - (self, other circle)
        Determines if the 2 circles are in collision.
        out - bool'''
        distance_x = abs (self.center [0] - c2.center [0])
        distance_y = abs (self.center [1] - c2.center [1])
        distance_z = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance_z < (self.radius + c2.radius):
            return True
        return False




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

    @staticmethod
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
    Ball.update_all (balls, walls, players, clock)

    # Draw screen:
    drawScreen (walls, players, balls)


pygame.mixer.music.stop ()
pygame.quit ()
