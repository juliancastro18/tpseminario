import pygame
from random import randint

anchoPantalla, altoPantalla = 640, 480
blanco = (255,255,255)
negro = (0,0,0)

class Plataforma():

    def __init__(self):
        self.ancho = 200
        self.alto = 20

        self.posX = self.randomPosX()
        self.posY = altoPantalla+self.alto
        self.distanciaNext = randint(80,200)

        self.rect = pygame.Rect(self.posX, self.posY, self.ancho, self.alto)
        self.velY = 3

    def randomPosX(self):
        cuartoDePantalla = int((anchoPantalla-self.ancho)/4)
        posX = cuartoDePantalla * randint(0, 4)
        return posX

    def setPrimerPlataforma(self):
        self.rect.right = anchoPantalla
        self.rect.top = altoPantalla + 200

    def permiteSiguientePlataforma(self):
        distanciaDelSuelo = self.posY - self.rect.top
        if distanciaDelSuelo > self.distanciaNext:
            return True
        else:
            return False

    def actualizar(self, ventana):
        self.rect.top -= self.velY
        pygame.draw.rect(ventana, blanco, self.rect)