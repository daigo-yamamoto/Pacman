import math

class Vetor2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.erro = 0.000001

    def __add__(self, outro_vetor):
        return Vetor2(self.x + outro_vetor.x, self.y + outro_vetor.y)

    def __sub__(self, outro_vetor):
        return Vetor2(self.x - outro_vetor.x, self.y - outro_vetor.y)

    def __neg__(self):
        return Vetor2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vetor2(self.x * scalar, self.y * scalar)

    def __div__(self, numero):
        if numero != 0:
            return Vetor2(self.x / float(numero), self.y / float(numero))
        return None

    def __truediv__(self, numero):
        return self.__div__(numero)

    def __eq__(self, numero):
        if abs(self.x - numero.x) < self.erro:
            if abs(self.y - numero.y) < self.erro:
                return True
        return False

    def moduloQuadrado(self):
        return self.x**2 + self.y**2

    def modulo(self):
        return math.sqrt(self.moduloQuadrado())

    def copia(self):
        return Vetor2(self.x, self.y)

    def tupla(self):
        return self.x, self.y

    def intTupla(self):
        return int(self.x), int(self.y)
