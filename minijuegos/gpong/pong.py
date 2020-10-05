import pygame, sys
from pygame.locals import *

from minijuegos.constantes import color
from minijuegos.scene import *
from minijuegos.gpong.bolapong import *
from minijuegos.gpong.paddle import *
from minijuegos.gpong.enemy import *
from minijuegos.meta import pause


class Pong(Scene):
    
    def __init__(self,largo,posXYJugador,posXYEnemy,posXYBola,loop): 
        super().__init__()
        self._velocidadBola = 5 + loop
        self._player = Paddle(posXYJugador, largo)
        self._enemy = Enemy(posXYEnemy, largo)
        self._bola = BolaPong(posXYBola,self._velocidadBola)

    def process(self):
        self._clock.tick(self._fps)
        
        if not self.getIsPaused():
            self._bola.update()
        #eventos
        if self._state['playing']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.togglePause()
                if not self.getIsPaused():
                    key = pygame.key.get_pressed()
                    if(self._player._rect.top >= 0):
                        if key[pygame.K_w]:
                            self._player._rect.top += -self._player.speed
                    if(self._player._rect.bottom <= configuration.SCREEN_HEIGHT):
                        if key[pygame.K_s]:
                            self._player._rect.bottom += self._player.speed
            if not self.getIsPaused():
                self._bola.reboteSuperiorInferior()
                #colision
                self._enemy.update(self._bola)
                self._bola.colision(self._player,self._enemy,self)
        
        self._state['playing'] = self._bola.bolaEnJuego()
        if self._state['playing'] == False:
            #Capturo pos bola para pasarsela al proximo juego
            posBola = (self._bola.getPosicionXY())
            posPlayer = self._player.getPosXY()
            posEnemy = self._enemy.getPosXY()
            #deberia retornar esta tupla
            posiciones = (posPlayer,posEnemy)

            pygame.quit()
            sys.exit()


            
    
    def display_frame(self):
        self.screen.fill(color.BLACK)       
        self._player.draw(self.screen)
        self._enemy.draw(self.screen)
        self._bola.draw(self.screen)
        pygame.display.update()


    def getIsPaused(self):
        return self._state['pause']
    
    def getIsPlaying(self):
        return self._state['playing']

    def togglePause(self):
        self._state['pause'] ^= True
    
    def agregarScore(self, puntos = 1):
        self._score += puntos
 
    
