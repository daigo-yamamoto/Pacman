import pygame
from vetor import Vetor2
from constantes import *
import numpy as np

class No(object):
    def __init__(self, x, y):
        self.posicao = Vetor2(x, y)
        self.neighbors = {CIMA:None, BAIXO:None, ESQUERDA:None, DIREITA:None, PORTAL:None}
        self.acesso = {CIMA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       BAIXO:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       ESQUERDA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       DIREITA:[PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA]}

    def rejeitaAcesso(self, direcao, andarilho):
        if andarilho.nome in self.acesso[direcao]:
            self.acesso[direcao].remove(andarilho.nome)

    def aceitaAcesso(self, direcao, andarilho):
        if andarilho.nome not in self.acesso[direcao]:
            self.acesso[direcao].append(andarilho.nome)

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.posicao.tupla()
                line_end = self.neighbors[n].posicao.tupla()
                pygame.draw.line(screen, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(screen, VERMELHO, self.posicao.intTupla(), 12)


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
        for linha in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[linha][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, linha+yoffset)
                    self.nodesLUT[(x, y)] = No(x, y)

    def constructKey(self, x, y):
        return x * LARGURANO, y * ALTURANO


    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for linha in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[linha][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, linha+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, linha+yoffset)
                        self.nodesLUT[key].neighbors[DIREITA] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[ESQUERDA] = self.nodesLUT[key]
                        key = otherkey
                elif data[linha][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for linha in list(range(dataT.shape[1])):
                if dataT[col][linha] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, linha+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, linha+yoffset)
                        self.nodesLUT[key].neighbors[BAIXO] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[CIMA] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][linha] not in self.pathSymbols:
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

    def pegaNoTiles(self, col, linha):
        x, y = self.constructKey(col, linha)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def rejeitaAcesso(self, col, linha, direcao, andarilho):
        node = self.pegaNoTiles(col, linha)
        if node is not None:
            node.rejeitaAcesso(direcao, andarilho)

    def aceitaAcesso(self, col, linha, direcao, andarilho):
        no = self.pegaNoTiles(col, linha)
        if no is not None:
            no.aceitaAcesso(direcao, andarilho)

    def listaAcessoRejeitado(self, col, linha, direcao, andarilhos):
        for andarilho in andarilhos:
            self.rejeitaAcesso(col, linha, direcao, andarilho)

    def ListaAcessoAceito(self, col, linha, direction, andarilhos):
        for andarilho in andarilhos:
            self.aceitaAcesso(col, linha, direction, andarilho)

    def rejeitaAcessoCasa(self, andarilho):
        self.nodesLUT[self.homekey].rejeitaAcesso(BAIXO, andarilho)

    def aceitaAcessoCasa(self, andarilho):
        self.nodesLUT[self.homekey].aceitaAcesso(BAIXO, andarilho)

    def listaAcessoRejeitadoCasa(self, andarilhos):
        for andarilho in andarilhos:
            self.rejeitaAcessoCasa(andarilho)

    def listaAcessoAceitoCasa(self, andarilhos):
        for andarilho in andarilhos:
            self.aceitaAcessoCasa(andarilho)

    def desenha(self, tela):
        for no in self.nodesLUT.values():
            no.desenha(tela)
