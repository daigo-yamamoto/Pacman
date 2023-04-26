import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilho
from modos import ModeController
from sprites import GhostSprites

class Fantasma(Andarilho):
    def __init__(self, no, pacman=None, blinky=None):
        Andarilho.__init__(self, no)
        self.nome = FANTASMA
        self.pontos = 200
        self.goal = Vetor2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = no

    def reset(self):
        Andarilho.reset(self)
        self.pontos = 200
        self.directionMethod = self.goalDirection

    def atualiza(self, dt):
        self.sprites.update(dt)
        self.mode.atualiza(dt)
        if self.mode.current is INICIO:
            self.inicio()
        elif self.mode.current is PERSEGUIR:
            self.perseguir()
        Andarilho.atualiza(self, dt)

    def inicio(self):
        self.goal = Vetor2()

    def perseguir(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def comecaAleatorio(self):
        self.mode.setFreightMode()
        if self.mode.current == ALEATORIO:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def modoNormal(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(BAIXO, self)




class Bafao(Fantasma):
    def __init__(self, no, pacman=None, blinky=None):
        Fantasma.__init__(self, no, pacman, blinky)
        self.nome = BAFAO
        self.cor = VERMELHO
        self.sprites = GhostSprites(self)


class Alonso(Fantasma):
    def __init__(self, no, pacman=None, blinky=None):
        Fantasma.__init__(self, no, pacman, blinky)
        self.nome = ALONSO
        self.cor = ROSA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, 0)

    def perseguir(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * LARGURANO * 4


class Rogerio(Fantasma):
    def __init__(self, no, pacman=None, blinky=None):
        Fantasma.__init__(self, no, pacman, blinky)
        self.nome = ROGERIO
        self.cor = AZULCLARO
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, ALTURANO * NUMLINHA)

    def perseguir(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * LARGURANO * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Manga(Fantasma):
    def __init__(self, no, pacman=None, blinky=None):
        Fantasma.__init__(self, no, pacman, blinky)
        self.nome = MANGA
        self.cor = LARANJA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(0, ALTURANO * NUMLINHA)

    def perseguir(self):
        d = self.pacman.position - self.position
        ds = d.moduloQuadrado()
        if ds <= (LARGURANO * 8)**2:
            self.inicio()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * LARGURANO * 4


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

    def startFreight(self):
        for ghost in self:
            ghost.comecaAleatorio()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.pontos *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.pontos = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

