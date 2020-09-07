import pygame

anchoPantalla, altoPantalla = 640, 480
blanco = (255,255,255)
negro = (0,0,0)

class Bola():
    
    radio = 14

    def __init__(self, posX, posY):

        self.rect = pygame.Rect(posX, posY, self.radio*2, self.radio*2) # rectángulo en el que se inscribe el círculo

        self.velYInicial = 0.5
        self.velY = 8
        self.velX = 10

    def actualizar(self, ventana, enPausa):
        if not enPausa:
            # aceleracion inicial
            if self.velYInicial < self.velY:
                self.rect.top += self.velYInicial
                self.velYInicial = self.velYInicial * 1.04
            else:
                self.rect.top += self.velY

            # si la bola no esta en la pantalla, se termina el juego
            if self.rect.bottom < 0 or self.rect.top > altoPantalla:
                return False

        pygame.draw.circle(ventana, blanco, self.rect.center, self.radio)
        return True

    def desplazamientoHorizontal(self, esDerecha):
        if esDerecha:
            self.rect.right += self.velX
            if self.rect.right > anchoPantalla:
                self.rect.right = anchoPantalla

        else:
            self.rect.left -= self.velX
            if self.rect.left < 0:
                self.rect.left = 0

    def setEnPlataforma(self, posY):
        if posY >= (self.rect.bottom-self.velY-4): # agrego esta comparación para evitar que tenga en cuenta colisiones laterales
            self.rect.bottom = posY - self.velY +1 # seteo el inferior de la bola para que coincida con el superior de la plataforma

    def posicionXY(self):
        return self.rect.center