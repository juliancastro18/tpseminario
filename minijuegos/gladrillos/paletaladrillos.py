import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.barra import *

class Paleta(Barra):
    
    #CONSTRUCTOR
    def __init__(self, posXY, largo, vel):
        
        super().__init__(False, posXY, largo)

        self.centro= self._posX + self._ancho/2
        self.izq= False
        self.der= False
        self.vel= vel
    
    #METODOS

    def update(self, esDerecha):         
        if esDerecha:
            self._rect.right += self.vel
            if self._rect.right > configuration.SCREEN_WIDTH:
                self._rect.right = configuration.SCREEN_WIDTH
        else:
            self._rect.left -= self.vel
            if self._rect.left < 0:
                self._rect.left = 0
                
        self._posX, self._posY = self._rect.topleft
