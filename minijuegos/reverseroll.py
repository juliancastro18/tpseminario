import pygame, sys
from pygame.locals import *

from minijuegos import color
from minijuegos.scene import Scene
from minijuegos.clasesrapidroll.plataforma import *
from minijuegos.clasesreverseroll.bolareverseroll import *
from minijuegos.clasesreverseroll.plataformamovil import *

class ReverseRoll(Scene):

    def __init__(self, posXY, loop = 0):

        super().__init__()
        self._bolaJugador = BolaReverseRoll(posXY, loop)
        self._plataformas = []
        self._contadorPlataformas = 0
        self._maximoPlataformas = 10 + (loop * 3)
        self._velPlataformas = 3 + int(loop*0.5)
        self._largoPlataformas = forma.BARRA_LADO_MAYOR - 50 + (loop*5)


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
            if key_input[pygame.K_UP]:
                self._bolaJugador.desplazamientoVertical(True)
            if key_input[pygame.K_DOWN]:
                self._bolaJugador.desplazamientoVertical(False)

            self.administradorPlataformas()

            for plat in self._plataformas:
                plat.update(self.screen)

            # si solo queda la ultima plataforma y el jugador esta colisionando con ella, indico que terminó el juego
            if len(self._plataformas) == 1 and self._plataformas[0].getUltimaPlataforma():
                self._state['playing'] = False


    def display_frame(self):
        self.screen.fill(color.BLACK)

        for plat in self._plataformas:
            plat.draw(self.screen)
            if plat.colisionSuperior(self._bolaJugador):
                self._state['alive'] = False

        self._bolaJugador.draw(self.screen)
        pygame.display.update()


    def administradorPlataformas(self):

        if len(self._plataformas) == 0 and self._contadorPlataformas == 0:
            self._plataformas.append( Plataforma(self._velPlataformas, self._largoPlataformas) )

        # elimino plataformas que ya no estén en pantalla
        for plat in self._plataformas:
            if plat.getBottom() < 0:
                self._plataformas.remove(plat)


        # verifico si la ultima plataforma permite agregar una nueva, si es así la agrego
        if self._contadorPlataformas < self._maximoPlataformas:
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma():
                if self._plataformas[len(self._plataformas)-1].getDistanciaNext() >= 145:
                    self._plataformas.append ( PlataformaMovil(self._velPlataformas, self._largoPlataformas) )
                else:
                    self._plataformas.append( Plataforma(self._velPlataformas, self._largoPlataformas) )
                self._contadorPlataformas += 1
        else:
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma():
                ultimaPlataforma = Plataforma(self._velPlataformas, 75)
                ultimaPlataforma.setUltimaPlataforma()
                ultimaPlataforma.setGrosor(25)
                self._plataformas.append( ultimaPlataforma )


    def agregarPrimerPlataforma(self):
        primerPlataforma = Plataforma(self._velPlataformas, self._largoPlataformas)
        primerPlataforma.setPrimerPlataforma()
        self._plataformas.append(primerPlataforma)
        self._contadorPlataformas += 1


    def getIsPaused(self):
        return self._state['pause']

    def getUltimaPlataformaPosXY(self):
        if len(self._plataformas) == 1:
            return self._plataformas[0].getPosXY()
        else:
            return (0,0)

    def togglePause(self):
        self._state['pause'] ^= True

    def getJugadorPosXY(self):
        return self._bolaJugador.getPosicionXY()