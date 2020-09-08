import MiniJuegos.configuration
import MiniJuegos.color
import pygame

class Scene():

	def __init__(self):
		self.screen = display.set_mode(size = (MiniJuegos.configuration.SCREEN_WIDTH,configuration.SCREEN_HEIGHT))
		self._alive = True
		self._clock = time.Clock()
		self._fps = 30

	def process(self):
		pass

	def display_frame(self):
		pass

	def _draw_text(self, font, text : str, x : int, y : int):
		text_Obj = font.render(text,1,color.WHITE,self.screen)
		text_rect = text_Obj.get_rect()
		text_rect.topleft = (x,y)
		self.screen.blit(text_Obj, text_rect)