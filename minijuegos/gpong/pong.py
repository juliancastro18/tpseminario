import pygame, sys, math
from pygame.locals import *

from minijuegos.constantes import color
from minijuegos.scene import *
from minijuegos.gpong.bolapong import *
from minijuegos.gpong.paddle import *
from minijuegos.gpong.enemy import *
from minijuegos.meta import pause


class Pong(Scene):
    
    def __init__(self,barras,bola,loop): 
        super().__init__()
        self._velocidadBola = 8 + loop
        self._player = Paddle(barras[0].getPosXY(), barras[0].getRect().height, self._velocidadBola)
        self._enemy = Enemy(barras[1].getPosXY(), barras[0].getRect().height, self._velocidadBola)
        self._bola = BolaPong(bola.getPosicionXY(),self._velocidadBola)

    def process(self):
        self._clock.tick(self._fps)
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.togglePause()

        if not self.getIsPaused():

            self._bola.update()

            key = pygame.key.get_pressed()
            if(self._player._rect.top >= 0):
                if key[pygame.K_UP]:
                    self._player._rect.top += -self._player.speed
            if(self._player._rect.bottom <= configuration.SCREEN_HEIGHT):
                if key[pygame.K_DOWN]:
                    self._player._rect.bottom += self._player.speed

            #colision
            self._enemy.update(self._bola)
            self._bola.colision(self._player,self._enemy)
        
        self._state['alive'] = self._bola.bolaEnJuego(self)

        if (self._bola.verificarPuntos()):
            self._state['playing'] = False


            
    def display_frame(self):
        self.screen.fill(color.BLACK)       
        self._player.draw(self.screen)
        self._enemy.draw(self.screen)
        self._bola.draw(self.screen)

    def getIsPaused(self):
        return self._state['pause']
    
    def getIsPlaying(self):
        return self._state['playing']

    def get_barras(self):
        return [self._player, self._enemy]

    def togglePause(self):
        self._state['pause'] ^= True
    
    def agregarScore(self, puntos = 50):
        self._score += puntos

 
    
