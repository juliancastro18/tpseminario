import sys
import pygame
from pygame import draw, display, event, time, font, mixer
from minijuegos.constantes import configuration, color
from minijuegos.scene import Scene
from ui.input_box import InputBox
class GameOver(Scene):
    def __init__(self, score : int):
        super().__init__()
        self.input_box = InputBox(260,120,30,60)
        self.tittle_text = "GAME OVER"
        self.tittle_font = font.Font('data\\font\\dpcomic.ttf',100)
        self.name_font = font.Font('data\\font\\dpcomic.ttf',55)
        self.score_font = font.Font('data\\font\\dpcomic.ttf',20)
        
        self.game_over_clip = mixer.Sound('data\\sound\\gameOver.ogg')
        self.game_over_clip.play()
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
        
        self.input_box.draw(self.screen)
        
        
        end = self.input_box.end
        
        self._draw_text(self.tittle_font,self.tittle_text,105,20)
        self._draw_text(self.name_font,"NAME: ",105,130)
        self._draw_text(self.name_font,"SCORE: {}".format(self.score),105,200)
        
        pygame.display.flip()
        self._clock.tick(self._fps)

def main(score):
    """[summary]

    Args:
        score ([int]): [score of the player]

    Returns:
        [Tuple]: [name of the player and save the score or dont save this]
    """
    pygame.init()
    my_end = GameOver(score)
    end = False
    while not end:
        my_end.process()
        my_end.display_frame()
        end = my_end.input_box.end
    name = my_end.input_box.text
    return (name, my_end.input_box.save)

