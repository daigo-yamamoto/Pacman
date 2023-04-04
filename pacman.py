import pygame
from esqueleto import *
from constantes import *
class Pacman():
    def __init__(self, posicao):
        self.cor = AMARELO
        self.posicao = posicao

    def desenha(self, tela):
        pygame.draw.circle(tela, AMARELO, self.posicao, TAMANHO_NO, 0)


