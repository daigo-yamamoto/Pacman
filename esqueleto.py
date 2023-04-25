import pygame
from pygame.locals import *
from vector import Vector2
from constantes import *
from random import randint

class Esqueleto(object):
    def __init__(self, node):
        self.nome = None
        self.direcoes = {CIMA: Vector2(0, -1), BAIXO: Vector2(0, 1),
                         ESQUERDA: Vector2(-1, 0), DIREITA: Vector2(1, 0), PARA: Vector2()}
        self.direction = PARA
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = BRANCO
        self.visible = True
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copia()

    def update(self, dt):
        self.position += self.direcoes[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirection(self, direction):
        if direction is not PARA:
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
            node2Target = vec1.distancia_quadrado()
            node2Self = vec2.distancia_quadrado()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not PARA:
            if direction == self.direction * -1:
                return True
        return False

    def validDirections(self):
        directions = []
        for key in [CIMA, BAIXO, ESQUERDA, DIREITA]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.direcoes[direction] * TAMANHO_NO - self.goal
            distances.append(vec.distancia_quadrado())
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
        self.direction = PARA
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        self.speed = speed * TAMANHO_NO / 16

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TAMANHO_NO, TAMANHO_NO) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.eh_int()
                pygame.draw.circle(screen, self.color, p, self.radius)
