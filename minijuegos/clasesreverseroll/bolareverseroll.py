import pygame
from minijuegos import color, forma, configuration
from minijuegos.gameobject import *
from minijuegos.bola import *

class BolaReverseRoll(Bola):
    
    radio = forma.BOLA_RADIO

    def __init__(self, posXY, loop):

        super().__init__(posXY)

        self.vel = 8 + int(loop*0.5)

    def update(self):
        pass

    def setEnPlataforma(self, platPosY):
        self.rect.bottom = platPosY + 1

    def desplazamientoHorizontal(self, esDerecha):
        if esDerecha:
            self.rect.right += self.vel
            if self.rect.right > configuration.SCREEN_WIDTH:
                self.rect.right = configuration.SCREEN_WIDTH
        else:
            self.rect.left -= self.vel
            if self.rect.left < 0:
                self.rect.left = 0

    def desplazamientoVertical(self, esArriba):
        if esArriba:
            self.rect.top -= self.vel
            if self.rect.top < 0:
                self.rect.top = 0
        else:
            self.rect.bottom += self.vel
            if self.rect.bottom > configuration.SCREEN_HEIGHT:
                self.rect.bottom = configuration.SCREEN_HEIGHT