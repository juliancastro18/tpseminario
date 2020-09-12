import random
import sys
import pygame
from pygame import draw, display, event, time, font, mixer
import minijuegos.configuration, minijuegos.color
from minijuegos.bola import Bola
from minijuegos.clasessnake.snake import Snake, Square
from minijuegos.scene import Scene
class Game(Scene):
    def __init__(self, player_pos = (0,0), ball_position = None, loop = 0):
        self.__game_state = {"done":False,"win":False, "snake_is_alive":True}
    
        self.__clock = time.Clock()
        self.__screen = display.set_mode(size=(minijuegos.configuration.SCREEN_WIDTH, minijuegos.configuration.SCREEN_HEIGHT))
        self.__snake = Snake(pos=player_pos)
        self.__green_squares = []
        if ball_position==None:
            self.__green_squares.append(Bola((100,100)))
        else:
            self.__green_squares.append(Bola(posXY=ball_position))
        
        self.__time = 0
        self.__inital_time = 7000
        self.__iteration = 1
        self.extra_speed = 10*loop
        
        self.font = font.Font('data\\font\\dpcomic.ttf', 20)
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,minijuegos.color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        self.score_to_win = 5 + loop*1
        self.sounds = []
        self.load_sounds()
        
    def load_sounds(self):
        self.sounds.append(mixer.Sound('data\\sound\\power_up.wav'))
  
    def get_game_state(self):
        return self.__game_state
    
    def process(self):
        self.__time = time.get_ticks()
        key = -1000
        for event_ in event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_ESCAPE:
                    self.__game_state["done"] = True
                key = event_.key
            if event_.type == pygame.KEYUP:
                pass
            
        # LOGIC ZONE
        self.__game_state["snake_is_alive"] = self.__snake.update()
        if self.__time > self.__inital_time * self.__iteration:
            self.__iteration+=1
            self.spawn_food()
            
        index = -1
        aux = 0
        for element in self.__green_squares:
            if self.__snake.get_head().collider.colliderect(element.rect):
                index = aux
            aux+=1
        if not index == -1:
            self.__green_squares.pop(index)
            self.__snake.add_square()
        if len(self.__snake.body) > self.score_to_win:
            self.__game_state['win'] = True
        self.update_score_text()

    def update_score_text(self):
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,minijuegos.color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        # END LOGIC ZONE
        
            
        
    def display_frame(self):
        self.__screen.fill(minijuegos.color.BLACK)
        
        for element in self.__green_squares:
            element.draw(self.__screen)
        self.__snake.draw(self.__screen)
        self.__screen.blit(self.score_text, self.textRect)
        # UPDATE
        display.flip()
        self.__clock.tick(120 + self.extra_speed * 2)
        
    def spawn_food(self):
        if len(self.__green_squares)==0:
            x = random.randint(20,minijuegos.configuration.SCREEN_WIDTH - 50)
            y = random.randint(20,minijuegos.configuration.SCREEN_HEIGHT - 50)
            self.__green_squares.append(Bola((x,y)))