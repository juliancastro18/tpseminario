import pygame, random
from minijuegos.constantes import configuration, tamformas
from minijuegos.grapidroll.plataforma import *

class PlataformaMovil(Plataforma):

    def __init__(self, velY, largo = None):

        super().__init__(velY, largo)

        random_bit = random.getrandbits(1)
        self._velX = self._velY*2
        self._distanciaNext = randint(80,200)
        self._esDerecha = bool(random_bit)
        self._sound_lr = pygame.mixer.Sound('data\\sound\\movil_lr.wav')
        self._sound_rl = pygame.mixer.Sound('data\\sound\\movil_rl.wav')

        self._playSound()

    def update(self, ventana):

        # si la plataforma ya no se ve en pantalla horizontalmente
        # la hago aparecer del otro lado
        if self._rect.right < 0:
            self._rect.left = configuration.SCREEN_WIDTH
            self._playSound()
        elif self._rect.left > configuration.SCREEN_WIDTH:
            self._rect.right = 0
            self._playSound()

        # la muevo para el lado correspondiente
        if self._esDerecha:
            self._rect.right += self._velX
        else:
            self._rect.left -= self._velX

        super().update(ventana)

    def _playSound(self):
        if self._esDerecha == True:
            self._sound_lr.set_volume(self._getVolumen())
            self._sound_lr.play()
        else:
            self._sound_rl.set_volume(self._getVolumen())
            self._sound_rl.play()

    def _getVolumen(self):
        volumen = 0

        centro = int(configuration.SCREEN_HEIGHT/2)
        posPlat = self.getTop() + int(tamformas.BARRA_LADO_MENOR/2)
        distancia_al_centro = abs(centro - posPlat)

        if posPlat == centro:
            volumen = 1
        else:
            distancia = centro - distancia_al_centro
            volumen = distancia/centro

        return volumen