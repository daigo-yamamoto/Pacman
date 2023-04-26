from constantes import *

class ModoPrincipal(object):
    def __init__(self):
        self.timer = 0
        self.salvar()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.tempo:
            if self.modo is INICIO:
                self.peseguir()
            elif self.modo is PERSEGUIR:
                self.salvar()

    def salvar(self):
        self.modo = INICIO
        self.tempo = 7
        self.timer = 0

    def peseguir(self):
        self.modo = PERSEGUIR
        self.tempo = 20
        self.timer = 0

class ModeController(object):
    def __init__(self, andarilho):
        self.timer = 0
        self.tempo = None
        self.modoPrincipal = ModoPrincipal()
        self.atual = self.modoPrincipal.modo
        self.andarilho = andarilho

    def atualiza(self, dt):
        self.modoPrincipal.update(dt)
        if self.atual is ALEATORIO:
            self.timer += dt
            if self.timer >= self.tempo:
                self.tempo = None
                self.andarilho.normalMode()
                self.atual = self.modoPrincipal.modo
        elif self.atual in [INICIO, PERSEGUIR]:
            self.atual = self.modoPrincipal.modo

        if self.atual is SPAWN:
            if self.andarilho.no == self.andarilho.spawnNode:
                self.andarilho.normalMode()
                self.atual = self.modoPrincipal.modo

    def setSpawnMode(self):
        if self.atual is ALEATORIO:
            self.atual = SPAWN

    def defineModoAleatorio(self):
        if self.atual in [INICIO, PERSEGUIR]:
            self.timer = 0
            self.tempo = 7
            self.atual = ALEATORIO
        elif self.atual is ALEATORIO:
            self.timer = 0
