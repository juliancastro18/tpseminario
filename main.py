import pygame, sys
from pygame.locals import *

from minijuegos.grapidroll import rapidroll
from minijuegos.gladrillos import ladrillosgame
from minijuegos.greverseroll import reverseroll
from minijuegos.gsnake import snake_game
from minijuegos.constantes import configuration, tamformas, color
from minijuegos.meta import administrador
from minijuegos.gubicadorpong import ubicadorpong
from ui.menu import menu
from minijuegos.formas import barra, bola
from minijuegos import scene
from scorefile.filemanager import ScoreFile
import ui.gameover.gameover
import ui.highscore.highscore

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
    pygame.mouse.set_visible(False)

    # instancio el administrador y el menu
    admin = administrador.Administrador() # inicio el administrador de juegos
    menu_principal = menu.Menu()

    while True: # loop infinito hasta que se cierre pygame

        menu_principal.main()

        barras_inicio = menu_principal.ubicador_pong.get_barras()
        bola_inicio = menu_principal.ubicador_pong.get_bola()
        ubicador_inicio = ubicadorpong.UbicadorPong(50, barras = barras_inicio, bola_param = bola_inicio)
        admin.ejecutarJuego(ubicador_inicio)

        while admin.getEnJuego():

            admin.reproducirNuevoLoop()

            # << acá iría el pong >>
            # el pong tendria que tener un metodo para obtener la pos de la bola cuando terminó de ejecutar
            # (ver getJugadorPosXY() en RapidRoll como referencia)
            # y tambien otro que devuelva una lista con las barras del pong


            #rapid = rapidroll.RapidRoll((600, 40), admin.getLoopContador())
            #admin.ejecutarJuego(rapid)
            
            posAuxPelota = configuration.SCREEN_WIDTH/2-14, configuration.SCREEN_HEIGHT-59
            posAuxPaleta = configuration.SCREEN_WIDTH/2-50, configuration.SCREEN_HEIGHT-30
            ladrillos = ladrillosgame.Ladrillos(posAuxPelota, posAuxPaleta)
            admin.ejecutarJuego(ladrillos)
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
        
        name_and_save = ui.gameover.gameover.main(score=score, menu=menu_principal, top=score_file.check_top(score))
        
        name = name_and_save[0]
        save = name_and_save[1]
        if save and not name == "":
            print("Se guarda y vuelve al menu")
            score_file.save_score(name,score)
            #TABLA DE PUNTUACIONES
            for element in score_file.__str__int__():
                print(element)
            #clase que guarda en un archivo local las puntuaciones al estilo => name:score (por ejemplo)
            score_file.override_file()
        else:
            print("No se guarda y vuelve al menu")
        
        #PUNTUACIONES, LLAMAR CUANDO SEA NECESARIO
        # ui.highscore.highscore.main(score_file.__str__int__())

        # pongo el menu y el admin con sus valores iniciales
        menu_principal.set_restart()
        admin.set_restart()
        


#TO_DO_LIST:
# Los que usan vs code pueden instalar: Todo Tree para ver esta clase de comentarios :)
#TODO: Hacer la escena del high_score_local (eze)

if __name__ == "__main__":
    main()