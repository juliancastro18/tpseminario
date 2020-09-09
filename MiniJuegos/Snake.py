import random
import pygame
from pygame import draw, display, event, time, font, mixer
import MiniJuegos.configuration, MiniJuegos.color
from MiniJuegos.Clases_Snake.snake import Snake, Square
from MiniJuegos.Scene import Scene
class Game(Scene):
    def __init__(self, player_pos = (0,0)):
        self.__game_state = {"done":False,"win":False, "snake_is_alive":True}
    
        self.__clock = time.Clock()
        self.__screen = display.set_mode(size=(MiniJuegos.configuration.SCREEN_WIDTH, MiniJuegos.configuration.SCREEN_HEIGHT))
        
        self.__snake = Snake()
        
        self.__green_squares = []
        
        
        self.__time = 0
        self.__inital_time = 7000
        self.__iteration = 1
        self.extra_speed = 0
        
        
        self.font = font.Font('data\\font\\dpcomic.ttf', 20)
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,MiniJuegos.color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        
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
                self.__game_state["done"] = True
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_ESCAPE:
                    self.__game_state["done"] = True
                key = event_.key
            if event_.type == pygame.KEYUP:
                pass
            
        # LOGIC ZONE
        self.__game_state["snake_is_alive"] = self.__snake.update(key)
        if self.__time > self.__inital_time * self.__iteration:
            self.__iteration+=1
            self.spawn_food()
            
        index = -1
        aux = 0
        for element in self.__green_squares:
            if self.__snake.get_head().collider.colliderect(element.collider):
                index = aux
            aux+=1
        if not index == -1:
            self.__green_squares.pop(index)
            self.__snake.add_square()
        self.__up_speed() 
        
        self.update_score_text()

    def update_score_text(self):
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,MiniJuegos.color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        # END LOGIC ZONE
        
    def __up_speed(self):
        if self.__snake.get_len() == 5:
            if not self.extra_speed == 20:
                self.extra_speed = 20
                self.sounds[0].play()
        elif self.__snake.get_len() == 10:
            if not self.extra_speed == 40:
                self.extra_speed = 40
                self.sounds[0].play()
        elif self.__snake.get_len() == 15:
            if not self.extra_speed == 60:
                self.extra_speed = 60
                self.sounds[0].play()
        elif self.__snake.get_len() == 25:
            if not self.extra_speed == 90:
                self.extra_speed = 90
                self.sounds[0].play()
        elif self.__snake.get_len() == 35:
            if not self.extra_speed == 120:
                self.extra_speed = 120
                self.sounds[0].play()
            
        
    def display_frame(self):
        self.__screen.fill(MiniJuegos.color.BLACK)
        
        for element in self.__green_squares:
            element.draw(self.__screen)
        self.__snake.draw(self.__screen)
        self.__screen.blit(self.score_text, self.textRect)
        # UPDATE
        display.flip()
        self.__clock.tick(120 + self.extra_speed)
        
    def spawn_food(self):
        x = random.randint(20,MiniJuegos.configuration.SCREEN_WIDTH - 20)
        y = random.randint(20,MiniJuegos.configuration.SCREEN_HEIGHT - 20)
        self.__green_squares.append(Square(color = MiniJuegos.color.WHITE, pos = (x,y)))