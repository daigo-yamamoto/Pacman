import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Entity
from modos import ModeController
from sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.nome = FANTASMA
        self.points = 200
        self.goal = Vetor2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def atualiza(self, dt):
        self.sprites.update(dt)
        self.mode.atualiza(dt)
        if self.mode.current is INICIO:
            self.inicio()
        elif self.mode.current is PERSEGUIR:
            self.perseguir()
        Entity.atualiza(self, dt)

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




class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.nome = BAFAO
        self.cor = VERMELHO
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.nome = ALONSO
        self.cor = ROSA
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, 0)

    def perseguir(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * LARGURANO * 4


class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.nome = ROGERIO
        self.cor = AZULCLARO
        self.sprites = GhostSprites(self)

    def inicio(self):
        self.goal = Vetor2(LARGURANO * NUMCOLUNA, ALTURANO * NUMLINHA)

    def perseguir(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * LARGURANO * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
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
        self.bafao = Blinky(node, pacman)
        self.alonso = Pinky(node, pacman)
        self.rogerio = Inky(node, pacman, self.bafao)
        self.manga = Clyde(node, pacman)
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
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

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

