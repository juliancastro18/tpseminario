import pygame
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.bola import *
from minijuegos.gpong.paddle import *
from minijuegos.gpong.enemy import *

class BolaPong(Bola):
    def __init__(self,posXY,velocidad):
        super().__init__(posXY)
        self.dirY = 1
        self.dirX = 1
        self.speed = velocidad
        

    def update(self):
        if self.bolaEnJuego():
            #desplazamiento bola
            self.rect.bottom += self.speed * self.dirY
            self.rect.right += self.speed * self.dirX

    
    def bolaEnJuego(self):
        sigue_enJuego = True
        #comprobamos si la pelota esta o no en pantalla.
        if (self.rect.left < -50 or self.rect.right > configuration.SCREEN_WIDTH):
            sigue_enJuego = False
        return sigue_enJuego


    def reboteSuperiorInferior(self):
        if self.rect.bottom >= configuration.SCREEN_HEIGHT:
            self.dirY *= -1
        if self.rect.top <= 0:
            self.dirY *= -1


    def colision(self,paddle,enemy,escena):
        if self.rect.colliderect(paddle._rect): 
                self.rect.left = paddle._rect.right
                self.dirX = 1
                escena.agregarScore()
                print(escena._score)
                
        if self.rect.colliderect(enemy._rect):
                self.rect.right = enemy._rect.left
                self.dirX = -1
                
            
            


        
    


            