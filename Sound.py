import pygame

class Sound (object):
    isOn = True
    pygame.mixer.music.load ("bg_music.mp3")
    bounce = pygame.mixer.Sound ("funny-bounce.wav")
    point = pygame.mixer.Sound ("point.wav")
