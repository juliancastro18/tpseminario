import pygame, sys
from pygame.locals import *

from minijuegos import color
from minijuegos.scene import Scene
from minijuegos.clasesrapidroll.plataforma import *
from minijuegos.clasesrapidroll.bolarapidroll import *

class ReverseRoll(Scene):

    def __init__(self, posXY):

        super().__init__()
        self._bolaJugador = BolaRapidRoll(posXY)
        self._plataformas = []
        self._contadorPlataformas = 0
        self._maximoPlataformas = 10


    def process(self):

        self._clock.tick(self._fps) # defino 30 frames por segundo como maximo

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
                self._bolaJugador.desplazamientoHorizontal(False)
            if key_input[pygame.K_RIGHT]:
                self._bolaJugador.desplazamientoHorizontal(True)

            self.administradorPlataformas()

            for plat in self._plataformas:
                plat.update(self.screen)

            self._bolaJugador.update()

            # si solo queda la ultima plataforma y el jugador esta colisionando con ella, indico que terminó el juego
            if len(self._plataformas) == 1 and self._plataformas[0].ultimaPlataforma == True and self._bolaJugador.rect.colliderect(self._plataformas[0]):
                self._state['playing'] = False


    def display_frame(self):
        self.screen.fill(color.BLACK)

        for plat in self._plataformas:
            plat.draw(self.screen)

        for plat in self._plataformas:
            if plat.colisionSuperior(self._bolaJugador):
                self._bolaJugador.setEnPlataforma(plat.rect.top)

        self._bolaJugador.draw(self.screen)
        pygame.display.update()


    def administradorPlataformas(self):

        if self._contadorPlataformas == 0:
            self.agregarPrimerPlataforma()

        # elimino plataformas que ya no estén en pantalla
        for plat in self._plataformas:
            if plat.rect.bottom < 0:
                self._plataformas.remove(plat)


        # verifico si la ultima plataforma permite agregar una nueva, si es así la agrego
        if self._contadorPlataformas < self._maximoPlataformas:
            if len(self._plataformas) < 6 and self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma():
                self._plataformas.append( Plataforma() )
                self._contadorPlataformas += 1

        else:

            # si llego al maximo de plataformas, agrego a la lista la ultima plataforma
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma():
                ultimaPlataforma = Plataforma()
                self._plataformas.append( ultimaPlataforma )
                ultimaPlataforma.setUltimaPlataforma()


    def agregarPrimerPlataforma(self):
        primerPlataforma = Plataforma()
        primerPlataforma.setPrimerPlataforma()
        self._plataformas.append(primerPlataforma)
        self._contadorPlataformas += 1


    def getIsPaused(self):
        return self._state['pause']

    def togglePause(self):
        self._state['pause'] ^= True

    def getBola(self):
        return self._bolaJugador