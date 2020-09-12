import pygame
from minijuegos import color, forma, configuration
from random import randint
from minijuegos.gameobject import *
from minijuegos.barra import *

class Plataforma(Barra):

    def __init__(self, velY, largo = None, barra : Barra = None):

        if barra is not None:
            super().__init__(barra._esVertical, (barra._posX, barra._posY), barra.getLargo())
        else:
            x = self.randomPosX(largo)
            y = configuration.SCREEN_HEIGHT+forma.BARRA_LADO_MENOR
            super().__init__(False, (x,y), largo)

        self._ultimaPlataforma = False
        self._distanciaNext = randint(80,200)
        self._velY = velY

    def randomPosX(self, largo):
        cuartoDePantalla = int((configuration.SCREEN_WIDTH-largo)/4)
        posX = cuartoDePantalla * randint(0, 4)
        return posX

    def setPrimerPlataforma(self):
        self._rect.right = configuration.SCREEN_WIDTH
        self._rect.top = configuration.SCREEN_HEIGHT + 200

    def setUltimaPlataforma(self):
        self._rect.left = (configuration.SCREEN_WIDTH/2) - (self._ancho/2)
        self._ultimaPlataforma = True
        self._distanciaNext = 200

    def setSinDistanciaNext(self):
        self.distanciaNext = 0

    def getTop(self):
        return self._rect.top

    def getBottom(self):
        return self._rect.bottom

    def getUltimaPlataforma(self):
        return self._ultimaPlataforma

    def permiteSiguientePlataforma(self):
        distanciaDelSuelo = self._posY - self._rect.top
        if distanciaDelSuelo > self._distanciaNext:
            return True
        else:
            return False

    def colisionSuperior(self, bola):
        if self._rect.colliderect(bola.rect):
            if not bola.rect.collidepoint(self._rect.bottomleft) and not bola.rect.collidepoint(self._rect.bottomright):
                return True
        return False

    def update(self, ventana):
        if self._ultimaPlataforma == True and self._rect.top < configuration.SCREEN_HEIGHT - 80:
            self._velY = 0
        self._rect.top -= self._velY