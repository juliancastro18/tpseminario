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
        self.speed = 1
        self.speed_max = velocidad
        self.set_xy(self.angulo_random_ini())
        self._sonidoColision = pygame.mixer.Sound('data\\sound\\hit.wav')
        self._sonidoWin = pygame.mixer.Sound('data\\sound\\coin.wav')
        self.puntos = 0
        self.recien_iniciada = True
        

    def update(self):
        #desplazamiento bola
        self.rect.top += self.dirY * self.speed
        self.rect.left += self.dirX * self.speed

        if self.speed < self.speed_max:
            self.speed = self.speed*1.1
        elif self.speed > self.speed_max:
            self.speed  = self.speed_max

        self.reboteSuperiorInferior()

    
    def bolaEnJuego(self, escena):
        sigue_enJuego = True
        #comprobamos si la pelota esta o no en pantalla.
        if self.rect.right >= configuration.SCREEN_WIDTH:
            escena.agregarScore()
            if self.puntos<1:
                self.rect.centerx = configuration.SCREEN_WIDTH/2
                self.rect.centery = configuration.SCREEN_HEIGHT/2
                self.speed = 1
                self.recien_iniciada = True
                self.set_xy(self.angulo_random_ini())
            else:
                self.rect.right = configuration.SCREEN_WIDTH
            self.puntos += 1
            self._sonidoWin.play()
        if self.rect.left < 0:
            sigue_enJuego = False

        return sigue_enJuego

    def verificarPuntos(self):
        pasarJuego = False
        if self.puntos >=2:
            pasarJuego = True
        return pasarJuego
            


    def reboteSuperiorInferior(self):
        if self.rect.bottom > configuration.SCREEN_HEIGHT:
            self.dirY *= -1
            self.rect.bottom = configuration.SCREEN_HEIGHT
        if self.rect.top < 0:
            self.dirY *= -1
            self.rect.top = 0


    def colision(self,paddle,enemy):
        if self.rect.colliderect(paddle._rect):
                self.set_angulo(paddle)
        elif self.rect.colliderect(enemy._rect):
                self.set_angulo(enemy)
                
            
    def set_angulo(self, barra):
        if self.recien_iniciada == True:
            self.recien_iniciada = False
        # calculo distancia de la bola al centro de la paleta
        distancia_centro = self.rect.midleft[1] - barra._rect.midleft[1]

        # obtengo el porcentaje de distancia (1 si esta en la punta, 0 en el centro)
        porcentaje_dist = distancia_centro / (barra.getLargo() / 2)
        # para sacar el angulo: a 90º se le resta (45º * el porcentaje_dist)
        if isinstance(barra, Paddle):
            angulo = porcentaje_dist * (math.pi/4)
        else:
            angulo = math.pi - porcentaje_dist * (math.pi/4)

        # seteo direcciones de la bola en relacion al angulo
        self.set_xy(angulo)          

        # si la bola excede la posicion de la barra, no rebota
        if isinstance(barra, Paddle):
            if self.rect.left < barra._rect.right-(self.dirX*self.speed)-tamformas.BARRA_LADO_MENOR/2:
                self.dirX *= -1
            else:
                self.rect.left = barra._rect.right
                self._sonidoColision.play()
        else:
            if self.rect.right > barra._rect.left-(self.dirX*self.speed)+tamformas.BARRA_LADO_MENOR/2:
                self.dirX *= -1
            else:
                self.rect.right = barra._rect.left
                self._sonidoColision.play()


    def set_xy(self, angulo):
        self.dirX = math.cos(angulo) 
        self.dirY = math.sin(angulo) 

    def angulo_random_ini(self):
        return random.uniform(-math.pi/8,math.pi/8)          