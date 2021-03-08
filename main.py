import pygame, sys, os
from pygame.locals import *

from minijuegos.constantes import configuration, tamformas, color
from minijuegos.formas import barra, bola
from minijuegos.gpong import pong
from minijuegos.grapidroll import rapidroll
from minijuegos.gladrillos import ladrillosgame
from minijuegos.greverseroll import reverseroll
from minijuegos.gsnake import snake_game
from minijuegos.gubicadorpong import ubicadorpong
from minijuegos.meta import administrador
from ui.menu import menu
from scorefile.filemanager import ScoreFile
import ui.gameover.gameover
import ui.highscore.highscore

def main():

    # AUDIO INIT
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    # PYGAME INIT
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    # SETEO VENTANA
    pygame.display.set_caption('5in1')
    icono = pygame.image.load("data\\img\\ico.png")
    pygame.display.set_icon(icono)
    pygame.mouse.set_visible(False)

    # ADMIN Y MENU INIT
    admin = administrador.Administrador() # inicio el administrador de juegos
    menu_principal = menu.Menu()


    while True: # loop infinito hasta el cierre del programa

    	# MUESTRO MENU
        menu_principal.main()

        # GET DE ELEMENTOS DEL UBICADOR
        barras_inicio = menu_principal.ubicador_pong.get_barras()
        bola_inicio = menu_principal.ubicador_pong.get_bola()

        # UBICADOR INICIO
        dist_borde = tamformas.BARRA_LADO_MENOR*2
        ubicador_inicio = ubicadorpong.UbicadorPong(dist_borde, barras = barras_inicio, bola_param = bola_inicio, tam_final=tamformas.BARRA_LADO_MAYOR-60)
        admin.ejecutarJuego(ubicador_inicio)

        while admin.getEnJuego():

            admin.iniciarNuevoLoop()

            # PONG
            pong_game = pong.Pong(ubicador_inicio.get_barras(),ubicador_inicio.get_bola(),admin.getLoopContador())
            admin.ejecutarJuego(pong_game)

            # RAPIDROLL
            if admin.getEnJuego():
	            rapid = rapidroll.RapidRoll(pong_game._bola.getPosicionXY(), pong_game.get_barras(), admin.getLoopContador())
	            admin.ejecutarJuego(rapid)
            
            # LADRILLOS
            if admin.getEnJuego():
	            ladrillos = ladrillosgame.Ladrillos(rapid.getJugadorPosXY(), rapid.getUltimaPlataforma(),
                                                    rapid.getListaBarrasProxJuego(), admin.getLoopContador())
	            admin.ejecutarJuego(ladrillos)

	        # REVERSEROLL
            if admin.getEnJuego():
	            reverse = reverseroll.ReverseRoll(ladrillos.getBolaPosXY(), ladrillos.getPaleta(), admin.getLoopContador())
	            admin.ejecutarJuego(reverse)

	        # SNAKE
            if admin.getEnJuego():
	            snake = snake_game.Game(loop=admin.getLoopContador(),ball_position=reverse.getJugadorPosXY(),
	                                         player_pos=reverse.getUltimaPlataformaPosXY())
	            admin.ejecutarJuego(snake)

            # TRANSICION A PONG
            if admin.getEnJuego():
                barra_izq = barra.Barra(True, (-tamformas.BARRA_LADO_MENOR,0), largo=configuration.SCREEN_HEIGHT)
                barra_der = barra.Barra(True, (configuration.SCREEN_WIDTH,0), largo=configuration.SCREEN_HEIGHT)
                ubicador_fin = ubicadorpong.UbicadorPong(barras=(barra_izq,barra_der), fondo_transparente=True,
                                                        bloqueo = True, barras_desde_afuera = True)
                ubicador_fin.ocultar_bola()
                admin.ejecutarJuego(ubicador_fin, juego_sec=snake)
                ubicador_inicio = ubicadorpong.UbicadorPong(barras=ubicador_fin.get_barras(), tam_final=pong_game.get_barras()[0].getLargo(),
                                                        bloqueo = True, distancia_final_screen_left=pong_game.get_barras()[0]._rect.left)
                admin.ejecutarJuego(ubicador_inicio)
            

	    # MANEJO DE PUNTUACIÓN
        score_file = ScoreFile()
        score = admin.getScore()
        name_and_save = ui.gameover.gameover.main(score=score, menu=menu_principal, top=score_file.check_top(score))
        
        name = name_and_save[0]
        save = name_and_save[1]
        if save and not name == "":
            #print("Se guarda y vuelve al menu")
            score_file.save_score(name,score)
            # TABLA DE PUNTUACIONES
            for element in score_file.__str__int__():
                print(element)
            # Clase que guarda en un archivo local las puntuaciones al estilo => name:score (por ejemplo)
            score_file.override_file()
        else:
            pass
            #print("No se guarda y vuelve al menu")

        # RESETEO ADMIN Y MENU
        admin.set_restart()
        menu_principal.set_restart()
        

if __name__ == "__main__":
    main()