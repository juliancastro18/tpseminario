import pygame
from pygame import draw
import MiniJuegos.configuration
class Square():
    _MAX_SPEED = 1
    def __init__(self, color = (0,0,0), pos = (0,0)):
        self.__color = color
        self.__pos = pos
        self.__width = 25
        self.__height = 25
        self.__speed_x = Square._MAX_SPEED
        self.__speed_y = 0
        self.collider = pygame.Rect(0,0,0,0)
    
    def get_pos(self):
        return self.__pos
    
    def get_speed(self):
        return (self.__speed_x, self.__speed_y)
    
    def set_speed(self, speed_x : int, speed_y : int):
        self.__speed_x = speed_x
        self.__speed_y = speed_y
    
    def update(self):
        self.__pos = (self.__pos[0] + self.__speed_x, self.__pos[1] + self.__speed_y )

    
    def draw(self, screen):
        self.out_screen()
        self.collider = draw.rect(screen,self.__color,(self.__pos[0],self.__pos[1],self.__width,self.__height))

    def out_screen(self):
        if self.__pos[0]<0:
            self.__pos = (MiniJuegos.configuration.SCREEN_WIDTH, self.__pos[1])
            
        if self.__pos[0]>MiniJuegos.configuration.SCREEN_WIDTH:
            self.__pos = (0, self.__pos[1])
            
        if self.__pos[1]<0:
            self.__pos = (self.__pos[0], MiniJuegos.configuration.SCREEN_HEIGHT)
            
        if self.__pos[1]>MiniJuegos.configuration.SCREEN_HEIGHT:
            self.__pos = (self.__pos[0],0)
    
    