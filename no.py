import pygame
from vetor import Vetor2
from constantes import *

class Node(object):
    def __init__(self, x, y):
        self.posicao = Vetor2(x, y)
        self.vizinhos = {CIMA: None, BAIXO: None, ESQUERDA: None, DIREITA: None}

    def render(self, tela):
        for n in self.vizinhos.keys():
            if self.vizinhos[n] is not None:
                line_start = self.posicao.tupla()
                line_end = self.vizinhos[n].posicao.tupla()
                pygame.draw.line(tela, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(tela, VERMELHO, self.posicao.intTupla(), 12)

class NodeGroup(object):
    def __init__(self):
        self.listaNo = []

    def setupTestNodes(self):
        nodeA = Node(80, 80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
        nodeA.vizinhos[DIREITA] = nodeB
        nodeA.vizinhos[BAIXO] = nodeC
        nodeB.vizinhos[ESQUERDA] = nodeA
        nodeB.vizinhos[BAIXO] = nodeD
        nodeC.vizinhos[CIMA] = nodeA
        nodeC.vizinhos[DIREITA] = nodeD
        nodeC.vizinhos[BAIXO] = nodeF
        nodeD.vizinhos[CIMA] = nodeB
        nodeD.vizinhos[ESQUERDA] = nodeC
        nodeD.vizinhos[DIREITA] = nodeE
        nodeE.vizinhos[ESQUERDA] = nodeD
        nodeE.vizinhos[BAIXO] = nodeG
        nodeF.vizinhos[CIMA] = nodeC
        nodeF.vizinhos[DIREITA] = nodeG
        nodeG.vizinhos[CIMA] = nodeE
        nodeG.vizinhos[ESQUERDA] = nodeF

        self.listaNo = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def render(self, tela):
        for node in self.listaNo:
            node.render(tela)
