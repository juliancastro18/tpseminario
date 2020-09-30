import pygame, sys
from pygame.locals import *

from minijuegos.constantes import color
from minijuegos.scene import *
from minijuegos.gladrillos.bolaladrillos import *
from minijuegos.gladrillos.paletaladrillos import *

class Ladrillos(Scene):
    
    def __init__(self, bolaPosXY, paletaPosXY):
        
        super().__init__()
        self._bola = BolaLadrillos(bolaPosXY)
        self._bola.vel_x = 10
        self._bola.vel_y = -5
        self._paletaJugador = Paleta(paletaPosXY)

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
                self._bola.vel_y *= -1


    def display_frame(self):
        self.screen.fill(color.BLACK)
        self._bola.draw(self.screen)
        self._paletaJugador.draw(self.screen)

    def getIsPaused(self):
        return self._state['pause']