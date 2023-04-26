import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from random import randint


class Andarilho(object):
    def __init__(self, node):
        self.nome = None
        self.directions = {CIMA: Vetor2(0, -1), BAIXO: Vetor2(0, 1),
                           ESQUERDA: Vetor2(-1, 0), DIREITA: Vetor2(1, 0), PARADO: Vetor2()}
        self.direcao = PARADO
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.cor = BRANCO
        self.visible = True
        self.disablePortal = False
        self.chegada = None
        self.metodoDirecionamento = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copia()

    def atualiza(self, dt):
        self.position += self.directions[self.direcao] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.metodoDirecionamento(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direcao = direction
            else:
                self.target = self.getNewTarget(self.direcao)

            self.setPosition()

    def validDirection(self, direction):
        if direction is not PARADO:
            if self.nome in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.moduloQuadrado()
            node2Self = vec2.moduloQuadrado()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direcao *= -1
        temp = self.node
        self.node = self.target
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
            vec = self.node.position + self.directions[direction] * LARGURANO - self.chegada
            distances.append(vec.moduloQuadrado())
        index = distances.index(min(distances))
        return directions[index]

    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direcao = PARADO
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        self.speed = speed * LARGURANO / 16

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vetor2(LARGURANO, ALTURANO) / 2
                p = self.position - adjust
                screen.blit(self.image, p.tupla())
            else:
                p = self.position.intTupla()
                pygame.draw.circle(screen, self.cor, p, self.radius)