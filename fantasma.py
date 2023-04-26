import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilhos
from modos import ModeController
from sprites import GhostSprites

class Fantasma(Andarilhos):
    def __init__(self, no, pacman=None, bafao=None):
        Andarilhos.__init__(self, no)
        self.nome = FANTASMA
        self.cor = VERDE
        self.pontos = 200
        self.chegada = Vetor2()
        self.metodoDirecionamento = self.direcaoChegada
        self.pacman = pacman
        self.modo = ModeController(self)
        self.bafao = bafao
        self.noCasa = no

    def atualiza(self, dt):
        self.modo.atualiza(dt)
        if self.modo.atual is INICIO:
            self.inicio()
        elif self.modo.atual is PERSEGUIR:
            self.perseguir()
        Andarilhos.atualiza(self, dt)

    def inicio(self):
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
        self.noCasa.denyAccess(BAIXO, self)

    def spawn(self):
        self.chegada = self.spawnNode.posicao

    def defineNoSpawn(self, node):
        self.spawnNode = node

    def comecaSpawn(self):
        self.modo.defineModoAleatorio()
        if self.modo.atual == SPAWN:
            self.defineVelocidade(150)
            self.metodoDirecionamento = self.direcaoChegada
            self.spawn()

    def reset(self):
        Andarilhos.reset(self)
        self.pontos = 200
        self.metodoDirecionamento = self.direcaoChegada


class GrupoFantasma(object):
    def __init__(self, no, pacman):
        self.bafao = Bafao(no, pacman)
        self.alonso = Alonso(no, pacman)
        self.rogerio = Rogerio(no, pacman, self.bafao)
        self.manga = Manga(no, pacman)
        self.fantasmas = [self.bafao, self.alonso, self.rogerio, self.manga]

    def __iter__(self):
        return iter(self.fantasmas)

    def atualiza(self, dt):
        for fantasma in self:
            fantasma.atualiza(dt)

    def comecaAleatorio(self):
        for fantasma in self:
            fantasma.startFreight()
        self.resetaPontos()

    def defineNoSpawn(self, no):
        for fantasma in self:
            fantasma.defineNoSpawn(no)

    def atualisaPontos(self):
        for fantasma in self:
            fantasma.pontos *= 2

    def resetaPontos(self):
        for fantasma in self:
            fantasma.pontos = 200

    def reset(self):
        for fantasma in self:
            fantasma.reset()

    def esconde(self):
        for fantasma in self:
            fantasma.visivel = False

    def mostra(self):
        for fantasma in self:
            fantasma.visivel = True

    def desenha(self, tela):
        for fantasma in self:
            fantasma.desenha(tela)

class Bafao(Fantasma):
    def __init__(self, no, pacman=None, bafao=None):
        Fantasma.__init__(self, no, pacman, bafao)
        self.nome = BAFAO
        self.color = VERMELHO
        self.sprites = GhostSprites(self)

class Alonso(Fantasma):
    def __init__(self, no, pacman=None, alonso=None):
        Fantasma.__init__(self, no, pacman, alonso)
        self.nome = ALONSO
        self.color = ROSA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.chegada = Vetor2(LARGURA_NO * NUM_COLUNA, 0)

    def perseguir(self):
        self.chegada = self.pacman.posicao + self.pacman.direcoes[self.pacman.direcao] * LARGURA_NO * 4

class Rogerio(Fantasma):
    def __init__(self, no, pacman=None, rogerio=None):
        Fantasma.__init__(self, no, pacman, rogerio)
        self.nome = ROGERIO
        self.color = AZULCLARO
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.chegada = Vetor2(LARGURA_NO*NUM_COLUNA, ALTURA_NO*NUM_LINHA)

    def perseguir(self):
        vec1 = self.pacman.posicao + self.pacman.direcoes[self.pacman.direcao] * LARGURA_NO * 2
        vec2 = (vec1 - self.bafao.posicao) * 2
        self.chegada = self.bafao.posicao + vec2

class Manga(Fantasma):
    def __init__(self, no, pacman=None, manga=None):
        Fantasma.__init__(self, no, pacman, manga)
        self.nome = MANGA
        self.cor = LARANJA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.chegada = Vetor2(0, LARGURA_NO*NUM_LINHA)

    def perseguir(self):
        d = self.pacman.posicao - self.posicao
        ds = d.distanciaQuadrado()
        if ds <= (LARGURA_NO * 8)**2:
            self.inicio()
        else:
            self.chegada = self.pacman.posicao + self.pacman.direcoes[self.pacman.direcao] * LARGURA_NO * 4
