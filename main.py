import pygame, sys
from pygame.locals import *

from minijuegos.grapidroll import rapidroll
from minijuegos.greverseroll import reverseroll
from minijuegos.gsnake import snake_game
from minijuegos.constantes import configuration
from minijuegos.meta import administrador
import ui.gameover.gameover

def main():

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init() # inicio pygame
    pygame.display.set_caption('5in1')
    icono = pygame.image.load("data\\img\\ico.png")
    pygame.display.set_icon(icono)



    while True: # loop infinito hasta que se cierre pygame

        admin = administrador.Administrador() # inicio el administrador de juegos

        # << acá iría el menú >>
        # opciones: comenzar, puntuaciones, controles, salir

        admin.iniciarCronometro() # comienzo a contar el tiempo transcurrido
        while admin.getEnJuego():

            admin.reproducirNuevoLoop()

            # << acá iría el pong >>
            # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
            # (ver getJugadorPosXY() en RapidRoll como referencia)
            # y tambien otro que devuelva una lista con las barras del pong


            rapid = rapidroll.RapidRoll((600, 40), admin.getLoopContador())
            admin.ejecutarJuego(rapid)
            

            # << acá iría el de los ladrillos >>
            # tendría que pasarle al reverse roll la posicion de la bola que rompe los ladrillos al romper el ultimo
            # y la barra que maneja el jugador


            posJugadorAux = (rapid.getJugadorPosXY()[0], rapid.getJugadorPosXY()[1]-200) # LINEA PROVISIONAL!!!!!!
            reverse = reverseroll.ReverseRoll(posJugadorAux, admin.getLoopContador())
            admin.ejecutarJuego(reverse)

            
            snake = snake_game.Game(loop=admin.getLoopContador(),ball_position=reverse.getJugadorPosXY(),
                                         player_pos=reverse.getUltimaPlataformaPosXY())
            admin.ejecutarJuego(snake)
            

            admin.agregarLoopContador()


        # << acá mostraría el score >>
        # apretando ESC vuelve al menu
        # apretando ENTER te pide nombre y guarda la puntuación, luego vuelve al menu
        
        score = admin.getScore()
        name_and_save = ui.gameover.gameover.main(score=score)
        name = name_and_save[0]
        save = name_and_save[1]
        if save and not name == "":
            print("Se guarda y vuelve al menu")
            #clase que guarda en un archivo local las puntuaciones al estilo => name:score (por ejemplo)
        else:
            print("No se guarda y vuelve al menu")

        print("FIN DEL JUEGO (se reincia porque no está implementado el menu)")
        

#TO_DO_LIST:
# Los que usan vs code pueden instalar: Todo Tree para ver esta clase de comentarios :)
#TODO: Hacer la escena del high_score_local (eze)

if __name__ == "__main__":
    main()