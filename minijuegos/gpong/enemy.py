import pygame, random
from minijuegos.constantes import color, configuration
from minijuegos.formas.barra import *
from minijuegos.formas.bola import *

class Enemy(Barra):
    def __init__(self,posXY,largo,vel_bola):
        super().__init__(True, posXY, largo)
        self.speed = vel_bola
        self._distancia_reaccion = 110 + vel_bola #antes era 150

        self._siguiendo_bola = False
        self._offset = 0

    def update(self,bola):
        distancia_x = abs(self._rect.centerx - bola.rect.centerx)

        if distancia_x < self._distancia_reaccion or bola.recien_iniciada:
            if self._siguiendo_bola == False:
                self._nuevo_offset()
                self._siguiendo_bola = True

            #hago de la velocidad la distancia, al menos que esté lejos
            distancia_bola = abs(self._rect.centery + self._offset - bola.rect.centery)
            velocidad = self.speed
            if distancia_bola < velocidad:
                velocidad = distancia_bola

            #si la bola esta mas arriba que el centro de la paleta
            if self._rect.centery + self._offset < bola.rect.centery:
                #la sigue
                self._rect.top += velocidad
            elif self._rect.centery + self._offset > bola.rect.centery:
                self._rect.bottom -= velocidad

            #el enemigo se detiene en la linea inferior o superior
            if self._rect.bottom > configuration.SCREEN_HEIGHT:
                self._rect.bottom = configuration.SCREEN_HEIGHT
            elif self._rect.top < 0:
                self._rect.top = 0

        else:
            self._siguiendo_bola = False


    def _nuevo_offset(self):
        dist_offset = self.getLargo()/2 - 15
        self._offset = randint(-dist_offset, dist_offset)