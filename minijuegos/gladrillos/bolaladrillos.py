import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.bola import *

class BolaLadrillos(Bola):
    #CONSTRUCTOR
    def __init__(self, posXY):

        super().__init__(posXY)
        self.vel_x = 0
        self.vel_y = 0

    #METODOS

    def update(self):

        #MOVIMIENTO de la bola
        self.posX += self.vel_x
        self.posY += self.vel_y
        self.rect.x = self.posX
        self.rect.y = self.posY

        if self.rect.left < 0 or self.rect.right > configuration.SCREEN_WIDTH:
                self.vel_x *= -1

        if self.rect.top<=0:
            self.vel_y *= -1

        #FIN DE JUEGO cuando la bola sale por abajo
        if self.rect.top > configuration.SCREEN_HEIGHT:
            return False

        return True