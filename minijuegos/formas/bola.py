import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *

class Bola(GameObject):
    
    radio = tamformas.BOLA_RADIO

    def __init__(self, posXY : tuple):

        super().__init__()
        self.posX, self.posY = posXY
        self.rect = pygame.Rect(self.posX, self.posY, self.radio*2, self.radio*2) # rectángulo en el que se inscribe el círculo

    def draw(self, ventana):
        pygame.draw.circle(ventana, color.WHITE, self.rect.center, self.radio)

    def getPosicionXY(self):
        return self.rect.topleft