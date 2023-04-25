import pygame
from vetor import Vetor2
from constantes import *
import numpy as np

class Pontos(object):
    def __init__(self, linha, coluna):
        self.nome = PONTOS
        self.posicao = Vetor2(coluna * LARGURA_NO, linha * ALTURA_NO)
        self.cor = BRANCO
        self.raio = int(4 * LARGURA_NO / 16)
        self.raio_colisao = int(4 * LARGURA_NO / 16)
        self.pontos = 10
        self.visivel = True

    def desenha(self, tela):
        if self.visivel:
            p = self.posicao.intTupla()
            pygame.draw.circle(tela, self.cor, p, self.raio)


class PontoPoder(Pontos):
    def __init__(self, linha, coluna):
        Pontos.__init__(self, linha, coluna)
        self.nome = PONTOSPODER
        self.raio = int(8 * LARGURA_NO / 16)
        self.pontos = 50
        self.tempo = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.tempo:
            self.visivel = not self.visivel
            self.timer = 0


class GrupoPontos(object):
    def __init__(self, arquivo_pontos):
        self.lista_pontos = []
        self.pontos_poder = []
        self.criaListaPontos(arquivo_pontos)
        self.num_pontos_comidos = 0

    def atualiza(self, dt):
        for ponto_poder in self.pontos_poder:
            ponto_poder.update(dt)

    def criaListaPontos(self, arquivo_pontos):
        dados = self.lerArquivoPontos(arquivo_pontos)
        for linha in range(dados.shape[0]):
            for coluna in range(dados.shape[1]):
                if dados[linha][coluna] in ['.', '+']:
                    self.lista_pontos.append(Pontos(linha, coluna))
                elif dados[linha][coluna] in ['P', 'p']:
                    pp = PontoPoder(linha, coluna)
                    self.lista_pontos.append(pp)
                    self.pontos_poder.append(pp)

    def lerArquivoPontos(self, arquivo_texto):
        return np.loadtxt(arquivo_texto, dtype='<U1')

    def vazio(self):
        if len(self.lista_pontos) == 0:
            return True
        return False

    def desenha(self, screen):
        for pellet in self.lista_pontos:
            pellet.desenha(screen)
