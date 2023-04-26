import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from random import randint


class Andarilho(object):
    def __init__(self, no):
        self.nome = None
        self.directions = {CIMA: Vetor2(0, -1), BAIXO: Vetor2(0, 1),
                           ESQUERDA: Vetor2(-1, 0), DIREITA: Vetor2(1, 0), PARADO: Vetor2()}
        self.direcao = PARADO
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.cor = BRANCO
        self.visivel = True
        self.disablePortal = False
        self.chegada = None
        self.metodoDirecionamento = self.randomDirection
        self.selecionaNoInicial(no)
        self.image = None

    def setPosition(self):
        self.posicao = self.no.posicao.copia()

    def atualiza(self, dt):
        self.posicao += self.directions[self.direcao] * self.speed * dt

        if self.overshotTarget():
            self.no = self.target
            directions = self.validDirections()
            direction = self.metodoDirecionamento(directions)
            if not self.disablePortal:
                if self.no.neighbors[PORTAL] is not None:
                    self.no = self.no.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.no:
                self.direcao = direction
            else:
                self.target = self.getNewTarget(self.direcao)

            self.setPosition()

    def validDirection(self, direction):
        if direction is not PARADO:
            if self.nome in self.no.acesso[direction]:
                if self.no.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.no.neighbors[direction]
        return self.no

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.posicao - self.no.posicao
            vec2 = self.posicao - self.no.posicao
            node2Target = vec1.moduloQuadrado()
            node2Self = vec2.moduloQuadrado()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direcao *= -1
        temp = self.no
        self.no = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not PARADO:
            if direction == self.direcao * -1:
                return True
        return False

    def validDirections(self):
        directions = []
        for key in [CIMA, BAIXO, ESQUERDA, DIREITA]:
            if self.validDirection(key):
                if key != self.direcao * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direcao * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def direcaoChegada(self, directions):
        distances = []
        for direction in directions:
            vec = self.no.posicao + self.directions[direction] * LARGURANO - self.chegada
            distances.append(vec.moduloQuadrado())
        index = distances.index(min(distances))
        return directions[index]

    def selecionaNoInicial(self, no):
        self.no = no
        self.startNode = no
        self.target = no
        self.setPosition()

    def setBetweenNodes(self, direction):
        if self.no.neighbors[direction] is not None:
            self.target = self.no.neighbors[direction]
            self.posicao = (self.no.posicao + self.target.posicao) / 2.0

    def reset(self):
        self.selecionaNoInicial(self.startNode)
        self.direcao = PARADO
        self.speed = 100
        self.visivel = True

    def setSpeed(self, speed):
        self.speed = speed * LARGURANO / 16

    def render(self, screen):
        if self.visivel:
            if self.image is not None:
                adjust = Vetor2(LARGURANO, ALTURANO) / 2
                p = self.posicao - adjust
                screen.blit(self.image, p.tupla())
            else:
                p = self.posicao.intTupla()
                pygame.draw.circle(screen, self.cor, p, self.radius)