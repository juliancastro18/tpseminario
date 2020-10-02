import pygame, sys
from pygame.locals import *

from minijuegos.constantes import color, configuration
from minijuegos.scene import *
from minijuegos.gladrillos.bolaladrillos import *
from minijuegos.gladrillos.paletaladrillos import *

class Ladrillos(Scene):
    
    def __init__(self, bolaPosXY, barra : Barra, listaBarras : Barra):
        
        super().__init__()
        self._bola = BolaLadrillos(bolaPosXY)
        self._paletaJugador = Paleta(barra.getPosXY(), barra.getLargo())
        self._tablero = listaBarras

    def process(self):
        self._clock.tick(self._fps) # defino 60 frames por segundo como maximo

        # para cada evento que reciba pygame...
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.togglePause()

        if not self.getIsPaused():

            key_input = pygame.key.get_pressed()   
            if key_input[pygame.K_LEFT]:
                self._paletaJugador.update(False)
            if key_input[pygame.K_RIGHT]:
                self._paletaJugador.update(True)

            self._state['alive'] = self._bola.update()

            if self._bola.rect.colliderect(self._paletaJugador._rect):
                if self._bola.rect.bottom <= self._paletaJugador._rect.top+self._bola.vel_y+2: #si la bola está por encima de la paleta
                    self._bola.posY = self._paletaJugador._rect.top-(self._bola.radio*2) #posiciono la bola encima de la paleta
                    self._bola.vel_y *= -1 #cambio de direccion

            self.colisionTablero()

            if len(self._tablero) == 0:
                self._state['playing'] = False

    def colisionTablero(self):
        for bloque in self._tablero:
            if self._bola.rect.colliderect(bloque._rect):
                self._tablero.remove(bloque)
                self.agregarScore()
                if self._bola.rect.top >= bloque._rect.bottom+self._bola.vel_y or self._bola.rect.bottom <= bloque._rect.top+self._bola.vel_y:
                    self._bola.vel_y *= -1
                    break
                elif self._bola.rect.right >= bloque._rect.left or self._bola.rect.left <= bloque._rect.right:
                    self._bola.vel_x *= -1
                    break

    def display_frame(self):
        self.screen.fill(color.BLACK)
        self._bola.draw(self.screen)
        self._paletaJugador.draw(self.screen)

        for bloque in self._tablero:
            bloque.draw(self.screen)

    def getIsPaused(self):
        return self._state['pause']

    def agregarScore(self, puntos = 1):
        self._score += puntos

    #GETS PARA JUEGO SIGUIENTE

    def getBolaPosXY(self):
        return self._bola.getPosicionXY()

    def getPaleta(self):
        return self._paletaJugador