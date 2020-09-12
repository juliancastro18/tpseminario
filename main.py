import pygame, sys
from pygame.locals import *

import minijuegos.rapidroll
import minijuegos.snake
import minijuegos.reverseroll
from minijuegos import configuration


def main():
    
    pygame.init()
    enJuego = True
    loopContador = 0
    
    while enJuego:

        # << acá iría el pong >>
        # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
        # (ver getJugadorPosXY() en RapidRoll como referencia)
        # y tambien otro que devuelva una lista con las barras del pong


        rapidroll = minijuegos.rapidroll.RapidRoll((configuration.SCREEN_WIDTH-50, 40), loopContador)
        while enJuego and rapidroll.get_game_state()['playing']:
            rapidroll.process()
            rapidroll.display_frame()
            enJuego = rapidroll.get_game_state()['alive']
            

        # << acá iría el de los ladrillos >>
        # tendría que pasarle al reverse roll la posicion de la bola que rompe los ladrillos al romper el ultimo
        # y la barra que maneja el jugador

        posJugadorAux = (rapidroll.getJugadorPosXY()[0], rapidroll.getJugadorPosXY()[1]-200) #LINEA PROVISIONAL
        reverseroll = minijuegos.reverseroll.ReverseRoll(posJugadorAux, loopContador)
        while enJuego and reverseroll.get_game_state()['playing']:
            reverseroll.process()
            reverseroll.display_frame()
            enJuego = reverseroll.get_game_state()['alive']


        snake = minijuegos.snake.Game(loop=loopContador,ball_position=reverseroll.getJugadorPosXY(), player_pos=(0,0))
        while enJuego and not snake.get_game_state()["done"]:
           snake.process()
           snake.display_frame()
           enJuego = snake.get_game_state()["snake_is_alive"]


        loopContador += 1


    print("Fin del programa")


if __name__ == "__main__":
    main()