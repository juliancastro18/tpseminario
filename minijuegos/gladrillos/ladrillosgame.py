import pygame, sys, math, random
from pygame.locals import *

from minijuegos.constantes import color, configuration, tamformas
from minijuegos.scene import *
from minijuegos.gladrillos.bolaladrillos import *
from minijuegos.gladrillos.paletaladrillos import *

class Ladrillos(Scene):
    
    def __init__(self, bolaPosXY, barra : Barra, listaBarras : Barra, loop):        
        super().__init__()
        self._vel_bola = 8 + loop #setea la vel constante, aumenta con cada loop 
        self._bola = BolaLadrillos(bolaPosXY, self._vel_bola)
        self._paletaJugador = Paleta(barra.getPosXY(), barra.getLargo(), self._vel_bola)
        self._tablero = listaBarras
        self._ult_dist = 0

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

            # si la bola colisiona con la paleta
            if self._bola.rect.colliderect(self._paletaJugador._rect):
                # calculo distancia de la bola al centro de la paleta
                distancia_centro = self._bola.rect.midbottom[0] - self._paletaJugador._rect.midtop[0]
                if distancia_centro == 0 and self._ult_dist == 0: # con este if evito rebotes verticales infinitos
                    if bool(random.getrandbits(1)):
                        distancia_centro = 2
                    else:
                        distancia_centro = -2
                # obtengo el porcentaje de distancia (1 si esta en la punta, 0 en el centro)
                porcentaje_dist = distancia_centro / (self._paletaJugador.getLargo() / 2)
                # para sacar el angulo: a 90º se le resta (45º * el porcentaje_dist)
                angulo = math.pi/2 - porcentaje_dist * (math.pi/4)
                # seteo direcciones de la bola en relacion al angulo
                self._bola.set_xy(angulo)
                # si la bola está por encima de la mitad de la paleta, la hago rebotar
                if self._bola.rect.bottom <= self._paletaJugador._rect.top+self._bola.mov_y+tamformas.BARRA_LADO_MENOR/2:
                    self._bola.mov_y *= -1 # rebote
                self._ult_dist = distancia_centro

            self.colisionTablero()

            if len(self._tablero) == 0:
                self._state['playing'] = False

    def colisionTablero(self):
        for bloque in self._tablero:
            if self._bola.rect.colliderect(bloque._rect):
                self._tablero.remove(bloque)
                self.agregarScore()
                if self._bola.rect.top >= bloque._rect.bottom+self._bola.mov_y or self._bola.rect.bottom <= bloque._rect.top+self._bola.mov_y:
                    self._bola.mov_y *= -1
                    break
                elif self._bola.rect.right >= bloque._rect.left or self._bola.rect.left <= bloque._rect.right:
                    self._bola.mov_x *= -1
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