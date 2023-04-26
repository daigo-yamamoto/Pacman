import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilho
from sprites import PacmanSprites


class Pacman(Andarilho):
    def __init__(self, node):
        Andarilho.__init__(self, node)
        self.nome = PACMAN
        self.cor = AMARELO
        self.direcao = ESQUERDA
        self.setBetweenNodes(ESQUERDA)
        self.vivo = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        Andarilho.reset(self)
        self.direcao = ESQUERDA
        self.setBetweenNodes(ESQUERDA)
        self.vivo = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.vivo = False
        self.direcao = PARADO

    def atualiza(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direcao] * self.speed * dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direcao = direction
            else:
                self.target = self.getNewTarget(self.direcao)

            if self.target is self.node:
                self.direcao = PARADO
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return CIMA
        if key_pressed[K_DOWN]:
            return BAIXO
        if key_pressed[K_LEFT]:
            return ESQUERDA
        if key_pressed[K_RIGHT]:
            return DIREITA
        return PARADO

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.moduloQuadrado()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False
