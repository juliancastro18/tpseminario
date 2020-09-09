import pygame
from pygame import draw
from minijuegos.gameobject import GameObject
import minijuegos.configuration
class Square(GameObject):
    _MAX_SPEED = 1
    def __init__(self, color = (0,0,0), pos = (0,0), width = 25, height = 25):
        self.__color = color
        self.__pos = pos
        self.__width = width
        self.__height = height
        self.__speed_x = Square._MAX_SPEED
        self.__speed_y = 0
        self.collider = pygame.Rect(0,0,0,0)
    
    def get_pos(self):
        return self.__pos
    def set_pos(self, x = 0, y = 0):
        self.__pos = (x,y)
    
    def get_speed(self):
        return (self.__speed_x, self.__speed_y)
    
    def set_speed(self, speed_x : int, speed_y : int):
        self.__speed_x = speed_x
        self.__speed_y = speed_y
    
    def update(self):
        self.__pos = (self.__pos[0] + self.__speed_x, self.__pos[1] + self.__speed_y )

    
    def draw(self, screen):
        result = self.out_screen()
        self.collider = draw.rect(screen,self.__color,(self.__pos[0],self.__pos[1],self.__width,self.__height))
        return result
    
    def out_screen(self):
        out = False
        if self.__pos[0]<0:
            # self.__pos = (minijuegos.configuration.SCREEN_WIDTH, self.__pos[1])
            out = True
            
        if self.__pos[0]>minijuegos.configuration.SCREEN_WIDTH - 25:
            # self.__pos = (0, self.__pos[1])
            out = True
            
        if self.__pos[1]<0:
            # self.__pos = (self.__pos[0], minijuegos.configuration.SCREEN_HEIGHT)
            out = True
            
        if self.__pos[1]>minijuegos.configuration.SCREEN_HEIGHT - 25:
            # self.__pos = (self.__pos[0],0)
            out = True
        return out

    
    