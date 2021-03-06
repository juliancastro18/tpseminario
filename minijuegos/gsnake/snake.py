import pygame
from pygame import draw, mixer, time
from minijuegos.gsnake.square import Square, GameObject
from minijuegos.constantes import color

class Snake(GameObject):
    _MAX_SPEED = 1
    def __init__(self, pos=(70,25)):
        pos=pos[0] + 25, pos[1]
        self.__head = Square(color=color.WHITE,pos=pos)

        self.__eyes = (
            Square(color=color.BLACK, pos=self.__head.get_pos(), width=5,height=5),
            Square(color=color.BLACK, pos=self.__head.get_pos(), width=5,height=5)
        )

        self.body = []
        self.__initial_body(x=pos[0],y=pos[1])
        self.__is_alive = True
        self.sounds = []
        self.load_sounds()

        self.time = -1
        self.iteration = 1

    def __initial_body(self,x = 75, y = 25):
        self.body.insert(0, self.__head)
        for i in range(25,101,25):
            self.body.insert(0, Square(color=color.WHITE,pos=(x-i,y)))
        
    def load_sounds(self):
        self.sounds.append(mixer.Sound('data\\sound\\coin.wav'))
        
    def get_head(self):
        return self.__head
    
    def add_square(self):
        pos = self.body[0].get_pos()
        speed = self.body[0].get_speed()
        pos = self.relative_to_speed(speed, pos)
        self.body.insert(0, Square(color=color.WHITE,pos = pos))
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
    
    def update_head(self):
        #La cabeza depende del input
        self.__change_direction()
    
    def update(self):
        same_speed_x = self.__head.get_speed()[0] == self.body[len(self.body)-2].get_speed()[0] 
        same_speed_y = self.__head.get_speed()[1] == self.body[len(self.body)-2].get_speed()[1]
        
        #Esto lo hago para evitar bugs
        if same_speed_x:
            self.update_head()
        elif same_speed_y:
            self.update_head()
            
        #cada parte depende de la siguiente y copia su velocidad(todas excepto la cabeza)
        for index in range(len(self.body)-1):
            self.change_speed(index)
            self.body[index].update()
        self.__head.update()
        
        
        #Esto es para que los ojos sigan bien a la cabeza
        head_speed_x, head_speed_y = self.__head.get_speed()
        head_x, head_y = self.__head.get_pos()
        index = 0
        for eye in self.__eyes:
            eye.set_speed(head_speed_x,head_speed_y)
            if head_speed_x>0:
                eye.set_pos(head_x + 14,head_y + 2 + index*15)
            elif head_speed_x<0:
                eye.set_pos(head_x + 6 ,head_y + 2 + index*15)
            elif head_speed_y<0:
                eye.set_pos(head_x + 2 + index*15 , head_y + 4) 
            elif head_speed_y>0:
                eye.set_pos(head_x + 2 + index*15 , head_y + 12)
            index +=1
            eye.update()
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
              
    def __change_direction(self):
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            if self.__head.get_speed()[0] == Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(-Snake._MAX_SPEED, 0)
        if key_input[pygame.K_RIGHT]:
            if self.__head.get_speed()[0] == -Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(Snake._MAX_SPEED, 0)
        elif key_input[pygame.K_UP]:
            if self.__head.get_speed()[1] == Snake._MAX_SPEED:
                Snake.is_alive = False
            else :
                self.__head.set_speed(0,-Snake._MAX_SPEED)
        elif key_input[pygame.K_DOWN]:
            if self.__head.get_speed()[1] == -Snake._MAX_SPEED:
                Snake.is_alive = False
            else:
                self.__head.set_speed(0,Snake._MAX_SPEED)

    def draw(self, screen, pause = False):
        # Dibuja cada parte de su cuerpo
        for index in range(len(self.body)):
            if(self.body[index].draw(screen)):
                self.__is_alive = False
                
        #Es el dibujado del parpadeo
        if pause:
            self.time=-1
        else:
            if self.time == -1:
                self.time = 700 + time.get_ticks()
            else:
                dt = self.time - time.get_ticks()
                if 1<dt<400:
                    for eye in self.__eyes:
                        eye.draw(screen)
                elif dt<0:
                    self.time=-1
        
    def get_len(self):
        return len(self.body)
    
    
        
    
    