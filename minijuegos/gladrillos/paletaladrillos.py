import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.barra import *

class Paleta(Barra):
    
    #CONSTRUCTOR
    def __init__(self, posXY):
        
        super().__init__(False, posXY, 120)
        
        self.centro= self._posX + self._ancho/2
        self.izq= False
        self.der= False
    
    #METODOS

    def update(self, esDerecha):         
        if esDerecha:
            self._rect.right += 10
            if self._rect.right > configuration.SCREEN_WIDTH:
                self._rect.right = configuration.SCREEN_WIDTH
        else:
            self._rect.left -= 10
            if self._rect.left < 0:
                self._rect.left = 0
        
        self.centro= self._posX + self._ancho/2