import pygame
from MiniJuegos import color, forma, configuration
from random import randint

class Plataforma():

    def __init__(self):
        self.ancho = forma.BARRA_LADO_MAYOR
        self.alto = forma.BARRA_LADO_MENOR
        self.ultimaPlataforma = False

        self.posX = self.randomPosX()
        self.posY = configuration.SCREEN_HEIGHT+self.alto
        self.distanciaNext = randint(80,200)

        self.rect = pygame.Rect(self.posX, self.posY, self.ancho, self.alto)
        self.velY = 3

    def randomPosX(self):
        cuartoDePantalla = int((configuration.SCREEN_WIDTH-self.ancho)/4)
        posX = cuartoDePantalla * randint(0, 4)
        return posX

    def setPrimerPlataforma(self):
        self.rect.right = configuration.SCREEN_WIDTH
        self.rect.top = configuration.SCREEN_HEIGHT + 200

    def setUltimaPlataforma(self):
        self.rect.left = (configuration.SCREEN_WIDTH/2) - (self.ancho/2)
        self.ultimaPlataforma = True
        self.distanciaNext = 200

    def permiteSiguientePlataforma(self):
        distanciaDelSuelo = self.posY - self.rect.top
        if distanciaDelSuelo > self.distanciaNext:
            return True
        else:
            return False

    def actualizar(self, ventana, enPausa):
        if not enPausa:
            if self.ultimaPlataforma == True and self.rect.top < configuration.SCREEN_HEIGHT - 80:
                self.velY = 0
            self.rect.top -= self.velY

        pygame.draw.rect(ventana, color.WHITE, self.rect)