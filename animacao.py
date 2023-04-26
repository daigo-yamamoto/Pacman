from constantes import *


class Animacao(object):
    def __init__(self, frames=[], velocidade=20, loop=True):
        self.frames = frames
        self.frameAtual = 0
        self.velocidade = velocidade
        self.loop = loop
        self.dt = 0
        self.acabou = False

    def reset(self):
        self.frameAtual = 0
        self.acabou = False

    def atualiza(self, dt):
        if not self.acabou:
            self.nextFrame(dt)
        if self.frameAtual == len(self.frames):
            if self.loop:
                self.frameAtual = 0
            else:
                self.acabou = True
                self.frameAtual -= 1

        return self.frames[self.frameAtual]

    def nextFrame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.velocidade):
            self.frameAtual += 1
            self.dt = 0






