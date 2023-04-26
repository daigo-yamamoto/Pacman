import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from no import GrupoNo
from pontos import GrupoPontos
from fantasma import Fantasma

class GameController(object):
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.tela_fundo = None
        self.tempo = pygame.time.Clock()

    def setTelaFundo(self):
        self.tela_fundo = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.tela_fundo.fill(PRETO)

    def comecaJogo(self):
        self.setTelaFundo()
        self.no = GrupoNo("mapa.txt")
        self.pacman = Pacman(self.no.pegaNoInicial())
        self.pontos = GrupoPontos("mapa.txt")
        self.fantasma = Fantasma(self.no.pegaNoInicial())

    def atualiza(self):
        dt = self.tempo.tick(30) / 1000.0
        self.pacman.atualiza(dt)
        self.fantasma.atualiza(dt)
        self.pontos.atualiza(dt)
        self.checaEventoPontos()
        self.checaEvento()
        self.desenha()

    def checaEvento(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                exit()

    def desenha(self):
        self.tela.blit(self.tela_fundo, (0,0))
        self.no.desenha(self.tela)
        self.pontos.desenha(self.tela)
        self.pacman.desenha(self.tela)
        self.fantasma.desenha(self.tela)
        pygame.display.update()

    def checaEventoPontos(self):
        pellet = self.pacman.comePonto(self.pontos.lista_pontos)
        if pellet:
            self.pontos.num_pontos_comidos += 1
            self.pontos.lista_pontos.remove(pellet)

if __name__ == "__main__":
    jogo = GameController()
    jogo.comecaJogo()
    while True:
        jogo.atualiza()
