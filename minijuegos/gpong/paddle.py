import pygame
from minijuegos.constantes import color, configuration
from minijuegos.formas.barra import *


class Paddle(Barra):
    def __init__(self,posXY,largo,vel_bola):
        super().__init__(True, posXY, largo)
        self.speed = vel_bola-2
        
    def update(self):
        pass
        







        
        
            





    
