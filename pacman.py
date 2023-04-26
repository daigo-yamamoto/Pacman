import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilho
from sprites import PacmanSprites


class Pacman(Andarilho):
    def __init__(self, no):
        Andarilho.__init__(self, no)
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

    def morre(self):
        self.vivo = False
        self.direcao = PARADO

    def atualiza(self, dt):
        self.sprites.update(dt)
        self.posicao += self.directions[self.direcao] * self.speed * dt
        direction = self.pegaChaveValida()
        if self.overshotTarget():
            self.no = self.target
            if self.no.neighbors[PORTAL] is not None:
                self.no = self.no.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.no:
                self.direcao = direction
            else:
                self.target = self.getNewTarget(self.direcao)

            if self.target is self.no:
                self.direcao = PARADO
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def pegaChaveValida(self):
        teclaApertada = pygame.key.get_pressed()
        if teclaApertada[K_UP]:
            return CIMA
        if teclaApertada[K_DOWN]:
            return BAIXO
        if teclaApertada[K_LEFT]:
            return ESQUERDA
        if teclaApertada[K_RIGHT]:
            return DIREITA
        return PARADO

    def comePontos(self, listaPontos):
        for ponto in listaPontos:
            if self.checaColisao(ponto):
                return ponto
        return None

    def colideFantasma(self, fantasma):
        return self.checaColisao(fantasma)

    def checaColisao(self, outro):
        d = self.posicao - outro.posicao
        dSquared = d.moduloQuadrado()
        rSquared = (self.collideRadius + outro.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False
