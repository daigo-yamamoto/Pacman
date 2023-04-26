import pygame
from pygame.locals import *
from constantes import *
from pacman import Pacman
from no import GrupoNo
from pontos import GrupoPontos
from fantasma import GrupoFantasma
from fruta import Fruta
from pausa import Pausa
from sprites import LifeSprites
from sprites import MazeSprites


class GameController(object):
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.tela_fundo = None
        self.tempo = pygame.time.Clock()
        self.fruta = None
        self.pausa = Pausa(True)
        self.vidas = 5
        self.lifesprites = LifeSprites(self.vidas)

    def restartGame(self):
        self.vidas = 5
        self.pausa.pausado = True
        self.fruta = None
        self.comecaJogo()
        self.lifesprites.resetLives(self.vidas)

    def resetLevel(self):
        self.pausa.paused = True
        self.pacman.reset()
        self.fantasmas.reset()
        self.fruta = None

    def setTelaFundo(self):
        self.tela_fundo = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.tela_fundo.fill(PRETO)

    def comecaJogo(self):
        self.setTelaFundo()
        self.mazesprites = MazeSprites("mapa.txt", "mapa_rotacionado.txt")
        self.tela_fundo = self.mazesprites.constructBackground(self.tela_fundo, 0)
        self.no = GrupoNo("mapa.txt")
        homekey = self.no.createHomeNodes(11.5, 14)
        self.no.conectaNoCasa(homekey, (12, 14), ESQUERDA)
        self.no.conectaNoCasa(homekey, (15, 14), DIREITA)
        self.pacman = Pacman(self.no.pegaNoTiles(15, 26))
        self.pontos = GrupoPontos("mapa.txt")
        self.fantasmas = GrupoFantasma(self.no.pegaNoInicial(), self.pacman)

        self.fantasmas.bafao.setStartNode(self.no.pegaNoTiles(2 + 11.5, 0 + 14))
        self.fantasmas.alonso.setStartNode(self.no.pegaNoTiles(2 + 11.5, 3 + 14))
        self.fantasmas.rogerio.setStartNode(self.no.pegaNoTiles(0 + 11.5, 3 + 14))
        self.fantasmas.manga.setStartNode(self.no.pegaNoTiles(4 + 11.5, 3 + 14))
        self.fantasmas.defineNoSpawn(self.no.pegaNoTiles(2 + 11.5, 3 + 14))

        self.no.denyHomeAccess(self.pacman)
        self.no.denyHomeAccessList(self.fantasmas)
        self.no.denyAccessList(2 + 11.5, 3 + 14, ESQUERDA, self.fantasmas)
        self.no.denyAccessList(2 + 11.5, 3 + 14, DIREITA, self.fantasmas)
        self.fantasmas.alonso.no_inicial.denyAccess(DIREITA, self.fantasmas.alonso)
        self.fantasmas.manga.no_inicial.denyAccess(ESQUERDA, self.fantasmas.manga)
        self.no.denyAccessList(12, 14, CIMA, self.fantasmas)
        self.no.denyAccessList(15, 14, CIMA, self.fantasmas)
        self.no.denyAccessList(12, 26, CIMA, self.fantasmas)
        self.no.denyAccessList(15, 26, CIMA, self.fantasmas)

    def atualiza(self):
        dt = self.tempo.tick(30) / 1000.0
        self.pontos.atualiza(dt)
        if not self.pausa.pausado:
            self.pacman.atualiza(dt)
            self.fantasmas.atualiza(dt)
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
                    if self.pacman.vivo:
                        self.pausa.setPause(playerPaused=True)
                        if not self.pausa.pausado:
                            self.showEntities()
                        else:
                            self.hideEntities()

    def checaEventoFantasma(self):
        for fantasma in self.fantasmas:
            if self.pacman.collideGhost(fantasma):
                if fantasma.modo.atual is ALEATORIO:
                    self.pacman.visible = False
                    fantasma.visible = False
                    self.pausa.setPause(tempoPausa=1, func=self.showEntities)
                    fantasma.comecaSpawn()
                    self.no.allowHomeAccess(fantasma)
                elif fantasma.modo.atual is not SPAWN:
                    if self.pacman.vivo:
                        self.vidas -= 1
                        self.lifesprites.removeImage()
                        self.pacman.morre()
                        self.fantasmas.esconde()
                        if self.vidas <= 0:
                            self.pausa.setPause(tempoPausa=3, func=self.restartGame)
                        else:
                            self.pausa.setPause(tempoPausa=3, func=self.resetLevel)

    def showEntities(self):
        self.pacman.visible = True
        self.fantasmas.mostra()

    def hideEntities(self):
        self.pacman.visible = False
        self.fantasmas.esconde()

    def desenha(self):
        self.tela.blit(self.tela_fundo, (0,0))
        self.pontos.desenha(self.tela)
        if self.fruta is not None:
            self.fruta.desenha(self.tela)
        self.pacman.desenha(self.tela)
        self.fantasmas.desenha(self.tela)

        for i in range(len(self.lifesprites.imagens)):
            x = self.lifesprites.imagens[i].get_width() * i
            y = ALTURA_TELA - self.lifesprites.imagens[i].get_height()
            self.tela.blit(self.lifesprites.imagens[i], (x, y))

        pygame.display.update()

    def checaEventoPontos(self):
        ponto = self.pacman.comePonto(self.pontos.lista_pontos)
        if ponto:
            self.pontos.num_pontos_comidos += 1
            if self.pontos.num_pontos_comidos == 30:
                self.fantasmas.alonso.no_inicial.allowAccess(DIREITA, self.fantasmas.alonso)
            if self.pontos.num_pontos_comidos == 70:
                self.fantasmas.manga.no_inicial.allowAccess(ESQUERDA, self.fantasmas.manga)
            self.pontos.lista_pontos.remove(ponto)
            if ponto.nome == PONTOSPODER:
                self.fantasmas.comecaAleatorio()


if __name__ == "__main__":
    jogo = GameController()
    jogo.comecaJogo()
    while True:
        jogo.atualiza()
