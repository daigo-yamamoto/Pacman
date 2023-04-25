import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *

class Pacman(object):
    def __init__(self, no):
        self.nome = PACMAN
        self.direcoes = {PARADO:Vetor2(), CIMA:Vetor2(0,-1), BAIXO:Vetor2(0,1), ESQUERDA:Vetor2(-1,0), DIREITA:Vetor2(1,0)}
        self.direcao = PARADO
        self.velocidade = 100
        self.raio = 10
        self.cor = AMARELO
        self.no = no
        self.definePosicao()

    def definePosicao(self):
        self.posicao = self.no.posicao.copia()

    def atualiza(self, dt):
        direcao = self.getTeclaValida()
        self.direcao = direcao
        self.no = self.pegaNovoAlvo(direcao)
        self.definePosicao()

    def direcaoValida(self, direcao):
        if direcao is not PARADO:
            if self.no.vizinhos[direcao] is not None:
                return True
        return False

    def pegaNovoAlvo(self, direcao):
        if self.direcaoValida(direcao):
            return self.no.vizinhos[direcao]
        return self.no

    def getTeclaValida(self):
        tecla_pessionada = pygame.key.get_pressed()
        if tecla_pessionada[K_UP]:
            return CIMA
        if tecla_pessionada[K_DOWN]:
            return BAIXO
        if tecla_pessionada[K_LEFT]:
            return ESQUERDA
        if tecla_pessionada[K_RIGHT]:
            return DIREITA
        return PARADO

    def render(self, tela):
        p = self.posicao.intTupla()
        pygame.draw.circle(tela, (255, 0, 0), p, self.raio)
