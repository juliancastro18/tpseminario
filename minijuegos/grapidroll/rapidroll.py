import pygame, sys
from pygame.locals import *

from minijuegos.constantes import color
from minijuegos.scene import *
from minijuegos.grapidroll.bolarapidroll import *
from minijuegos.grapidroll.plataforma import *

class RapidRoll(Scene):

    def __init__(self, posXY, loop = 0):

        super().__init__()
        self._bolaJugador = BolaRapidRoll(posXY, loop)
        self._plataformas = []
        self._contadorPlataformas = 0
        self._maximoPlataformas = 10 + (loop * 2)
        self._velPlataformas = 3 + int(loop*0.5)
        self._largoPlataformas = tamformas.BARRA_LADO_MAYOR - (int(loop/2)*20)
        self._sonidoColision = pygame.mixer.Sound('data\\sound\\hit.wav')
        self._ultimaPlat = None
        self._degrade = pygame.image.load("data\\img\\gradient.png")

        self._sonidoAscenso = pygame.mixer.Sound('data\\sound\\platup.wav')


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
                self._bolaJugador.desplazamientoHorizontal(False)
            if key_input[pygame.K_RIGHT]:
                self._bolaJugador.desplazamientoHorizontal(True)

            self.administradorPlataformas()

            for plat in self._plataformas:
                plat.update(self.screen)

            self._state['alive'] = self._bolaJugador.update()

            # si solo queda la ultima plataforma y el jugador esta colisionando con ella, indico que terminó el juego
            if len(self._plataformas) > 1 and self._ultimaPlat is not None and self._sumarVelocidadesPlat() == 0:
                self._sonidoAscenso.stop()
                self._state['playing'] = False


    def display_frame(self):
        self.screen.fill(color.BLACK)

        for plat in self._plataformas:
            if not plat.getEsColisionable():
                plat.draw(self.screen)

        if self._ultimaPlat is not None:
            self.screen.blit(self._degrade, (0,0))

        colisionandoAhora = False
        for plat in self._plataformas:
            if plat.getEsColisionable():
                plat.draw(self.screen)
                if plat.colisionSuperior(self._bolaJugador):
                    self._bolaJugador.setEnPlataforma(plat.getTop())
                    colisionandoAhora = True

        if colisionandoAhora == False:
            self._bolaJugador.colisionando = False

        if self._bolaJugador.colisionando == False and colisionandoAhora == True:
            self._sonidoColision.play()
            self._bolaJugador.colisionando = True


        self._bolaJugador.draw(self.screen)


    def administradorPlataformas(self):

        if self._contadorPlataformas == 0:
            self.agregarPrimerPlataforma()

        # elimino plataformas que ya no estén en pantalla
        for plat in self._plataformas:
            if plat.getBottom() < 0:
                self._plataformas.remove(plat)


        # verifico si la ultima plataforma permite agregar una nueva, si es así la agrego
        if self._contadorPlataformas < self._maximoPlataformas:
            if len(self._plataformas) < 6 and self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma():
                self._plataformas.append( Plataforma(self._velPlataformas, self._largoPlataformas) )
                self._contadorPlataformas += 1

        else:

            # si llego al maximo de plataformas, agrego a la lista la ultima plataforma
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma() and self._ultimaPlat is None:
                ultimaPlataforma = Plataforma(self._velPlataformas, self._largoPlataformas, posicionFinal = 380)
                self._plataformas.append( ultimaPlataforma )
                ultimaPlataforma.setUltimaPlataforma()
                self._ultimaPlat = ultimaPlataforma
                self._contadorPlataformas += 1


        # agrego plataformas no colisionables si existe ultimaPlataforma
        if self._ultimaPlat is not None and self._bolaJugador.rect.colliderect(self._ultimaPlat.getRect()):
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma() and len(self._plataformas)<=18:
                self.agregarNoColisionable()


    def agregarPrimerPlataforma(self):
        primerPlataforma = Plataforma(self._velPlataformas, self._largoPlataformas)
        primerPlataforma.setPrimerPlataforma()
        self._plataformas.append(primerPlataforma)
        self._contadorPlataformas += 1

    def agregarNoColisionable(self):
        cantNoColisionables = self._cantNoColisionables()

        if cantNoColisionables == 1:
            self._sonidoAscenso.play()

        fila = (int(cantNoColisionables/6) * tamformas.BARRA_LADO_MENOR) + 50 + int(cantNoColisionables/6) * 5
        nuevaPlataforma = Plataforma(self._velPlataformas*1.35, 90, colisionable = False, posicionFinal = fila)
        nuevaPlataforma.setNoColisionable(self._plataformas[len(self._plataformas)-1])
        self._plataformas.append(nuevaPlataforma)

    def _sumarVelocidadesPlat(self):
        sumaVelocidad = 0
        for plat in self._plataformas:
            sumaVelocidad += plat._velY
        return sumaVelocidad

    def _cantNoColisionables(self):
        cont = 0
        for plat in self._plataformas:
            if not plat.getEsColisionable():
                cont += 1
        return cont


    def getIsPaused(self):
        return self._state['pause']

    def togglePause(self):
        self._state['pause'] ^= True


    # METODOS PARA QUE OTROS JUEGOS USEN SUS ELEMENTOS
    def getListaBarrasProxJuego(self):
        listaBarras = []
        for plat in self._plataformas:
            if not plat.getUltimaPlataforma():
                nuevaBarra = Barra.new_from(plat)
                listaBarras.append(nuevaBarra)
        return listaBarras

    def getJugadorPosXY(self):
        return self._bolaJugador.getPosicionXY()

    def getJugadorBola(self):
        return Bola.new_from(self._bolaJugador)

    def getUltimaPlataforma(self):
        return Barra.new_from(self._ultimaPlat)