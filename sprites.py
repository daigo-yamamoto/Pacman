import pygame
from constantes import *
import numpy as np
from animacao import Animacao

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
MORTO = 5


class Spritesheet(object):
    def __init__(self):
        self.folha = pygame.image.load("spritesheetfinal.png").convert()
        transcolor = self.folha.get_at((0, 0))
        self.folha.set_colorkey(transcolor)
        largura = int(self.folha.get_width() / BASETILEWIDTH * LARGURANO)
        altura = int(self.folha.get_height() / BASETILEHEIGHT * ALTURANO)
        self.folha = pygame.transform.scale(self.folha, (largura, altura))

    def getImage(self, x, y, width, height):
        x *= LARGURANO
        y *= ALTURANO
        self.folha.set_clip(pygame.Rect(x, y, width, height))
        return self.folha.subsurface(self.folha.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def defineAnimations(self):
        self.animations[ESQUERDA] = Animacao(((0, 0), (2, 0), (4, 0), (6, 0)))
        self.animations[DIREITA] = Animacao(((24, 0), (26, 0), (28, 0), (30, 0)))
        self.animations[CIMA] = Animacao(((0, 2), (2, 2), (4, 2), (6, 2), (8, 2)))
        self.animations[BAIXO] = Animacao(((24, 2), (26, 2), (28, 2), (30, 2), (32, 2)))
        self.animations[MORTO] = Animacao(((24, 4), (26, 4), (28, 4), (30, 4), (32, 4)), velocidade=1, loop=False)

    def update(self, dt):
        if self.entity.vivo == True:
            if self.entity.direcao == ESQUERDA:
                self.entity.image = self.getImage(*self.animations[ESQUERDA].atualiza(dt))
                self.stopimage = (2, 0)
            elif self.entity.direcao == DIREITA:
                self.entity.image = self.getImage(*self.animations[DIREITA].atualiza(dt))
                self.stopimage = (28, 0)
            elif self.entity.direcao == BAIXO:
                self.entity.image = self.getImage(*self.animations[BAIXO].atualiza(dt))
                self.stopimage = (30, 2)
            elif self.entity.direcao == CIMA:
                self.entity.image = self.getImage(*self.animations[CIMA].atualiza(dt))
                self.stopimage = (8, 2)
            elif self.entity.direcao == PARADO:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[MORTO].atualiza(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURANO, 2 * ALTURANO)


class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BAFAO: 0, ALONSO: 2, ROGERIO: 4, MANGA: 6}
        self.entity = entity
        self.entity.image = self.getStartImage()

    def update(self, dt):
        x = self.x[self.entity.nome]
        if self.entity.modo.atual in [INICIO, PERSEGUIR]:
            if self.entity.direcao == ESQUERDA:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direcao == DIREITA:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direcao == BAIXO:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direcao == CIMA:
                self.entity.image = self.getImage(x, 4)
        elif self.entity.modo.atual == ALEATORIO:
            self.entity.image = self.getImage(10, 4)
        elif self.entity.modo.atual == SPAWN:
            if self.entity.direcao == ESQUERDA:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direcao == DIREITA:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direcao == BAIXO:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direcao == CIMA:
                self.entity.image = self.getImage(8, 4)

    def getStartImage(self):
        return self.getImage(self.x[self.entity.nome], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURANO, 2 * ALTURANO)


class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))

    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURANO, 2 * ALTURANO)


class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURANO, 2 * ALTURANO)


class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, LARGURANO, ALTURANO)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col * LARGURANO, row * ALTURANO))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col * LARGURANO, row * ALTURANO))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)
