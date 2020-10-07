import pygame, sys
from pygame.locals import *

from minijuegos.constantes import color
from minijuegos.scene import *
from minijuegos.grapidroll.bolarapidroll import *
from minijuegos.grapidroll.plataforma import *

class RapidRoll(Scene):

    def __init__(self, posXY, barras, loop = 0):

        super().__init__()
        self._bolaJugador = BolaRapidRoll(posXY, loop)
        self._plataformas = []
        self._contadorPlataformas = 0
        self._maximoPlataformas = 20 #+ (loop * 3)
        self._velPlataformas = 3 + int(loop*0.5)
        self._agregar_plataformas(barras)
        self._largoPlataformas = tamformas.BARRA_LADO_MAYOR - 60 # - (int(loop/2)*20)
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
            if self._ultimaPlat is not None:
                self._check_pos_bola()


            self.administradorPlataformas()

            for plat in self._plataformas:
                plat.update(self.screen)

            self._state['alive'] = self._bolaJugador.update()

            if self._state['alive'] == False:
                self._sonidoAscenso.stop()

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
                self.agregarScore()

        else:

            # si llego al maximo de plataformas, agrego a la lista la ultima plataforma
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma() and self._ultimaPlat is None:
                pos_fin = configuration.SCREEN_HEIGHT - (tamformas.BARRA_LADO_MENOR*2.5)
                ultimaPlataforma = Plataforma(self._velPlataformas, tamformas.BARRA_LADO_MAYOR-60, posicionFinal = pos_fin) #self._largoPlatformas
                self._plataformas.append( ultimaPlataforma )
                ultimaPlataforma.setUltimaPlataforma()
                self._ultimaPlat = ultimaPlataforma
                self._contadorPlataformas += 1
                self.agregarScore()


        # agrego plataformas no colisionables si existe ultimaPlataforma
        if self._ultimaPlat is not None and self._bolaJugador.rect.colliderect(self._ultimaPlat.getRect()):
            if self._plataformas[len(self._plataformas)-1].permiteSiguientePlataforma() and len(self._plataformas)<=18:
                self.agregarNoColisionable()


    def agregarPrimerPlataforma(self):
        primerPlataforma = Plataforma(self._velPlataformas, self._largoPlataformas)
        primerPlataforma.setPrimerPlataforma()
        self._plataformas.append(primerPlataforma)
        self._contadorPlataformas += 1
        self.agregarScore()

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

    def _check_pos_bola(self):
        if self._bolaJugador.rect.colliderect(self._ultimaPlat.getRect()):
            if self._bolaJugador.rect.right < self._ultimaPlat.getRect().left +20:
                self._bolaJugador.rect.right = self._ultimaPlat.getRect().left +20
            elif self._bolaJugador.rect.left > self._ultimaPlat.getRect().right -20:
                self._bolaJugador.rect.left = self._ultimaPlat.getRect().right -20


    def getIsPaused(self):
        return self._state['pause']

    def agregarScore(self, puntos = 5):
        self._score += puntos

    def _agregar_plataformas(self, barras):
        for b in barras:
            plat_nueva = Plataforma(velY = self._velPlataformas, barra=b)
            plat_nueva._velInicial = 0.5
            self._plataformas.append(plat_nueva)

    # METODOS PARA QUE OTROS JUEGOS USEN SUS ELEMENTOS
    def getListaBarrasProxJuego(self):
        listaBarras = []
        for plat in self._plataformas:
            if not plat.getUltimaPlataforma():
                listaBarras.append(plat)
        return listaBarras

    def getJugadorPosXY(self):
        return self._bolaJugador.getPosicionXY()

    def getJugadorBola(self):
        return self._bolaJugador

    def getUltimaPlataforma(self):
        return self._ultimaPlat