import pygame
from constantes import *
from pacman import *
from mapa import *

class Jogo():
    # Deve ter as coisas que para o jogo, como:
    # iniciar o pygame
    # Atualizar a tela
    # Checar eventos
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(TAMANHO_TELA, 1)
        self.tempo = pygame.time.Clock()

    def inicia_jogo(self):
        self.pacman = Pacman()
        self.mapa = Mapa(TAMANHO_TELA, self.pacman)
        self.mapa.adicionar_movivel(self.pacman)

    def atualiza(self):
        # Checar se o pacman ta vivo
        self.calcular_regras()
        self.desenha()
        self.checar_eventos()

    def checar_eventos(self):
        evento = pygame.event.get()
        self.mapa.processar_eventos(evento)
        self.pacman.processar_eventos(evento)

    def calcular_regras(self):
        self.pacman.calcular_regra()
        self.mapa.calcular_regra()

    def desenha(self):
        self.tela.fill(PRETO)
        self.mapa.desenha(self.tela)
        self.pacman.desenha(self.tela)
        pygame.display.update()
        pygame.time.delay(100)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.inicia_jogo()
    while True:
        jogo.atualiza()
