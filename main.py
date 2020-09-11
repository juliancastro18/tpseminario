import pygame, sys
from pygame.locals import *

import minijuegos.rapidroll
import minijuegos.snake
import minijuegos.reverseroll
from minijuegos import configuration


def main():
    
    pygame.init()
    enJuego = True
    
    while enJuego:

        # << acá iría el pong >>
        # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
        # (ver getJugadorPosXY() en RapidRoll como referencia)
        # y tambien otro que devuelva una lista con las barras del pong


        rapidroll = minijuegos.rapidroll.RapidRoll((configuration.SCREEN_WIDTH-50, 40))
        while enJuego and rapidroll.get_game_state()['playing']:
            rapidroll.process()
            rapidroll.display_frame()
            enJuego = rapidroll.get_game_state()['alive']
            

        # << acá iría el de los ladrillos >>


        reverseroll = minijuegos.reverseroll.ReverseRoll(rapidroll.getJugadorPosXY())
        while enJuego and reverseroll.get_game_state()['playing']:
            reverseroll.process()
            reverseroll.display_frame()
            enJuego = reverseroll.get_game_state()['alive']


        snake = minijuegos.snake.Game()
        #snake.primerComida(reverseroll.getJugadorPosXY())
        while enJuego and not snake.get_game_state()["done"]:
           snake.process()
           snake.display_frame()
           enJuego = snake.get_game_state()["snake_is_alive"]


    print("Fin del programa")


if __name__ == "__main__":
    main()