import pygame, math, random
from minijuegos.constantes import color, tamformas, configuration
from minijuegos.gameobject import *
from minijuegos.formas.bola import *
from minijuegos.gpong.paddle import *
from minijuegos.gpong.enemy import *

class BolaPong(Bola):
    def __init__(self,posXY,velocidad):
        super().__init__(posXY)
        self.dirY = 0
        self.dirX = 0
        self.speed = velocidad
        self.set_xy(self.angulo_random_ini())
        self._ult_dist = 0
        

    def update(self):
        if self.bolaEnJuego():
            #desplazamiento bola
            self.rect.top += self.dirY
            self.rect.left += self.dirX

    
    def bolaEnJuego(self):
        sigue_enJuego = True
        #comprobamos si la pelota esta o no en pantalla.
        if (self.rect.left < -50 or self.rect.right > configuration.SCREEN_WIDTH):
            sigue_enJuego = False
        return sigue_enJuego


    def reboteSuperiorInferior(self):
        if self.rect.bottom > configuration.SCREEN_HEIGHT:
            self.dirY *= -1
            self.rect.bottom = configuration.SCREEN_HEIGHT
        if self.rect.top < 0:
            self.dirY *= -1
            self.rect.top = 0


    def colision(self,paddle,enemy,escena):
        if self.rect.colliderect(paddle._rect):
                self.set_angulo(paddle)
                #self.dirX *= -1
                escena.agregarScore()
                #print(escena._score)
        elif self.rect.colliderect(enemy._rect):
                self.set_angulo(enemy)
                #self.dirX *= -1
                
            
    def set_angulo(self, barra):
        # calculo distancia de la bola al centro de la paleta
        distancia_centro = self.rect.midleft[1] - barra._rect.midleft[1]

        if distancia_centro == self._ult_dist: # con este if evito rebotes verticales infinitos
            if bool(random.getrandbits(1)):
                distancia_centro += 2
            else:
                distancia_centro -= 2

        # obtengo el porcentaje de distancia (1 si esta en la punta, 0 en el centro)
        porcentaje_dist = distancia_centro / (barra.getLargo() / 2)
        # para sacar el angulo: a 90º se le resta (45º * el porcentaje_dist)
        if isinstance(barra, Paddle):
            angulo = porcentaje_dist * (math.pi/3)
        else:
            angulo = math.pi - porcentaje_dist * (math.pi/3)
        # seteo direcciones de la bola en relacion al angulo
        self.set_xy(angulo)          

        # si la bola excede la posicion de la barra, no rebota
        if isinstance(barra, Paddle):
            if self.rect.left < barra._rect.right-self.dirX-tamformas.BARRA_LADO_MENOR/2:
                self.dirX *= -1
        else:
            if self.rect.right > barra._rect.left-self.dirX+tamformas.BARRA_LADO_MENOR/2:
                self.dirX *= -1

        self._ult_dist = distancia_centro

    def set_xy(self, angulo):
        self.dirX = math.cos(angulo) * self.speed
        self.dirY = math.sin(angulo) * self.speed

    def angulo_random_ini(self):
        return random.uniform(-math.pi/8,math.pi/8)          