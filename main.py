import pygame, sys
from pygame.locals import *

import minijuegos.rapidroll
import minijuegos.snake
import minijuegos.reverseroll
from minijuegos import configuration
from minijuegos import pause


def main():

    def ejecutarJuego(juego):
        pantallaPausa = pause.Pause()
        enJuego = True

        while enJuego and juego.get_game_state()['playing']:
            juego.process()
            juego.display_frame()
            if juego.get_game_state()['pause']:
                pantallaPausa.display(juego.screen)
            enJuego = juego.get_game_state()['alive']

        return enJuego
    

    # inicio pygame y mis variables
    pygame.init()
    enJuego = True
    loopContador = 0

    # << acá iría el menú >>


    while enJuego:

        # << acá iría el pong >>
        # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
        # (ver getJugadorPosXY() en RapidRoll como referencia)
        # y tambien otro que devuelva una lista con las barras del pong


        if enJuego:
            rapidroll = minijuegos.rapidroll.RapidRoll((600, 40), loopContador)
            enJuego = ejecutarJuego(rapidroll)
        

        # << acá iría el de los ladrillos >>
        # tendría que pasarle al reverse roll la posicion de la bola que rompe los ladrillos al romper el ultimo
        # y la barra que maneja el jugador


        if enJuego:
            posJugadorAux = (rapidroll.getJugadorPosXY()[0], rapidroll.getJugadorPosXY()[1]-200) #LINEA PROVISIONAL!!!!!!
            reverseroll = minijuegos.reverseroll.ReverseRoll(posJugadorAux, loopContador)
            enJuego = ejecutarJuego(reverseroll)

        
        if enJuego:
            snake = minijuegos.snake.Game(loop=loopContador,ball_position=reverseroll.getJugadorPosXY(), player_pos=reverseroll.getUltimaPlataformaPosXY())
            while enJuego and not snake.get_game_state()["done"] and not snake.get_game_state()['win']:
               snake.process()
               snake.display_frame()
               enJuego = snake.get_game_state()["snake_is_alive"]
        

        loopContador += 1


    print("Fin del programa")


if __name__ == "__main__":
    main()