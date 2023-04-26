from constantes import *

class ModoPrincipal(object):
    def __init__(self):
        self.timer = 0
        self.salvar()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.tempo:
            if self.modo is SALVAR:
                self.peseguir()
            elif self.modo is PERSEGUIR:
                self.salvar()

    def salvar(self):
        self.modo = SALVAR
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

    def update(self, dt):
        self.modoPrincipal.update(dt)
        self.atual = self.modoPrincipal.modo
