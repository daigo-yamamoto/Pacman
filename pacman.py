import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from andarilhos import Andarilhos

class Pacman(Andarilhos):
    def __init__(self, no):
        Andarilhos.__init__(self, no)
        self.nome = PACMAN
        self.cor = AMARELO
        self.direcao = ESQUERDA

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

    def comePonto(self, lista_pontos):
        for ponto in lista_pontos:
            if self.checaColisao(ponto):
                return ponto
        return None

    def collideGhost(self, ghost):
        return self.checaColisao(ghost)

    def checaColisao(self, other):
        d = self.posicao - other.posicao
        dSquared = d.distanciaQuadrado()
        rSquared = (self.raio_colisao + other.raio_colisao) ** 2
        if dSquared <= rSquared:
            return True
        return False
