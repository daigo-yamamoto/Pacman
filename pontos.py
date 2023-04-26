import pygame
from vetor import Vetor2
from constantes import *
import numpy as np


class Pontos(object):
    def __init__(self, linha, column):
        self.nome = PONTOS
        self.posicao = Vetor2(column * LARGURANO, linha * ALTURANO)
        self.cor = BRANCO
        self.radius = int(2 * LARGURANO / 16)
        self.collideRadius = 2 * LARGURANO / 16
        self.pontos = 10
        self.visible = True

    def desenha(self, screen):
        if self.visible:
            adjust = Vetor2(LARGURANO, ALTURANO) / 2
            p = self.posicao + adjust
            pygame.draw.circle(screen, self.cor, p.intTupla(), self.radius)


class PowerPellet(Pontos):
    def __init__(self, linha, column):
        Pontos.__init__(self, linha, column)
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
        self.listaPontos = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numPontosComidos = 0

    def atualiza(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)
        for linha in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[linha][col] in ['.', '+']:
                    self.listaPontos.append(Pontos(linha, col))
                elif data[linha][col] in ['P', 'p']:
                    pp = PowerPellet(linha, col)
                    self.listaPontos.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.listaPontos) == 0:
            return True
        return False

    def desenha(self, screen):
        for pellet in self.listaPontos:
            pellet.desenha(screen)
