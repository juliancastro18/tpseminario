import pygame
from MiniJuegos import color, forma, configuration
from MiniJuegos.GameObject import *

class Bola(GameObject):
    
    radio = forma.BOLA_RADIO

    def __init__(self, posXY : tuple):

        super().__init__()
        self.posX, self.posY = posXY
        self.rect = pygame.Rect(self.posX, self.posY, self.radio*2, self.radio*2) # rectángulo en el que se inscribe el círculo

    def draw(self, ventana):
        pygame.draw.circle(ventana, color.WHITE, self.rect.center, self.radio)

    def getPosicionXY(self):
        return self.rect.topleft