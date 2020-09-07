import pygame
from pygame import draw, mixer
from MiniJuegos.Clases_Snake.square import Square
import MiniJuegos.color

class Snake():
    _MAX_SPEED = 1
    def __init__(self):
        self.__head = Square(color=MiniJuegos.color.WHITE,pos=(50,10))
        self.body = []
        self.__initial_body()
        self.__is_alive = True
        self.sounds = []
        self.load_sounds()

    def __initial_body(self):
        self.body.insert(0, self.__head)
        self.body.insert(0, Square(color=MiniJuegos.color.WHITE,pos=(25,10)))
        self.body.insert(0, Square(color=MiniJuegos.color.WHITE,pos=(0,10)))
        
    def load_sounds(self):
        self.sounds.append(mixer.Sound('data\\sound\\coin.wav'))
    def get_head(self):
        return self.__head
    
    def add_square(self):
        pos = self.body[0].get_pos()
        speed = self.body[0].get_speed()
        pos = self.relative_to_speed(speed, pos)
        self.body.insert(0, Square(color=MiniJuegos.color.WHITE,pos = pos))
        self.sounds[0].play()

    def relative_to_speed(self, speed, pos):
        #Si el ultimo se esta moviendo a la derecha, el nuevo se pondra a 25 unidades(x) y respetara la altura de el ultimo
        #[nuevo][ultimo]
        if speed[0]==1:
            pos = (pos[0]-25, pos[1])
        
        #Si el ultimo se esta moviendo a la izquierda, el nuevo se pondra a 25 unidades(x) y respetara la altura de el ultimo
        #[ultimo][nuevo]   
        if speed[0]==-1:
            pos = (pos[0]+25, pos[1])
            
        else:
            #Si el ultimo se esta moviendo hacia abajo, el nuevo respetara la x y se pondra a 25 unidades[y]
            #[nuevo]
            #[ultimo] 
            if speed[1] == 1:
                pos = (pos[0], pos[1]-25)
            
            #Si el ultimo se esta moviendo hacia arriba, el nuevo respetara la x y se pondra a 25 unidades[y]
            #[ultimo]
            #[nuevo]
            if speed[1] == -1:
                pos = (pos[0], pos[1]+25)
        return pos
    
    def update_head(self, key):
        #La cabeza depende del input
        self.__change_direction(key)
    
    def update(self,key):
        same_speed_x = self.__head.get_speed()[0] == self.body[len(self.body)-2].get_speed()[0] 
        same_speed_y = self.__head.get_speed()[1] == self.body[len(self.body)-2].get_speed()[1]
        
        #Esto lo hago para evitar bugs
        if same_speed_x:
            self.update_head(key)
        elif same_speed_y:
            self.update_head(key)
            
        #cada parte depende de la siguiente y copia su velocidad(todas excepto la cabeza)
        for index in range(len(self.body)-1):
            self.change_speed(index)
            self.body[index].update()
        self.__head.update()
        return self.__is_alive

    def change_speed(self, index):
        #Es un caos ahre, pero permite que las partes sigan a la que les corresponde
        
        if self.body[index].get_pos()[0] == self.body[index + 1].get_pos()[0]:
            if self.body[index + 1].get_speed()[1] == -Snake._MAX_SPEED:
                self.body[index].set_speed(0,-Snake._MAX_SPEED)
            elif self.body[index + 1].get_speed()[1] == Snake._MAX_SPEED:
                self.body[index].set_speed(0,Snake._MAX_SPEED)
        if self.body[index].get_pos()[1] == self.body[index + 1].get_pos()[1]:
            if self.body[index + 1].get_speed()[0] == -Snake._MAX_SPEED:
                self.body[index].set_speed(-Snake._MAX_SPEED,0)
            elif self.body[index + 1].get_speed()[0] == Snake._MAX_SPEED:
                self.body[index].set_speed(Snake._MAX_SPEED,0)
                
        #Revisa la colision de la cabeza con el resto del cuerpo
        if self.__head.collider.colliderect(self.body[index].collider):
            if not self.body[index] == self.body[len(self.body)-2]:
                self.__is_alive = False
              
    def __change_direction(self,key : int):
        if(key == pygame.K_w):
            if self.__head.get_speed()[1] == Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(0,-Snake._MAX_SPEED)
        if(key == pygame.K_s):
            if self.__head.get_speed()[1] == -Snake._MAX_SPEED:
                Snake.is_alive = False
            else:
                self.__head.set_speed(0,Snake._MAX_SPEED)
        if(key == pygame.K_a):
            if self.__head.get_speed()[0] == Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(-Snake._MAX_SPEED, 0)
        if(key == pygame.K_d):
            if self.__head.get_speed()[0] == -Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(Snake._MAX_SPEED, 0)
    
    def draw(self, screen):
        for index in range(len(self.body)):
            self.body[index].draw(screen)
    def get_len(self):
        return len(self.body)
        
    
    