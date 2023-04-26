import pygame
from andarilhos import Andarilho
from constantes import *
from sprites import FruitSprites

class Fruta(Andarilho):
    def __init__(self, node):
        Andarilho.__init__(self, node)
        self.nome = FRUTA
        self.cor = VERDE
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.setBetweenNodes(DIREITA)
        self.sprites = FruitSprites(self)

    def atualiza(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True