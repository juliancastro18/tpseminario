import pygame
from minijuegos.constantes import color, configuration
from minijuegos.formas.barra import *
from minijuegos.formas.bola import *

class Enemy(Barra):
    def __init__(self,posXY,largo):
        super().__init__(True, posXY, largo)
        self.speed = 1

    def update(self,bola):
        #si la bola esta en la pantalla
        if bola.rect.left > 0 or self._rect.right < configuration.SCREEN_WIDTH :
            #la sigue
            self._rect.bottom = bola.rect.bottom
            #el enemigo se detiene en la linea inferior
            if bola.rect.bottom >= configuration.SCREEN_HEIGHT :
                self._rect.bottom = configuration.SCREEN_HEIGHT







        