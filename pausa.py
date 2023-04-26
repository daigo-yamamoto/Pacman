class Pausa(object):
    def __init__(self, pausado=False):
        self.pausado = pausado
        self.timer = 0
        self.tempoPausa = None
        self.func = None

    def atualiza(self, dt):
        if self.tempoPausa is not None:
            self.timer += dt
            if self.timer >= self.tempoPausa:
                self.timer = 0
                self.pausado = False
                self.tempoPausa = None
                return self.func
        return None

    def setPause(self, playerPaused=False, tempoPausa=None, func=None):
        self.timer = 0
        self.func = func
        self.tempoPausa = tempoPausa
        self.flip()

    def flip(self):
        self.pausado = not self.pausado
