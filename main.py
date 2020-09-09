import pygame, sys
from pygame.locals import *

import minijuegos.rapidroll
import minijuegos.snake
from minijuegos import configuration


def main():
    
    pygame.init()
    enJuego = True
    
    while enJuego:

        # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
        # y tambien otro que devuelva una lista con las barras del pong
        rapidroll = minijuegos.rapidroll.RapidRoll((configuration.SCREEN_WIDTH-50, 40))
        while rapidroll.get_game_state()['alive'] and rapidroll.get_game_state()['playing']:
            rapidroll.process()
            rapidroll.display_frame()
            
        snake = minijuegos.snake.Game()
        #snake.primerComida(rapidroll.getBola())
        while not snake.get_game_state()["done"] and snake.get_game_state()["snake_is_alive"]:
           snake.process()
           snake.display_frame()

        enJuego = rapidroll.get_game_state()['alive'] and snake.get_game_state()['snake_is_alive'] # etc etc

    print("Fin del programa")

if __name__ == "__main__":
    main()