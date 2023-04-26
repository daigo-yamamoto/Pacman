from constantes import *

class ModoPrincipal(object):
    def __init__(self):
        self.timer = 0
        self.inicio()

    def atualiza(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.modo is INICIO:
                self.perseguir()
            elif self.modo is PERSEGUIR:
                self.inicio()

    def inicio(self):
        self.modo = INICIO
        self.time = 7
        self.timer = 0

    def perseguir(self):
        self.modo = PERSEGUIR
        self.time = 20
        self.timer = 0


class ModeController(object):
    def __init__(self, andarilho):
        self.timer = 0
        self.time = None
        self.mainmode = ModoPrincipal()
        self.atual = self.mainmode.modo
        self.andarilho = andarilho

    def atualiza(self, dt):
        self.mainmode.atualiza(dt)
        if self.atual is ALEATORIO:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.andarilho.modoNormal()
                self.atual = self.mainmode.modo
        elif self.atual in [INICIO, PERSEGUIR]:
            self.atual = self.mainmode.modo

        if self.atual is SPAWN:
            if self.andarilho.no == self.andarilho.NoSpawn:
                self.andarilho.modoNormal()
                self.atual = self.mainmode.modo

    def setFreightMode(self):
        if self.atual in [INICIO, PERSEGUIR]:
            self.timer = 0
            self.time = 7
            self.atual = ALEATORIO
        elif self.atual is ALEATORIO:
            self.timer = 0

    def setSpawnMode(self):
        if self.atual is ALEATORIO:
            self.atual = SPAWN