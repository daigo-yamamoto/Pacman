import pygame
import numpy as np
from vetor import Vetor2
from constantes import *

class No(object):
    def __init__(self, x, y):
        self.posicao = Vetor2(x, y)
        self.vizinhos = {CIMA: None, BAIXO: None, ESQUERDA: None, DIREITA: None}
        self.access = {CIMA: [PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       BAIXO: [PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       ESQUERDA: [PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA],
                       DIREITA: [PACMAN, BAFAO, ALONSO, ROGERIO, MANGA, FRUTA]}

    def denyAccess(self, direcao, andarilho):
        if andarilho.nome in self.access[direcao]:
            self.access[direcao].remove(andarilho.nome)

    def allowAccess(self, direcao, andarilho):
        if andarilho.nome not in self.access[direcao]:
            self.access[direcao].append(andarilho.nome)

    def desenha(self, tela):
        for n in self.vizinhos.keys():
            if self.vizinhos[n] is not None:
                line_start = self.posicao.tupla()
                line_end = self.vizinhos[n].posicao.tupla()
                pygame.draw.line(tela, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(tela, VERMELHO, self.posicao.intTupla(), 12)

class GrupoNo(object):
    def __init__(self, nivel):
        self.nivel = nivel
        self.dicionarioNo = {}
        self.simboloNo = ['+', 'P', 'n']
        self.simboloCaminho = ['.', '-', '|', 'p']
        data = self.leituraMapa(nivel)
        self.criarTabelaNo(data)
        self.conectaHorizontal(data)
        self.conectaVertical(data)
        self.homekey = None

    def leituraMapa(self, arquivo_texto):
        return np.loadtxt(arquivo_texto, dtype='<U1')

    def criarTabelaNo(self, dados, xoffset=0, yoffset=0):
        for linha in list(range(dados.shape[0])):
            for coluna in list(range(dados.shape[1])):
                if dados[linha][coluna] in self.simboloNo:
                    x, y = self.constroiMapa(coluna+xoffset, linha+yoffset)
                    self.dicionarioNo[(x, y)] = No(x, y)

    def constroiMapa(self, x, y):
        return x*ALTURA_NO, y*LARGURA_NO

    def conectaHorizontal(self, dados, xoffset=0, yoffset=0):
        for linha in list(range(dados.shape[0])):
            chave = None
            for coluna in list(range(dados.shape[1])):
                if dados[linha][coluna] in self.simboloNo:
                    if chave is None:
                        chave = self.constroiMapa(coluna + xoffset, linha + yoffset)
                    else:
                        outra_chave = self.constroiMapa(coluna + xoffset, linha + yoffset)
                        self.dicionarioNo[chave].vizinhos[DIREITA] = self.dicionarioNo[outra_chave]
                        self.dicionarioNo[outra_chave].vizinhos[ESQUERDA] = self.dicionarioNo[chave]
                        chave = outra_chave
                elif dados[linha][coluna] not in self.simboloCaminho:
                    chave = None

    def conectaVertical(self, dados, xoffset=0, yoffset=0):
        dadosT = dados.transpose()
        for coluna in list(range(dadosT.shape[0])):
            chave = None
            for linha in list(range(dadosT.shape[1])):
                if dadosT[coluna][linha] in self.simboloNo:
                    if chave is None:
                        chave = self.constroiMapa(coluna + xoffset, linha + yoffset)
                    else:
                        otherkey = self.constroiMapa(coluna + xoffset, linha + yoffset)
                        self.dicionarioNo[chave].vizinhos[BAIXO] = self.dicionarioNo[otherkey]
                        self.dicionarioNo[otherkey].vizinhos[CIMA] = self.dicionarioNo[chave]
                        chave = otherkey
                elif dadosT[coluna][linha] not in self.simboloCaminho:
                    chave = None

    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X', 'X', '+', 'X', 'X'],
                             ['X', 'X', '.', 'X', 'X'],
                             ['+', 'X', '.', 'X', '+'],
                             ['+', '.', '+', '.', '+'],
                             ['+', 'X', 'X', 'X', '+']])

        self.criarTabelaNo(homedata, xoffset, yoffset)
        self.conectaHorizontal(homedata, xoffset, yoffset)
        self.conectaVertical(homedata, xoffset, yoffset)
        self.homekey = self.constroiMapa(xoffset + 2, yoffset)
        return self.homekey

    def conectaNoCasa(self, homekey, otherkey, direction):
        key = self.constroiMapa(*otherkey)
        self.dicionarioNo[homekey].vizinhos[direction] = self.dicionarioNo[key]
        self.dicionarioNo[key].vizinhos[direction * -1] = self.dicionarioNo[homekey]

    def pegaNoPixel(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.dicionarioNo.keys():
            return self.dicionarioNo[(xpixel, ypixel)]
        return None

    def pegaNoTiles(self, col, row):
        x, y = self.constroiMapa(col, row)
        if (x, y) in self.dicionarioNo.keys():
            return self.dicionarioNo[(x, y)]
        return None

    def pegaNoInicial(self):
        nos = list(self.dicionarioNo.values())
        return nos[0]

    def desenha(self, tela):
        for no in self.dicionarioNo.values():
            no.desenha(tela)

    def denyAccess(self, coluna, linha, direcao, andarilho):
        no = self.pegaNoTiles(coluna, linha)
        if no is not None:
            no.denyAccess(direcao, andarilho)

    def allowAccess(self, coluna, linha, direcao, andarilho):
        no = self.pegaNoTiles(coluna, linha)
        if no is not None:
            no.allowAccess(direcao, andarilho)

    def denyAccessList(self, coluna, linha, direcao, andarilhos):
        for andarilho in andarilhos:
            self.denyAccess(coluna, linha, direcao, andarilho)

    def allowAccessList(self, coluna, linha, direcao, andarilhos):
        for andarilho in andarilhos:
            self.allowAccess(coluna, linha, direcao, andarilho)

    def denyHomeAccess(self, andarilho):
        self.dicionarioNo[self.homekey].denyAccess(BAIXO, andarilho)

    def allowHomeAccess(self, andarilho):
        self.dicionarioNo[self.homekey].allowAccess(BAIXO, andarilho)

    def denyHomeAccessList(self, andarilhos):
        for andarilho in andarilhos:
            self.denyHomeAccess(andarilho)

    def allowHomeAccessList(self, andarilhos):
        for andarilho in andarilhos:
            self.allowHomeAccess(andarilho)