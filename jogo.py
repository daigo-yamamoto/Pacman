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
        self.telaFundo = None
        self.telaFundoNorm = None
        self.telaFundoFlash = None
        self.tempo = pygame.time.Clock()
        self.fruta = None
        self.pausa = Pausa(True)
        self.vidas = 1
        self.pontuacao = 0

        self.lifesprites = LifeSprites(self.vidas)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.NoFruta = None

    def definePlanoFundo(self):
        self.telaFundoNorm = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.telaFundoNorm.fill(PRETO)
        self.telaFundoFlash = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.telaFundoFlash.fill(PRETO)
        self.telaFundoNorm = self.mazesprites.constructBackground(self.telaFundoNorm, 3)
        self.telaFundoFlash = self.mazesprites.constructBackground(self.telaFundoFlash, 5)
        self.flashBG = False
        self.telaFundo = self.telaFundoNorm

    def ImiciaJogo(self):
        self.mazesprites = MazeSprites("mapa.txt", "mapa_rotacionado.txt")
        self.definePlanoFundo()
        self.no = GrupoNo("mapa.txt")
        homekey = self.no.createHomeNodes(11.5, 14)
        self.no.connectHomeNodes(homekey, (12, 14), ESQUERDA)
        self.no.connectHomeNodes(homekey, (15, 14), DIREITA)
        self.pacman = Pacman(self.no.pegaNoTiles(15, 26))
        self.pontos = GrupoPontos("mapa.txt")

        self.fantasmas = GrupoFantasma(self.no.pegaNoInicial(), self.pacman)
        self.fantasmas.bafao.selecionaNoInicial(self.no.pegaNoTiles(2 + 11.5, 0 + 14))
        self.fantasmas.alonso.selecionaNoInicial(self.no.pegaNoTiles(2 + 11.5, 3 + 14))
        self.fantasmas.rogerio.selecionaNoInicial(self.no.pegaNoTiles(0 + 11.5, 3 + 14))
        self.fantasmas.manga.selecionaNoInicial(self.no.pegaNoTiles(4 + 11.5, 3 + 14))
        self.fantasmas.defineNoSpawn(self.no.pegaNoTiles(2 + 11.5, 3 + 14))

        self.no.rejeitaAcessoCasa(self.pacman)
        self.no.listaAcessoRejeitadoCasa(self.fantasmas)
        self.no.listaAcessoRejeitado(2 + 11.5, 3 + 14, ESQUERDA, self.fantasmas)
        self.no.listaAcessoRejeitado(2 + 11.5, 3 + 14, DIREITA, self.fantasmas)
        self.fantasmas.rogerio.startNode.rejeitaAcesso(DIREITA, self.fantasmas.rogerio)
        self.fantasmas.manga.startNode.rejeitaAcesso(ESQUERDA, self.fantasmas.manga)
        self.no.listaAcessoRejeitado(12, 14, CIMA, self.fantasmas)
        self.no.listaAcessoRejeitado(15, 14, CIMA, self.fantasmas)
        self.no.listaAcessoRejeitado(12, 26, CIMA, self.fantasmas)
        self.no.listaAcessoRejeitado(15, 26, CIMA, self.fantasmas)

    def atualiza(self):
        dt = self.tempo.tick(30) / 1000.0
        self.pontos.atualiza(dt)
        if not self.pausa.paused:
            self.fantasmas.atualiza(dt)
            if self.fruta is not None:
                self.fruta.atualiza(dt)
            self.checaEventoPontos()
            self.checaEventoFantasma()

        if self.pacman.vivo:
            if not self.pausa.paused:
                self.pacman.atualiza(dt)
        else:
            self.pacman.atualiza(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.telaFundo == self.telaFundoNorm:
                    self.telaFundo = self.telaFundoFlash
                else:
                    self.telaFundo = self.telaFundoNorm

        afterPauseMethod = self.pausa.atualiza(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.desenha()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.vivo:
                        self.pausa.setPause(playerPaused=True)
                        if not self.pausa.paused:
                            self.mostraAndarilhos()

    def checaEventoPontos(self):
        pontos = self.pacman.comePontos(self.pontos.listaPontos)
        if pontos:
            self.pontos.numPontosComidos += 1
            self.atualizaPontos(pontos.pontos)
            if self.pontos.numPontosComidos == 30:
                self.fantasmas.rogerio.startNode.aceitaAcesso(DIREITA, self.fantasmas.rogerio)
            if self.pontos.numPontosComidos == 70:
                self.fantasmas.manga.startNode.aceitaAcesso(ESQUERDA, self.fantasmas.manga)
            self.pontos.listaPontos.remove(pontos)
            if pontos.nome == PONTOPODER:
                self.fantasmas.iniciaAleatorio()
            if self.pontos.isEmpty():
                self.flashBG = True
                self.escondeAndarilhos()

    def checaEventoFantasma(self):
        for fantasma in self.fantasmas:
            if self.pacman.colideFantasma(fantasma):
                if fantasma.modo.atual is ALEATORIO:
                    self.pacman.visivel = False
                    fantasma.visivel = False
                    self.atualizaPontos(fantasma.pontos)
                    self.fantasmas.atualizaPontos()
                    self.pausa.setPause(pauseTime=1, func=self.mostraAndarilhos)
                    fantasma.comecaSpawn()
                    self.no.aceitaAcessoCasa(fantasma)
                elif fantasma.modo.atual is not SPAWN:
                    if self.pacman.vivo:
                        self.vidas -= 1
                        self.lifesprites.removeImage()
                        self.pacman.morre()
                        self.fantasmas.esconde()
                        if self.vidas <= 0:
                            self.pausa.setPause(pauseTime=3, func=self.restartGame)

    def mostraAndarilhos(self):
        self.pacman.visivel = True
        self.fantasmas.mostra()

    def escondeAndarilhos(self):
        self.pacman.visivel = False
        self.fantasmas.esconde()

    def restartGame(self):
        self.vidas = 5
        self.pausa.paused = True
        self.fruta = None
        self.ImiciaJogo()
        self.pontuacao = 0

        self.lifesprites.resetLives(self.vidas)
        self.fruitCaptured = []

    def atualizaPontos(self, points):
        self.pontuacao += points

    def desenha(self):
        self.tela.blit(self.telaFundo, (0, 0))
        self.pontos.desenha(self.tela)
        if self.fruta is not None:
            self.fruta.desenha(self.tela)
        self.pacman.render(self.tela)
        self.fantasmas.desenha(self.tela)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = ALTURATELA - self.lifesprites.images[i].get_height()
            self.tela.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = LARGURATELA - self.fruitCaptured[i].get_width() * (i + 1)
            y = ALTURATELA - self.fruitCaptured[i].get_height()
            self.tela.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.ImiciaJogo()
    while True:
        game.atualiza()
