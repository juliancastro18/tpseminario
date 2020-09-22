import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene

class HighScore(Scene):
    def __init__(self, name_score : list):
        super().__init__()
        self.title_txt = 'HIGH SCORE'
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',120)
        
        self.score_font = font.Font('data\\font\\dpcomic.ttf',40)
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
        self.screen.fill(color.BLACK)
        self._draw_text(self.tittle_font,'HIGH SCORE',70,20)
        self._draw_text(self.score_font, 'NAME', 200, 160)
        self._draw_text(self.score_font,'|',362,160)
        self._draw_text(self.score_font,'|',362,180)
        self._draw_text(self.score_font,'SCORE',375,160)
        for i in range(22):
            self._draw_text(self.score_font,'_',120 + i*20, 165)
            
        for element in self.name_score:
            name = element[0]
            score = element[1]
            self._draw_text(self.score_font,'{}.'.format(index+1),165,200 + 40*index)
            self._draw_text(self.score_font,name,200,200 + 40*index)
            self._draw_text(self.score_font,'|',362,200 + 30 *index)
            self._draw_text(self.score_font,'|',362,200 + 40 *index)
            self._draw_text(self.score_font,str(score),375,200 + 40*index)
            index+=1
        self._clock.tick(60)
        display.update()

def main(name_score):
    high_score = HighScore(name_score)
    while high_score._state['alive']:
        high_score.process()
        high_score.display_frame()