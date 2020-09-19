import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *

class Bola(GameObject):
    
    radio = tamformas.BOLA_RADIO
    img_bola = pygame.image.load("data\\img\\bola.png")

    def __init__(self, posXY : tuple):

        super().__init__()
        self.posX, self.posY = posXY
        self.rect = pygame.Rect(self.posX, self.posY, self.radio*2, self.radio*2) # rectángulo en el que se inscribe el círculo

    @classmethod
    #pasando una clase hija, creo clase padre
    def new_from(cls, obj):
        if issubclass(obj.__class__, Barra):
            _new = cls((obj._posX, obj._posY))
            return _new
        else:
            raise TypeError('Se esperaba subclase de Barra, se obtuvo {}.'\
                                .format(type(obj)))

    def draw(self, ventana):
        ventana.blit(self.img_bola, self.rect.topleft)

    def getPosicionXY(self):
        return self.rect.topleft