import pygame
import math
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.bola import *

class BolaLadrillos(Bola):
    #CONSTRUCTOR
    def __init__(self, posXY, vel):

        super().__init__(posXY)
        self.vel = vel
        self.mov_x = 0
        self.mov_y = 0
        self.set_xy(math.pi/4) #angulo por defecto 45 grados

    #METODOS

    def update(self):

        #MOVIMIENTO de la bola
        self.posX += self.mov_x
        self.posY += self.mov_y
        self.rect.x = self.posX
        self.rect.y = self.posY

        if self.rect.left < 0:
            self.mov_x *= -1
            self.rect.left = 0

        if self.rect.right > configuration.SCREEN_WIDTH:
            self.mov_x *= -1
            self.rect.right = configuration.SCREEN_WIDTH

        if self.rect.top < 0:
            self.mov_y *= -1
            self.rect.top = 0

        #FIN DE JUEGO cuando la bola sale por abajo
        if self.rect.top > configuration.SCREEN_HEIGHT:
            return False

        return True


    def set_xy(self, angulo):
        self.mov_x = math.cos(angulo) * self.vel
        self.mov_y = math.sin(angulo) * self.vel