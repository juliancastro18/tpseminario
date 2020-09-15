import pygame
from minijuegos.constantes import configuration, color

class Pause():

	def __init__(self):
		self._font = pygame.font.Font('data\\font\\dpcomic.ttf', 80)
		self._background = pygame.image.load("data\\img\\grid.png")
		self._sound_pause = pygame.mixer.Sound('data\\sound\\pause.wav')
		self._sound_pause.set_volume(0.5)
		self._sound_pause_in = pygame.mixer.Sound('data\\sound\\pause\\sfx_sounds_pause4_in.wav')
		self._sound_pause_out = pygame.mixer.Sound('data\\sound\\pause\\sfx_sounds_pause4_out.wav')
		self._texto = "PAUSA"
		self._mostrandoTexto = False
		self._displayText = True
		self._timer = 0
  
		self.initial_pic = True


	def display(self, screen):

		self._timer += 1
		screen.blit(self._background, (0,0))
  
		if self.initial_pic:
			self.initial_pic = False
			self._sound_pause_in.play()
   
		if self._displayText:

			if self._mostrandoTexto == False:
				# self._sound_pause.play()
				
				self._mostrandoTexto = True

			text_Obj = self._font.render(self._texto,0,color.BLACK,screen)
			text_rect = text_Obj.get_rect()
			text_rect.center = ((configuration.SCREEN_WIDTH/2)+5, (configuration.SCREEN_HEIGHT/2)+5)
			screen.blit(text_Obj, text_rect)

			text_Obj = self._font.render(self._texto,0,color.WHITE,screen)
			text_rect = text_Obj.get_rect()
			text_rect.center = (configuration.SCREEN_WIDTH/2, configuration.SCREEN_HEIGHT/2)
			screen.blit(text_Obj, text_rect)
		else:
			self._mostrandoTexto = False

		if self._timer > 20:
			self._timer = 0
			self._displayText ^= True