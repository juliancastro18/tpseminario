import random
import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.formas.bola import Bola
from minijuegos.gsnake.snake import Snake, Square
from minijuegos.scene import Scene

class Game(Scene):
    def __init__(self, player_pos = (0,0), ball_position = None, loop = 0):
        super().__init__()
        self._state = {'alive':True, 'playing':True, 'pause':False}
        self.__clock = time.Clock()
        self.screen = display.set_mode(size=(configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT))
        
        self.__snake = Snake(pos=player_pos)
        self.__green_squares = []
        if ball_position==None:
            self.__green_squares.append(Bola((100,100)))
        else:
            self.__green_squares.append(Bola(posXY=ball_position))
        
        self.time = 0
        self.limit_time = 3000 + 200*loop
        self.extra_speed = 20*loop
        
        self.flicker = False

        self.font = font.Font('data\\font\\dpcomic.ttf', 20)
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        
        self.win = False
        self.score_to_win = 14 + loop*1
        self.extra_score = loop
        self.sounds = []
        self.load_sounds()

        
    def load_sounds(self):
        self.sounds.append(mixer.Sound('data\\sound\\power_up.wav'))
  
    def get_game_state(self):
        return self._state
    
    def process(self):
        for event_ in event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_ESCAPE:
                    self._state['pause'] = not self._state['pause']
            if event_.type == pygame.KEYUP:
                pass

        if not self._state['pause']:
            # LOGIC ZONE
            self._state["alive"] = self.__snake.update()

            
            
            if self.__snake.get_head().collider.colliderect(self.__green_squares[0]):
                self.__green_squares.pop(0)
                self.__snake.add_square()
                self._score = 10# + 1 *self.extra_score
            

            if len(self.__snake.body) > self.score_to_win:
                self._state['playing'] = False
            else:
                if len(self.__green_squares)==0:
                    self.spawn_food()

            self.update_score_text()

           
            

    def update_score_text(self):
        self.score_text = self.font.render('Score: {}'.format(self.__snake.get_len()-3),True,color.WHITE)
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (40,20)
        
            
        
    def display_frame(self):
        self.screen.fill(color.BLACK)
        if not self.flicker:
            for element in self.__green_squares:
                    element.draw(self.screen)
        self.__snake.draw(self.screen, pause=self._state['pause'])
        self.__clock.tick(300 + self.extra_speed)
        
        
    def spawn_food(self):
        if len(self.__green_squares)==0:
            x = random.randint(20,configuration.SCREEN_WIDTH - 50)
            y = random.randint(20,configuration.SCREEN_HEIGHT - 50)
            self.__green_squares.append(Bola((x,y)))

    def get_last_food(self):
        return self.__green_squares[0]

def loop():
    pygame.init()
    snake = Game(player_pos=(300,300))
    while snake.get_game_state()['playing']:
        snake.process()
        snake.display_frame()
        pygame.display.update()
        
# loop()
#minijuegos.gsnake.snake_game