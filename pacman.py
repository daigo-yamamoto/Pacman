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
        self.alvo = no
        self.raio_colisao = 5

    def definePosicao(self):
        self.posicao = self.no.posicao.copia()

    def atualiza(self, dt):
        self.posicao += self.direcoes[self.direcao] * self.velocidade * dt
        direcao = self.getTeclaValida()

        if self.ultrapassouAlvo():
            self.no = self.alvo
            self.alvo = self.pegaNovoAlvo(direcao)
            if self.alvo is not self.no:
                self.direcao = direcao
            else:
                self.alvo = self.pegaNovoAlvo(self.direcao)
            if self.alvo is self.no:
                self.direcao = PARADO
            self.definePosicao()
        else:
            if self.direcaoOposta(direcao):
                self.direcaoReversa()

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

    def desenha(self, tela):
        p = self.posicao.intTupla()
        pygame.draw.circle(tela, AMARELO, p, self.raio)

    def ultrapassouAlvo(self):
        if self.alvo is not None:
            vec1 = self.alvo.posicao - self.no.posicao
            vec2 = self.posicao - self.no.posicao
            no2alvo = vec1.distanciaQuadrado()
            no2self = vec2.distanciaQuadrado()
            return no2self >= no2alvo
        return False

    def direcaoReversa(self):
        self.direcao *= -1
        temp = self.no
        self.no = self.alvo
        self.alvo = temp

    def direcaoOposta(self, direcao):
        if direcao is not PARADO:
            if direcao == self.direcao * -1:
                return True
        return False

    def comePonto(self, lista_pontos):
        for ponto in lista_pontos:
            d = self.posicao - ponto.posicao
            dQuadrado = d.distanciaQuadrado()
            rQuadrado = (ponto.raio + self.raio_colisao) ** 2
            if dQuadrado <= rQuadrado:
                return ponto
        return None
