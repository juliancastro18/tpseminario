import pygame
from minijuegos.constantes import color, tamformas, configuration
from random import randint
from minijuegos.gameobject import *
from minijuegos.formas.barra import *

class Plataforma(Barra):

    def __init__(self, velY, largo = None, barra : Barra = None, colisionable = True, posicionFinal = 0):

        if barra is not None:
            super().__init__(barra._esVertical, (barra._posX, barra._posY), barra.getLargo())
        else:
            x = self.randomPosX(largo)
            y = configuration.SCREEN_HEIGHT+tamformas.BARRA_LADO_MENOR
            super().__init__(False, (x,y), largo)

        self._ultimaPlataforma = False
        self._distanciaNext = randint(80,200)
        self._velY = velY
        self._velInicial = velY #usado para plataforma que desacelera
        self._esColisionable = colisionable
        self._posicionFinal = posicionFinal

    def randomPosX(self, largo):
        cuartoDePantalla = int((configuration.SCREEN_WIDTH-largo)/4)
        posX = cuartoDePantalla * randint(0, 4)
        return posX


    def setPrimerPlataforma(self):
        self._rect.right = configuration.SCREEN_WIDTH
        self._rect.top = configuration.SCREEN_HEIGHT + 200

    def setUltimaPlataforma(self):
        self._rect.left = (configuration.SCREEN_WIDTH/2) - (self._ancho/2)
        self._posX = self._rect.left
        self._ultimaPlataforma = True
        self._setSinDistanciaNext()

    def setNoColisionable(self, plataformaAnterior):

        self._distanciaNext = 20
        if plataformaAnterior._ultimaPlataforma or plataformaAnterior._posX==515:
            self._posX = 40
        else:
            self._posX = plataformaAnterior._rect.right + 5

        self._rect = pygame.Rect(self._posX, self._posY, self._ancho, self._alto)

    def _setSinDistanciaNext(self):
        self._distanciaNext = 0

    def checkPosX(self, leftAnterior):
        while self._posX == leftAnterior:
            self._posX = self.randomPosX(self._ancho)
        self._rect = pygame.Rect(self._posX, self._posY, self._ancho, self._alto)


    def getTop(self):
        return self._rect.top

    def getBottom(self):
        return self._rect.bottom

    def getLeft(self):
        return self._rect.left

    def getUltimaPlataforma(self):
        return self._ultimaPlataforma

    def getRect(self):
        return self._rect

    def getDistanciaNext(self):
        return self._distanciaNext

    def getEsColisionable(self):
        return self._esColisionable


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

    def _desacelerar(self, posXFinal):
        distancia_comienzo_freno = 40
        comienzo_freno = posXFinal + distancia_comienzo_freno

        if self._rect.top <= comienzo_freno:
            falta_para_llegar = self._rect.top - posXFinal
            self._velY = self._velInicial * ( falta_para_llegar / distancia_comienzo_freno )


    def update(self, ventana):

        if not self._esColisionable or self._ultimaPlataforma and self._velY>0:
            self._desacelerar(self._posicionFinal)

        self._rect.top -= self._velY