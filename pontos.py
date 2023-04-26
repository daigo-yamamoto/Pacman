import pygame
from vetor import Vetor2
from constantes import *
import numpy as np


class Pellet(object):
    def __init__(self, row, column):
        self.nome = PONTOS
        self.position = Vetor2(column * LARGURANO, row * ALTURANO)
        self.cor = BRANCO
        self.radius = int(2 * LARGURANO / 16)
        self.collideRadius = 2 * LARGURANO / 16
        self.pontos = 10
        self.visible = True

    def desenha(self, screen):
        if self.visible:
            adjust = Vetor2(LARGURANO, ALTURANO) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.cor, p.intTupla(), self.radius)


class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.nome = PONTOPODER
        self.radius = int(8 * LARGURANO / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class GrupoPontos(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def atualiza(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def desenha(self, screen):
        for pellet in self.pelletList:
            pellet.desenha(screen)
