import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.barra import *

class Bloques(Barra):
    def __init__(self, ventana):
        self.ventana = ventana
        self.tablero = [[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]]

    def dibujar(self):
        for i in range(3):
            for j in range(4):
                if self.tablero[i][j] != 0:
                    pygame.draw.rect(self.ventana, WHITE, (j*150, i*15, 149, 14))