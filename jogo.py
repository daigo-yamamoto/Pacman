# Colocar o game controller
# COlocar a main
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
        self.tela = pygame.display.set_mode(TAMANHO_TELA, 0)
        self.tempo = pygame.time.Clock()
        self.pacman = Pacman((200, 200))
        self.mapa = Mapa(TAMANHO_TELA, self.pacman)
        self.mapa.adicionar_movivel(self.pacman)

    def inicia_jogo(self):
        pass
    def atualiza(self):
        # Checar se o pacman ta vivo
        self.checar_eventos()
        self.desenha()

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
        self.mapa.processar_eventos(pygame.event.get())


    def desenha(self):
        self.pacman.desenha(self.tela)
        self.mapa.desenha(self.tela)
        pygame.display.update()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.inicia_jogo()
    while True:
        # Calculo de regras
        # Desenha
        # Evento
        jogo.atualiza()


