import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilhos

class Fantasma(Andarilhos):
    def __init__(self, no):
        Andarilhos.__init__(self, no)
        self.name = FANTASMA
        self.cor = VERDE
        self.points = 200
        self.chegada = Vetor2()
        self.metodoDirecionamento = self.direcaoChegada
