import pygame
from andarilhos import Andarilhos
from constantes import *
from sprites import FruitSprites

class Fruta(Andarilhos):
    def __init__(self, no):
        Andarilhos.__init__(self, no)
        self.nome = FRUTA
        self.cor = VERDE
        self.lifespan = 5
        self.timer = 0
        self.destruido = False
        self.pontos = 100
        self.setBetweenNodes(DIREITA)
        self.sprites = FruitSprites(self)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destruido = True
