import pygame, sys
from pygame.locals import *

import MiniJuegos.RapidRoll
import MiniJuegos.Snake
from MiniJuegos import configuration


def main():
    
    pygame.init()
    enJuego = True
    rapidroll = MiniJuegos.RapidRoll.RapidRoll((configuration.SCREEN_WIDTH-50, 40))
    #snake = MiniJuegos.Snake.Game()
    
    while enJuego:

        rapidroll = MiniJuegos.RapidRoll.RapidRoll((configuration.SCREEN_WIDTH-50, 40))
        while rapidroll.get_game_state()['alive'] and rapidroll.get_game_state()['playing']:
            rapidroll.process()
            rapidroll.display_frame()

        #while not snake.get_game_state()["done"] and snake.get_game_state()["snake_is_alive"]:
        #    snake.process()
        #    snake.display_frame()

        enJuego = rapidroll.get_game_state()['alive'] # and skake.get_game_state()['snake_is_alive'] etc etc.

    print("Fin del programa")

if __name__ == "__main__":
    main()
