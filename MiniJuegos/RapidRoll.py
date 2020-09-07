import pygame, sys
from pygame.locals import *
from MiniJuegos.Clases_RapidRoll.Plataforma import *
from MiniJuegos.Clases_RapidRoll.Bola import *

anchoPantalla, altoPantalla = 640, 480
blanco = (255,255,255)
negro = (0,0,0)

def administradorPlataformas(plataformas, enPausa):

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
    enPausa = False
       
    while enJuego and contadorPlataformas < 20: # se ejecutará el siguiente loop hasta terminar el juego
        
        reloj.tick(60) # defino 60 frames por segundo como maximo
        
        ventana.fill(negro)

        # para cada evento que reciba pygame...
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_ESCAPE:
                    enPausa^=True
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT] and not enPausa:
            bolaJugador.desplazamientoHorizontal(False)
        if key_input[pygame.K_RIGHT] and not enPausa:
            bolaJugador.desplazamientoHorizontal(True)
        
        contadorPlataformas += administradorPlataformas(plataformas, enPausa)

        for plat in plataformas:
            plat.actualizar(ventana, enPausa)
            if plat.rect.colliderect(bolaJugador.rect):
                bolaJugador.setEnPlataforma(plat.rect.top)

        enJuego = bolaJugador.actualizar(ventana, enPausa)
        pygame.display.update()

    return enJuego, bolaJugador.posicionXY()