import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.barra import *

class Tablero(Barra):
    def __init__(self, listaBarras : Barra):

        super().__init__(False, listaBarras[0].getPosXY, listaBarras[0].getLargo)
        self.tablero = listaBarras


    def dibujar(self):
        for i in range(3):
            for j in range(4):
                if self.tablero[i][j] != 0:
                    pygame.draw.rect(self.ventana, WHITE, (j*150, i*15, 149, 14))