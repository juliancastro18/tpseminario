import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene

class HighScore(Scene):
    def __init__(self, name_score : list):
        super().__init__()
        # self.title_txt = 'HIGH SCORE'
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',50)
        
        self.score_font = font.Font('data\\font\\dpcomic.ttf',25)
        self.name_score = name_score
    
    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._state['alive'] = False

    def display_frame(self):
        index = 0
        x_name = 240
        y_name = 200
        x_score = 360
        y_score = 200
        
        dy = 20
        self.screen.fill(color.BLACK)
        self._draw_text_center(self.tittle_font,'Hiscore',configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2-70)
        self._draw_text(self.score_font, 'NAME', x_name, y_name)
        self._draw_text(self.score_font,'SCORE',x_score,y_name)
        j = 0
        for element in self.name_score:
            if j < 5:
                name = element[0]
                score = element[1]
                str_score = str(score)
                len_score = len(str_score)
                str_score = '0'*(6-len_score) + str_score
                
                self._draw_text(self.score_font,'{}.'.format(index+1),x_name - 20,y_name + 30 + dy*index)
                self._draw_text(self.score_font,name,x_name,230 + dy*index)
                self._draw_text(self.score_font,str_score,x_score,y_score + 30 + dy*index)
                index+=1
            j+=1
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