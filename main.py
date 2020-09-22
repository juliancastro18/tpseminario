import pygame, sys
from pygame.locals import *

from minijuegos.grapidroll import rapidroll
from minijuegos.greverseroll import reverseroll
from minijuegos.gsnake import snake_game
from minijuegos.constantes import configuration, tamformas, color
from minijuegos.meta import administrador
from minijuegos.gubicadorpong import ubicadorpong
from minijuegos.formas import barra, bola
from minijuegos import scene
from scorefile.filemanager import ScoreFile
import ui.gameover.gameover

def main():

    # inicio el audio
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    # inicio pygame
    pygame.init()
    # seteo la ventana
    pygame.display.set_caption('5in1')
    icono = pygame.image.load("data\\img\\ico.png")
    pygame.display.set_icon(icono)


    while True: # loop infinito hasta que se cierre pygame

        admin = administrador.Administrador() # inicio el administrador de juegos

        ubicador_pong = ubicadorpong.UbicadorPong(180, fondo_transparente = True, bloqueo = True)
        escena_aux = scene.Scene()
        fuente_aux = pygame.font.Font('data\\font\\dpcomic.ttf', 80)

        while ubicador_pong.get_game_state()['playing']:
            escena_aux.screen.fill(color.BLACK)
            escena_aux._draw_text(fuente_aux, "5in1", configuration.SCREEN_WIDTH/2-100, configuration.SCREEN_HEIGHT/2+20)
            ubicador_pong.process()
            ubicador_pong.display_frame()
            pygame.display.update()

        tupla_barras = ubicador_pong.get_barras()
        ubicador_pong2 = ubicadorpong.UbicadorPong(310, barras = tupla_barras, fondo_transparente = True, bloqueo = True)
        while ubicador_pong2.get_game_state()['playing']:
            escena_aux.screen.fill(color.BLACK)
            escena_aux._draw_text(fuente_aux, "nosviii", configuration.SCREEN_WIDTH/2-100, configuration.SCREEN_HEIGHT/2+20)
            ubicador_pong2.process()
            ubicador_pong2.display_frame()
            pygame.display.update()        

        # << acá iría el menú >>
        # opciones: comenzar, puntuaciones, controles, salir


        while admin.getEnJuego():

            admin.reproducirNuevoLoop()

            # << acá iría el pong >>
            # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
            # (ver getJugadorPosXY() en RapidRoll como referencia)
            # y tambien otro que devuelva una lista con las barras del pong


            rapid = rapidroll.RapidRoll((600, 40), admin.getLoopContador())
            admin.ejecutarJuego(rapid)
            
            # << acá iría el de los ladrillos >>
            # para obtener las barras: rapid.getListaBarrasProxJuego()
            # para obtener la bola: rapid.getJugadorPosXY() o rapid.getJugadorBola()
            # para obtener la barra que moverá el jugador: rapid.getUltimaPlataforma()

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
        score_file = ScoreFile()
        
        score = admin.getScore()
        if score_file.check_min_score(score):
            print('No entras en el top 10 y se va a el menu :P')
        else:
            name_and_save = ui.gameover.gameover.main(score=score)
            
            name = name_and_save[0]
            save = name_and_save[1]
            override = False
            if save and not name == "":
                print("Se guarda y vuelve al menu")
                score_file.save_score(name,score,override=override)
                #TABLA DE PUNTUACIONES
                for element in score_file.__str__int__():
                    print(element)
                #clase que guarda en un archivo local las puntuaciones al estilo => name:score (por ejemplo)
            else:
                print("No se guarda y vuelve al menu")

        print("FIN DEL JUEGO (se reincia porque no está implementado el menu)")
        

#TO_DO_LIST:
# Los que usan vs code pueden instalar: Todo Tree para ver esta clase de comentarios :)
#TODO: Hacer la escena del high_score_local (eze)

if __name__ == "__main__":
    main()