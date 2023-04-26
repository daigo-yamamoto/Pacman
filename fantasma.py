import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilho
from modos import ModeController
from sprites import GhostSprites

class Fantasma(Andarilho):
    def __init__(self, no, pacman=None, bafao=None):
        Andarilho.__init__(self, no)
        self.nome = FANTASMA
        self.pontos = 200
        self.chegada = Vetor2()
        self.metodoDirecionamento = self.direcaoChegada
        self.pacman = pacman
        self.modo = ModeController(self)
        self.bafao = bafao
        self.NoCasa = no

    def reset(self):
        Andarilho.reset(self)
        self.pontos = 200
        self.metodoDirecionamento = self.direcaoChegada

    def atualiza(self, dt):
        self.sprites.update(dt)
        self.modo.atualiza(dt)
        if self.modo.atual is INICIO:
            self.inicio()
        elif self.modo.atual is PERSEGUIR:
            self.perseguir()
        Andarilho.atualiza(self, dt)

    def inicio(self):
        self.chegada = Vetor2()

    def perseguir(self):
        self.chegada = self.pacman.posicao

    def spawn(self):
        self.chegada = self.NoSpawn.posicao

    def defineNoSpawn(self, no):
        self.NoSpawn = no

    def comecaSpawn(self):
        self.modo.setSpawnMode()
        if self.modo.atual == SPAWN:
            self.setSpeed(150)
            self.metodoDirecionamento = self.direcaoChegada
            self.spawn()

    def comecaAleatorio(self):
        self.modo.setFreightMode()
        if self.modo.atual == ALEATORIO:
            self.setSpeed(50)
            self.metodoDirecionamento = self.randomDirection

    def modoNormal(self):
        self.setSpeed(100)
        self.metodoDirecionamento = self.direcaoChegada
        self.NoCasa.rejeitaAcesso(BAIXO, self)




class Bafao(Fantasma):
    def __init__(self, no, pacman=None, bafao=None):
        Fantasma.__init__(self, no, pacman, bafao)
        self.nome = BAFAO
        self.cor = VERMELHO
        self.sprites = GhostSprites(self)


class Alonso(Fantasma):
    def __init__(self, no, pacman=None, bafao=None):
        Fantasma.__init__(self, no, pacman, bafao)
        self.nome = ALONSO
        self.cor = ROSA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, 0)

    def perseguir(self):
        self.goal = self.pacman.posicao + self.pacman.directions[self.pacman.direcao] * LARGURANO * 4


class Rogerio(Fantasma):
    def __init__(self, no, pacman=None, bafao=None):
        Fantasma.__init__(self, no, pacman, bafao)
        self.nome = ROGERIO
        self.cor = AZULCLARO
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, ALTURANO * NUMLINHA)

    def perseguir(self):
        vec1 = self.pacman.posicao + self.pacman.directions[self.pacman.direcao] * LARGURANO * 2
        vec2 = (vec1 - self.bafao.posicao) * 2
        self.goal = self.bafao.posicao + vec2


class Manga(Fantasma):
    def __init__(self, no, pacman=None, bafao=None):
        Fantasma.__init__(self, no, pacman, bafao)
        self.nome = MANGA
        self.cor = LARANJA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(0, ALTURANO * NUMLINHA)

    def perseguir(self):
        d = self.pacman.posicao - self.posicao
        ds = d.moduloQuadrado()
        if ds <= (LARGURANO * 8)**2:
            self.inicio()
        else:
            self.goal = self.pacman.posicao + self.pacman.directions[self.pacman.direcao] * LARGURANO * 4


class GrupoFantasma(object):
    def __init__(self, node, pacman):
        self.bafao = Bafao(node, pacman)
        self.alonso = Alonso(node, pacman)
        self.rogerio = Rogerio(node, pacman, self.bafao)
        self.manga = Manga(node, pacman)
        self.ghosts = [self.bafao, self.alonso, self.rogerio, self.manga]

    def __iter__(self):
        return iter(self.ghosts)

    def atualiza(self, dt):
        for ghost in self:
            ghost.atualiza(dt)

    def iniciaAleatorio(self):
        for ghost in self:
            ghost.comecaAleatorio()
        self.resetaPonto()

    def defineNoSpawn(self, node):
        for ghost in self:
            ghost.defineNoSpawn(node)

    def atualizaPontos(self):
        for ghost in self:
            ghost.pontos *= 2

    def resetaPonto(self):
        for ghost in self:
            ghost.pontos = 200

    def esconde(self):
        for ghost in self:
            ghost.visivel = False

    def mostra(self):
        for ghost in self:
            ghost.visivel = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def desenha(self, screen):
        for ghost in self:
            ghost.render(screen)

