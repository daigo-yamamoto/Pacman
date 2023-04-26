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
        self.modo.atualiza(dt)
        if self.modo.atual is INICIO:
            self.salvar()
        elif self.modo.atual is PERSEGUIR:
            self.perseguir()
        Andarilhos.atualiza(self, dt)

    def salvar(self):
        self.chegada = Vetor2()

    def perseguir(self):
        self.chegada = self.pacman.posicao

    def startFreight(self):
        self.modo.defineModoAleatorio()
        if self.modo.atual == ALEATORIO:
            self.defineVelocidade(50)
            self.metodoDirecionamento = self.direcaoAleatoria

    def normalMode(self):
        self.defineVelocidade(100)
        self.metodoDirecionamento = self.direcaoChegada

    def spawn(self):
        self.chegada = self.spawnNode.position

    def defienNoSpawn(self, node):
        self.spawnNode = node

    def comecaSpawn(self):
        self.modo.defineModoAleatorio()
        if self.modo.atual == SPAWN:
            self.defineVelocidade(150)
            self.metodoDirecionamento = self.direcaoChegada
            self.spawn()
