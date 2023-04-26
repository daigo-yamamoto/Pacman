import pygame
from constantes import *
import numpy as np
from animacao import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5


class Spritesheet(object):
    def __init__(self):
        self.folha = pygame.image.load("spritesheetfinal.png").convert()
        transcolor = self.folha.get_at((0, 0))
        self.folha.set_colorkey(transcolor)
        largura = int(self.folha.get_width() / BASETILEWIDTH * LARGURA_NO)
        altura = int(self.folha.get_height() / BASETILEHEIGHT * ALTURA_NO)
        self.folha = pygame.transform.scale(self.folha, (largura, altura))

    def getImage(self, x, y, width, height):
        x *= LARGURA_NO
        y *= ALTURA_NO
        self.folha.set_clip(pygame.Rect(x, y, width, height))
        return self.folha.subsurface(self.folha.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.andarilho = entity
        self.andarilho.imagem = self.getStartImage()
        self.animacao = {}
        self.defineAnimations()
        self.imagemParada = (8, 0)

    def defineAnimations(self):
        self.animacao[ESQUERDA] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animacao[DIREITA] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animacao[CIMA] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animacao[BAIXO] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))
        self.animacao[DEATH] = Animator(
            ((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)),
            speed=6, loop=False)

    def update(self, dt):
        if self.andarilho.alive == True:
            if self.andarilho.direcao == ESQUERDA:
                self.andarilho.imagem = self.getImage(*self.animacao[ESQUERDA].atualiza(dt))
                self.imagemParada = (8, 0)
            elif self.andarilho.direcao == DIREITA:
                self.andarilho.imagem = self.getImage(*self.animacao[DIREITA].atualiza(dt))
                self.imagemParada = (10, 0)
            elif self.andarilho.direcao == BAIXO:
                self.andarilho.imagem = self.getImage(*self.animacao[BAIXO].atualiza(dt))
                self.imagemParada = (8, 2)
            elif self.andarilho.direcao == CIMA:
                self.andarilho.imagem = self.getImage(*self.animacao[CIMA].atualiza(dt))
                self.imagemParada = (10, 2)
            elif self.andarilho.direcao == PARADO:
                self.andarilho.imagem = self.getImage(*self.imagemParada)
        else:
            self.andarilho.imagem = self.getImage(*self.animacao[DEATH].atualiza(dt))

    def reset(self):
        for key in list(self.animacao.keys()):
            self.animacao[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BAFAO: 0, ALONSO: 2, ROGERIO: 4, MANGA: 6}
        self.andarilho = entity
        self.andarilho.imagem = self.getStartImage()

    def atualiza(self, dt):
        x = self.x[self.andarilho.nome]
        if self.andarilho.modo.atual in [INICIO, PERSEGUIR]:
            if self.andarilho.direcao == ESQUERDA:
                self.andarilho.imagem = self.getImage(x, 8)
            elif self.andarilho.direcao == DIREITA:
                self.andarilho.imagem = self.getImage(x, 10)
            elif self.andarilho.direcao == BAIXO:
                self.andarilho.imagem = self.getImage(x, 6)
            elif self.andarilho.direcao == CIMA:
                self.andarilho.imagem = self.getImage(x, 4)
        elif self.andarilho.modo.atual == ALEATORIO:
            self.andarilho.imagem = self.getImage(10, 4)
        elif self.andarilho.modo.atual == SPAWN:
            if self.andarilho.direcao == ESQUERDA:
                self.andarilho.imagem = self.getImage(8, 8)
            elif self.andarilho.direcao == DIREITA:
                self.andarilho.imagem = self.getImage(8, 10)
            elif self.andarilho.direcao == BAIXO:
                self.andarilho.imagem = self.getImage(8, 6)
            elif self.andarilho.direcao == CIMA:
                self.andarilho.imagem = self.getImage(8, 4)

    def getStartImage(self):
        return self.getImage(self.x[self.andarilho.nome], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.andarilho = entity
        self.frutas = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.andarilho.imagem = self.getStartImage(level % len(self.frutas))

    def getStartImage(self, key):
        return self.getImage(*self.frutas[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.imagens) > 0:
            self.imagens.pop(0)

    def resetLives(self, numlives):
        self.imagens = []
        for i in range(numlives):
            self.imagens.append(self.getImage(0, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * LARGURA_NO, 2 * ALTURA_NO)


class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.dados = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, LARGURA_NO, ALTURA_NO)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, tela_fundo, y):
        for linha in list(range(self.dados.shape[0])):
            for coluna in list(range(self.dados.shape[1])):
                if self.dados[linha][coluna].isdigit():
                    x = int(self.dados[linha][coluna]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[linha][coluna])
                    sprite = self.rotate(sprite, rotval)
                    tela_fundo.blit(sprite, (coluna * LARGURA_NO, linha * ALTURA_NO))
                elif self.dados[linha][coluna] == '=':
                    sprite = self.getImage(10, 8)
                    tela_fundo.blit(sprite, (coluna * LARGURA_NO, linha * ALTURA_NO))

        return tela_fundo

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)
