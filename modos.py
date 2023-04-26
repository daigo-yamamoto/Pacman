from constantes import *

class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    def atualiza(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is INICIO:
                self.chase()
            elif self.mode is PERSEGUIR:
                self.scatter()

    def scatter(self):
        self.mode = INICIO
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = PERSEGUIR
        self.time = 20
        self.timer = 0


class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def atualiza(self, dt):
        self.mainmode.atualiza(dt)
        if self.current is ALEATORIO:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.modoNormal()
                self.current = self.mainmode.mode
        elif self.current in [INICIO, PERSEGUIR]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawnNode:
                self.entity.modoNormal()
                self.current = self.mainmode.mode

    def setFreightMode(self):
        if self.current in [INICIO, PERSEGUIR]:
            self.timer = 0
            self.time = 7
            self.current = ALEATORIO
        elif self.current is ALEATORIO:
            self.timer = 0

    def setSpawnMode(self):
        if self.current is ALEATORIO:
            self.current = SPAWN