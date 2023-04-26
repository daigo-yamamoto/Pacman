import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilhos
from modos import ModeController

class Fantasma(Andarilhos):
    def __init__(self, no, pacman=None):
        Andarilhos.__init__(self, no)
        self.name = FANTASMA
        self.cor = VERDE
        self.points = 200
        self.chegada = Vetor2()
        self.metodoDirecionamento = self.direcaoChegada
        self.pacman = pacman
        self.modo = ModeController(self)

    def atualiza(self, dt):
        self.modo.update(dt)
        if self.modo.atual is SALVAR:
            self.salvar()
        elif self.modo.atual is PERSEGUIR:
            self.perseguir()
        Andarilhos.atualiza(self, dt)

    def salvar(self):
        self.chegada = Vetor2()

    def perseguir(self):
        self.chegada = self.pacman.posicao
