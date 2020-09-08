from MiniJuegos import configuration, color
import pygame

class Scene():

	def __init__(self):
		self.screen = pygame.display.set_mode(size = (configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT))
		self._state = {'alive':True, 'playing':True, 'pause':False}
		self._clock = pygame.time.Clock()
		self._fps = 60

	def process(self):
		pass

	def display_frame(self):
		pass

	def _draw_text(self, font, text : str, x : int, y : int):
		text_Obj = font.render(text,1,color.WHITE,self.screen)
		text_rect = text_Obj.get_rect()
		text_rect.topleft = (x,y)
		self.screen.blit(text_Obj, text_rect)

	def get_game_state(self):
		return self._state