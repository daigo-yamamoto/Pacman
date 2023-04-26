import pygame
from vetor import Vetor2
from constantes import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vetor2(x, y)
        self.neighbors = {CIMA:None, BAIXO:None, ESQUERDA:None, DIREITA:None, PORTAL:None}
        self.access = {CIMA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       BAIXO:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       ESQUERDA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       DIREITA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA]}

    def denyAccess(self, direction, entity):
        if entity.nome in self.access[direction]:
            self.access[direction].remove(entity.nome)

    def allowAccess(self, direction, entity):
        if entity.nome not in self.access[direction]:
            self.access[direction].append(entity.nome)

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.tupla()
                line_end = self.neighbors[n].position.tupla()
                pygame.draw.line(screen, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(screen, VERMELHO, self.position.intTupla(), 12)


class GrupoNo(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * LARGURANO, y * ALTURANO


    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DIREITA] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[ESQUERDA] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[BAIXO] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[CIMA] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None


    def pegaNoInicial(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def pegaNoTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def denyAccess(self, col, row, direction, entity):
        node = self.pegaNoTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        node = self.pegaNoTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def allowAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.allowAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        self.nodesLUT[self.homekey].denyAccess(BAIXO, entity)

    def allowHomeAccess(self, entity):
        self.nodesLUT[self.homekey].allowAccess(BAIXO, entity)

    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.desenha(screen)