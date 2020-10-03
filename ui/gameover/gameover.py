import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene
from ui.input_box import InputBox
from ui.menu.menu import Menu

class GameOver(Scene):
    def __init__(self, score : int, top : bool):
        super().__init__()
        self.input_box = InputBox(configuration.SCREEN_WIDTH//2+10,configuration.SCREEN_HEIGHT//2+70,30,60,size_font=30, limit_char='|')
        self.tittle_text = "GAME OVER"
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',70)
        self.name_font = font.Font('data\\font\\dpcomic.ttf',30)
        self.rect_block = pygame.Rect(0, 340, 640, 100) 
        
        self.score = score
        self.top = top
        
    
    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.top:
                self.input_box.handle_event(event)
            else:
                if event.type == pygame.KEYDOWN:
                    self.input_box.end=True
        if self.top:
            self.input_box.update()

        
    def display_frame(self):
        self.screen.fill(color.BLACK)
        self.draw_texts()
        pygame.display.flip()
        self._clock.tick(self._fps)
        
    def draw_texts(self):
        
        self.input_box.draw(self.screen)
        pygame.draw.rect(self.screen, color.BLACK, self.rect_block) #para tapar lo que sobresale del "|"
        self._draw_text_center(self.tittle_font,self.tittle_text,configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2-70)

        if self.top:
            self._draw_text_center(self.name_font,"NEW HISCORE!",configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2-10)
        else:
            self._draw_text_center(self.name_font,"YOUR SCORE",configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2-10)
        self._draw_text_center(self.tittle_font,"{}".format(self.score),configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2+30)

        if self.top:
            self._draw_text(self.name_font,"ENTER NAME: ",174,configuration.SCREEN_HEIGHT//2+75)
        else:
            self._draw_text_center(self.name_font,"PRESS ANY KEY",configuration.SCREEN_WIDTH//2,configuration.SCREEN_HEIGHT//2+90)
        
    def _draw_text_center(self, font, text : str, x : int, y : int):
        text_Obj = font.render(text,0,color.WHITE,self.screen)
        text_rect = text_Obj.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_Obj, text_rect)
        return text_rect

def main(score, menu : Menu, top : bool):
    """[summary]

    Args:
        score ([int]): [score of the player]

    Returns:
        [Tuple]: [name of the player and save the score or dont save this]
    """
    # pygame.init()
    my_end = GameOver(score, top)
    ubicador = menu.game_over(my_end)
    menu.transicion(ubicador=ubicador,funcion=my_end.draw_texts,bola_visible=False)
    
    
    name = my_end.input_box.text
    return (name, my_end.input_box.save)

