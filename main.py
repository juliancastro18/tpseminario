import pygame, sys
from pygame.locals import *
from MiniJuegos.RapidRoll import *

#variables globales
anchoPantalla, altoPantalla = 640, 480
blanco = (255,255,255)
negro = (0,0,0)

pygame.init() # inicio pygame
ventana = pygame.display.set_mode((anchoPantalla, altoPantalla)) # creo la ventana con sus dimensiones 640x480
pygame.display.set_caption("TP Seminario de Lenguajes") # titulo de ventana


'''
while True:

    opcion = Inicio()

    if opcion == 1:
        
        enJuego = True
        while enJuego == True:

            if enJuego == True:
                enJuego, posXY, barrasPong = Pong(ventana)
            if enJuego == True:
                enJuego, posXY = RapidRoll(ventana, posXY, barrasPong)
            if enJuego == True:
                enJuego, posXY = Ladrillos(ventana, posXY)

        #evaluar puntuacion, pantalla de game over
'''

RapidRoll(anchoPantalla-50, 40, ventana)