import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *

class Pacman(object):
    def __init__(self):
        self.nome = PACMAN
        self.posicao = Vetor2(200, 400)
        self.direcoes = {PARADO:Vetor2(), CIMA:Vetor2(0,-1), BAIXO:Vetor2(0,1), ESQUERDA:Vetor2(-1,0), DIREITA:Vetor2(1,0)}
        self.direcao = PARADO
        self.velocidade = 100
        self.raio = 10
        self.cor = AMARELO

    def atualiza(self, dt):
        self.posicao += self.direcoes[self.direcao] * self.velocidade * dt
        direcao = self.getTeclaValida()
        self.direcao = direcao

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
