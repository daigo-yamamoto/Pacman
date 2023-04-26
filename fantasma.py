import pygame
from pygame.locals import *
from vector import Vector2
from constantes import *
from andarilhos import Andarilhos

class Fantasma(Andarilhos):
    def __init__(self, no):
        Andarilhos.__init__(self, no)
        self.name = FANTASMA
        self.points = 200