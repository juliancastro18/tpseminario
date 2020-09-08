import pygame, sys
from pygame.locals import *

import MiniJuegos.RapidRoll
import MiniJuegos.Snake
from MiniJuegos import configuration

pygame.init() # inicio pygame
ventana = pygame.display.set_mode((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT)) # creo la ventana con sus dimensiones 640x480
pygame.display.set_caption("TP Seminario de Lenguajes") # titulo de ventana



enJuego, posicionXY = MiniJuegos.RapidRoll.RapidRoll(configuration.SCREEN_WIDTH-50, 40, ventana)
print("Juego terminado.\nGanaste: ",enJuego,"\nPosicion centro bola:",posicionXY)

'''
def main():
    
    pygame.init()
    myGame = MiniJuegos.Snake.Game()
    
    while not myGame.get_game_state()["done"] and myGame.get_game_state()["snake_is_alive"]:
        myGame.process()
        myGame.display_frame()


if __name__ == "__main__":
    main()
'''