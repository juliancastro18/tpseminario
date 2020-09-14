import pygame
from minijuegos.constantes import configuration, color

class Pause():

	def __init__(self):
		self._font = pygame.font.Font('data\\font\\dpcomic.ttf', 80)
		self._background = pygame.image.load("data\\img\\grid.png")
		
		self._texto = "PAUSA"
		self._displayText = True
		self._timer = 0

	def display(self, screen):

		self._timer += 1
		screen.blit(self._background, (0,0))

		if self._displayText:
			text_Obj = self._font.render(self._texto,0,color.BLACK,screen)
			text_rect = text_Obj.get_rect()
			text_rect.center = ((configuration.SCREEN_WIDTH/2)+5, (configuration.SCREEN_HEIGHT/2)+5)
			screen.blit(text_Obj, text_rect)

			text_Obj = self._font.render(self._texto,0,color.WHITE,screen)
			text_rect = text_Obj.get_rect()
			text_rect.center = (configuration.SCREEN_WIDTH/2, configuration.SCREEN_HEIGHT/2)
			screen.blit(text_Obj, text_rect)

		if self._timer > 20:
			self._timer = 0
			self._displayText ^= True