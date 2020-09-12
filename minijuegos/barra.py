import pygame
from minijuegos import color, forma, configuration
from random import randint
from minijuegos.gameobject import *

class Barra(GameObject):

    def __init__(self, esVertical, posXY, largo = None):

        super().__init__()

        self._esVertical = esVertical

        if self._esVertical:  
            self._ancho = forma.BARRA_LADO_MENOR
            if largo is not None:
                self._alto = largo
            else:
                self._alto = forma.BARRA_LADO_MAYOR
        else:
            if largo is not None:
                self._ancho = largo
            else:
                self._ancho = forma.BARRA_LADO_MAYOR
            self._alto = forma.BARRA_LADO_MENOR

        self._posX, self._posY = posXY

        self._rect = pygame.Rect(self._posX, self._posY, self._ancho, self._alto)

    def getLargo(self):
        largo = 0
        if esVertical:
            largo = self._alto
        else:
            largo = self._ancho
        return largo

    def update(self,*parametros):
        pass

    def draw(self, ventana):
        pygame.draw.rect(ventana, self._color, self._rect)