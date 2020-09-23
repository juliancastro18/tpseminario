import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene
from ui.input_box import InputBox
from ui.menu.menu import Menu
class GameOver(Scene):
    def __init__(self, score : int):
        super().__init__()
        self.input_box = InputBox(300,215,30,60,size_font=25, limit_char='|')
        self.tittle_text = "Game over"
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',50)
        self.name_font = font.Font('data\\font\\dpcomic.ttf',25)
        self.score_font = font.Font('data\\font\\dpcomic.ttf',20)
        
        self.score = score
        
    
    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.input_box.handle_event(event)

        self.input_box.update()

        
    def display_frame(self):
        self.screen.fill(color.BLACK)
        self.draw_texts()
        pygame.display.flip()
        self._clock.tick(self._fps)
        
    def draw_texts(self):
        # self.screen.fill(color.BLACK)
        
        self.input_box.draw(self.screen)
        
        
        end = self.input_box.end
        
        self._draw_text_center(self.tittle_font,self.tittle_text,configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2 - 70)
        self._draw_text(self.name_font,"NAME: ",240,220)
        self._draw_text(self.name_font,"SCORE: {}".format(self.score),240,280)
        
    def _draw_text_center(self, font, text : str, x : int, y : int):
        text_Obj = font.render(text,0,color.WHITE,self.screen)
        text_rect = text_Obj.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_Obj, text_rect)
        return text_rect

def main(score, menu : Menu):
    """[summary]

    Args:
        score ([int]): [score of the player]

    Returns:
        [Tuple]: [name of the player and save the score or dont save this]
    """
    # pygame.init()
    my_end = GameOver(score)
    ubicador = menu.game_over(my_end)
    menu.transicion(ubicador=ubicador,funcion=my_end.draw_texts,bola_visible=False)
    
    
    name = my_end.input_box.text
    # menu.transicion()
    return (name, my_end.input_box.save)

