import pygame, sys
from pygame.locals import *
from MiniJuegos.Clases_RapidRoll.Plataforma import *
from MiniJuegos.Clases_RapidRoll.Bola import *

anchoPantalla, altoPantalla = 640, 480
blanco = (255,255,255)
negro = (0,0,0)

def administradorPlataformas(plataformas):

    plataformaAgregada = 0

    for plat in plataformas:
        if plat.rect.bottom < 0:
            plataformas.remove(plat)


    if len(plataformas) < 6 and plataformas[len(plataformas)-1].permiteSiguientePlataforma():
        plataformas.append( Plataforma() )
        plataformaAgregada = 1

    return plataformaAgregada


def RapidRoll(posX, posY, ventana):
    
    reloj = pygame.time.Clock() # creo un reloj para regular frames por segundo
    
    # inicializo los objetos
    bolaJugador = Bola(posX,posY)
    primerPlataforma = Plataforma()
    primerPlataforma.setPrimerPlataforma()
    plataformas = [primerPlataforma]
    contadorPlataformas = 1

    enJuego = True
       
    while enJuego and contadorPlataformas < 10: # se ejecutará el siguiente loop hasta terminar el juego
        
        reloj.tick(60) # defino 60 frames por segundo como maximo
        
        ventana.fill(negro)

        # para cada evento que reciba pygame...
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            bolaJugador.desplazamientoHorizontal(False)
        if key_input[pygame.K_RIGHT]:
            bolaJugador.desplazamientoHorizontal(True)
        
        contadorPlataformas += administradorPlataformas(plataformas)

        for plat in plataformas:
            plat.actualizar(ventana)
            if plat.rect.colliderect(bolaJugador.rect):
                bolaJugador.setEnPlataforma(plat.rect.top)

        enJuego = bolaJugador.actualizar(ventana)
        pygame.display.update()

    return enJuego, bolaJugador.posicionXY()