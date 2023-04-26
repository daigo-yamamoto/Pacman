import pygame
from constantes import *
import numpy as np
from animacao import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5


class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * LARGURA_NO)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * ALTURA_NO)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= LARGURA_NO
        y *= ALTURA_NO
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.imagem = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def defineAnimations(self):
        self.animations[ESQUERDA] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[DIREITA] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[CIMA] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[BAIXO] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(
            ((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)),
            speed=6, loop=False)

    def update(self, dt):
        if self.entity.alive == True:
            if self.entity.direction == ESQUERDA:
                self.entity.imagem = self.getImage(*self.animations[ESQUERDA].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == DIREITA:
                self.entity.imagem = self.getImage(*self.animations[DIREITA].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == BAIXO:
                self.entity.imagem = self.getImage(*self.animations[BAIXO].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == CIMA:
                self.entity.imagem = self.getImage(*self.animations[CIMA].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == PARADO:
                self.entity.imagem = self.getImage(*self.stopimage)
        else:
            self.entity.imagem = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class GhostSprites(Spritesheet):
    def __init__(self, andarilho):
        Spritesheet.__init__(self)
        self.x = {BAFAO: 0, ALONSO: 2, ROGERIO: 4, MANGA: 6}
        self.andarilho = andarilho
        self.andarilho.imagem = self.getStartImage()

    def update(self, dt):
        x = self.x[self.andarilho.nome]
        if self.andarilho.mode.current in [INICIO, PERSEGUIR]:
            if self.andarilho.direction == ESQUERDA:
                self.andarilho.imagem = self.getImage(x, 8)
            elif self.andarilho.direction == DIREITA:
                self.andarilho.imagem = self.getImage(x, 10)
            elif self.andarilho.direction == BAIXO:
                self.andarilho.imagem = self.getImage(x, 6)
            elif self.andarilho.direction == CIMA:
                self.andarilho.imagem = self.getImage(x, 4)
        elif self.andarilho.mode.current == ALEATORIO:
            self.andarilho.imagem = self.getImage(10, 4)
        elif self.andarilho.mode.current == SPAWN:
            if self.andarilho.direction == ESQUERDA:
                self.andarilho.imagem = self.getImage(8, 8)
            elif self.andarilho.direction == DIREITA:
                self.andarilho.imagem = self.getImage(8, 10)
            elif self.andarilho.direction == BAIXO:
                self.andarilho.imagem = self.getImage(8, 6)
            elif self.andarilho.direction == CIMA:
                self.andarilho.imagem = self.getImage(8, 4)

    def getStartImage(self):
        return self.getImage(self.x[self.andarilho.nome], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class FruitSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.entity.imagem = self.getStartImage(1 % len(self.fruits))

    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


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
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, LARGURA_NO, ALTURA_NO)

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
                    background.blit(sprite, (col * LARGURA_NO, row * ALTURA_NO))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col * LARGURA_NO, row * ALTURA_NO))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)
