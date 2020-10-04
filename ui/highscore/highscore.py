import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene

class HighScore(Scene):
    def __init__(self, name_score : list):
        super().__init__()
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',50)
        
        self.score_font = font.Font('data\\font\\dpcomic.ttf',35)
        
        self.name_score = name_score
    
    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._state['alive'] = False
                    
    def draw_hiscore(self):
        index = 0
        x_name = 206
        y_name = 192
        x_score = 370
        
        dy = 30
        self.screen.fill(color.BLACK)
        self._draw_text_center(self.tittle_font,'HISCORE',configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2-78)
        j = 0
        for element in self.name_score:
            if j < 5:
                name = element[0]
                score = element[1]
                str_score = str(score)
                len_score = len(str_score)
                str_score = '0'*(6-len_score) + str_score #Esto lo hago para que visualmente una puntuacion de 100 se vea de esta manera 000100.
                #python permite multiplicar caracteres, '0'*3 es lo mismo que '000'.
                
                self._draw_text(self.score_font,'{}.'.format(index+1),x_name - 30, y_name + dy*index)
                self._draw_text(self.score_font,name,x_name, y_name + dy*index)
                self._draw_text(self.score_font,str_score,x_score, y_name + dy*index)
                #Uso a dy para dejar espacio entre las puntuaciones
                index+=1
            j+=1
            
    def display_frame(self):
        self.draw_hiscore()
        #Aca separe el dibujado de la actualizacion de la pantalla, para poder incorporarlo al menu
        self._clock.tick(60)
        display.update()
        
    def _draw_text_center(self, font, text : str, x : int, y : int):
        text_Obj = font.render(text,0,color.WHITE,self.screen)
        text_rect = text_Obj.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_Obj, text_rect)
        return text_rect

def main(name_score):
    high_score = HighScore(name_score)
    while high_score._state['alive']:
        high_score.process()
        high_score.display_frame()
# ui.highscore.highscore