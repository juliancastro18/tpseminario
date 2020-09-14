import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.bola import *

class BolaRapidRoll(Bola):

    def __init__(self, posXY, loop):

        super().__init__(posXY)

        self.velYInicial = 0.5
        self.velY = 8 + int(loop*0.5)
        self.velX = 10 + int(loop*0.5)

    def update(self):
        # aceleracion inicial
        if self.velYInicial < self.velY:
            self.rect.top += self.velYInicial
            self.velYInicial = self.velYInicial * 1.04
        else:
            self.rect.top += self.velY

        # si la bola no esta en la pantalla, se termina el juego
        if self.rect.bottom < 0 or self.rect.top > configuration.SCREEN_HEIGHT:
            return False

        return True

    def setEnPlataforma(self, platPosY):
        self.rect.bottom = platPosY + 1

    def desplazamientoHorizontal(self, esDerecha):
        if esDerecha:
            self.rect.right += self.velX
            if self.rect.right > configuration.SCREEN_WIDTH:
                self.rect.right = configuration.SCREEN_WIDTH
        else:
            self.rect.left -= self.velX
            if self.rect.left < 0:
                self.rect.left = 0