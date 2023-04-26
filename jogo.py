import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from no import GrupoNo
from pontos import GrupoPontos
from fantasma import GrupoFantasma
from fruta import Fruta
from pausa import Pausa


class GameController(object):
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.tela_fundo = None
        self.tempo = pygame.time.Clock()
        self.fruta = None
        self.pausa = Pausa(True)

    def setTelaFundo(self):
        self.tela_fundo = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.tela_fundo.fill(PRETO)

    def comecaJogo(self):
        self.setTelaFundo()
        self.no = GrupoNo("mapa.txt")
        homekey = self.no.createHomeNodes(11.5, 14)
        self.no.conectaNoCasa(homekey, (12, 14), ESQUERDA)
        self.no.conectaNoCasa(homekey, (15, 14), DIREITA)
        self.pacman = Pacman(self.no.pegaNoTiles(15, 26))
        self.pontos = GrupoPontos("mapa.txt")
        self.fantasma = GrupoFantasma(self.no.pegaNoInicial(), self.pacman)
        self.fantasma.bafao.setStartNode(self.no.pegaNoTiles(2 + 11.5, 0 + 14))
        self.fantasma.alonso.setStartNode(self.no.pegaNoTiles(2 + 11.5, 3 + 14))
        self.fantasma.rogerio.setStartNode(self.no.pegaNoTiles(0 + 11.5, 3 + 14))
        self.fantasma.manga.setStartNode(self.no.pegaNoTiles(4 + 11.5, 3 + 14))
        self.fantasma.defineNoSpawn(self.no.pegaNoTiles(2 + 11.5, 3 + 14))

    def atualiza(self):
        dt = self.tempo.tick(30) / 1000.0
        self.pontos.atualiza(dt)
        if not self.pausa.pausado:
            self.pacman.atualiza(dt)
            self.fantasma.atualiza(dt)
            if self.fruta is not None:
                self.fruta.atualiza(dt)
            self.checaEventoPontos()
            self.checaEventoFantasma()
            self.checkFruitEvents()
        metodoAposPausa = self.pausa.atualiza(dt)
        if metodoAposPausa is not None:
            metodoAposPausa()
        self.checaEvento()
        self.desenha()

    def checkFruitEvents(self):
        if self.pontos.num_pontos_comidos == 50 or self.pontos.num_pontos_comidos == 140:
            if self.fruta is None:
                self.fruta = Fruta(self.no.pegaNoTiles(9, 20))
        if self.fruta is not None:
            if self.pacman.checaColisao(self.fruta):
                self.fruta = None
            elif self.fruta.destruido:
                self.fruta = None

    def checaEvento(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_SPACE:
                    self.pausa.setPause(playerPaused=True)
                    if not self.pausa.pausado:
                        self.showEntities()
                    else:
                        self.hideEntities()

    def checaEventoFantasma(self):
        for fantasma in self.fantasma:
            if self.pacman.collideGhost(fantasma):
                if fantasma.modo.atual is ALEATORIO:
                    self.pacman.visible = False
                    fantasma.visible = False
                    self.pausa.setPause(tempoPausa=1, func=self.showEntities)
                    fantasma.comecaSpawn()

    def showEntities(self):
        self.pacman.visible = True
        self.fantasma.mostra()

    def hideEntities(self):
        self.pacman.visible = False
        self.fantasma.esconde()

    def desenha(self):
        self.tela.blit(self.tela_fundo, (0,0))
        self.no.desenha(self.tela)
        self.pontos.desenha(self.tela)
        if self.fruta is not None:
            self.fruta.desenha(self.tela)
        self.pacman.desenha(self.tela)
        self.fantasma.desenha(self.tela)
        pygame.display.update()

    def checaEventoPontos(self):
        ponto = self.pacman.comePonto(self.pontos.lista_pontos)
        if ponto:
            self.pontos.num_pontos_comidos += 1
            self.pontos.lista_pontos.remove(ponto)
            if ponto.nome == PONTOSPODER:
                self.fantasma.comecaAleatorio()

if __name__ == "__main__":
    jogo = GameController()
    jogo.comecaJogo()
    while True:
        jogo.atualiza()
