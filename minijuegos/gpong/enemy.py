import pygame
from minijuegos.constantes import color, configuration
from minijuegos.formas.barra import *
from minijuegos.formas.bola import *

class Enemy(Barra):
    def __init__(self,posXY,largo):
        super().__init__(True, posXY, largo)
        self.speed = 10

    def update(self,bola):
        #hago de la velocidad la distancia, al menos que esté muy lejos
        distancia_bola = abs(self._rect.centery - bola.rect.centery)
        velocidad = self.speed
        if distancia_bola < velocidad:
            velocidad = distancia_bola

        #si la bola esta mas arriba que el centro de la paleta
        if self._rect.centery < bola.rect.centery:
            #la sigue
            self._rect.top += velocidad
        elif self._rect.centery > bola.rect.centery:
            self._rect.bottom -= velocidad

        #el enemigo se detiene en la linea inferior o superior
        if self._rect.bottom > configuration.SCREEN_HEIGHT:
            self._rect.bottom = configuration.SCREEN_HEIGHT
        elif self._rect.top < 0:
            self._rect.top = 0






        