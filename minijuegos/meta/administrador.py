import pygame
from minijuegos.meta import pause
from minijuegos.constantes import color

class Administrador():

	def __init__(self):

		self._enJuego = True
		self._loopContador = 0
		self._pantallaPausa = pause.Pause()

		self._score = 0
		self._reloj = 0
		self._font = pygame.font.Font('data\\font\\dpcomic.ttf', 30)

		self._sound_new_loop = pygame.mixer.Sound('data\\sound\\power_up.wav')

	def ejecutarJuego(self, juego):

		while self._enJuego and juego.get_game_state()['playing']:

			juego.process() # proceso el juego
			juego.display_frame() # lo dibujo en la pantalla

			if juego.get_game_state()['pause']:
				# si el juego esta pausado, muestro msj en pantalla
				self._pantallaPausa.display(juego.screen)
			else:
				# si no está pausado, actualizo el score
				self._update_score()

			self.display_score(juego.screen) # dibujo el score
			pygame.display.update() # actualizo la pantalla

			# reviso si el jugador está vivo
			self._enJuego = juego.get_game_state()['alive']


	def display_score(self, screen):

		score_str = str(self._score)
		while len(score_str) < 6:
			score_str = '0' + score_str

		text_obj = self._font.render(score_str,0,color.BLACK,screen)
		text_rect = text_obj.get_rect()
		text_rect.topleft = (14,14)
		screen.blit(text_obj, text_rect)

		text_obj = self._font.render(score_str,0,color.WHITE,screen)
		text_rect = text_obj.get_rect()
		text_rect.topleft = (10,10)
		screen.blit(text_obj, text_rect)

	def _update_score(self):
		tiempo_actual = pygame.time.get_ticks()
		if tiempo_actual - self._reloj > 500: # si paso mas de medio seg
			self._score += 25 * (self._loopContador+1)
			self._reloj = tiempo_actual

	def getLoopContador(self):
		return self._loopContador

	def getEnJuego(self):
		return self._enJuego

	def getScore(self):
		return self._score

	def agregarLoopContador(self):
		self._loopContador += 1

	def iniciarCronometro(self):
		self._reloj = pygame.time.get_ticks()

	def reproducirNuevoLoop(self):
		self._sound_new_loop.play()