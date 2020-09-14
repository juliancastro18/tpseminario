import pygame, random
from minijuegos.constantes import configuration
from minijuegos.grapidroll.plataforma import *

class PlataformaMovil(Plataforma):

    def __init__(self, velY, largo = None):

        super().__init__(velY, largo)

        random_bit = random.getrandbits(1)
        self._esDerecha = bool(random_bit)
        self._velX = self._velY*2
        self._distanciaNext = randint(80,200)


    def update(self, ventana):

        # si la plataforma ya no se ve en pantalla horizontalmente
        # la hago aparecer del otro lado
        if self._rect.right < 0:
            self._rect.left = configuration.SCREEN_WIDTH
        elif self._rect.left > configuration.SCREEN_WIDTH:
            self._rect.right = 0

        # la muevo para el lado correspondiente
        if self._esDerecha:
            self._rect.right += self._velX
        else:
            self._rect.left -= self._velX

        super().update(ventana)