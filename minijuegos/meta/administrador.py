import pygame
from minijuegos.meta import pause
from minijuegos.constantes import color

class Administrador():

	def __init__(self):

		# parametros generales
		self._enJuego = True
		self._loopContador = -1
		self._clock = pygame.time.Clock()

		# manejo de pausa
		self._pantallaPausa = pause.Pause()
		self.initial_pic_post_pause = False

		# manejo de puntuacion
		self._total_score = 0
		self._font = pygame.font.Font('data\\font\\dpcomic.ttf', 30)

		# otros
		self._sound_new_loop = pygame.mixer.Sound('data\\sound\\power_up.wav')
		self.game_over_clip = pygame.mixer.Sound('data\\sound\\gameOver.ogg')
		self._array_transicion = self._cargar_ruido()

	def ejecutarJuego(self, juego):

		while self._enJuego and juego.get_game_state()['playing']:

			juego.process() # proceso el juego
			juego.display_frame() # lo dibujo en la pantalla
			self._total_score += juego.get_score() * (self._loopContador+1) #actualizo score

			if juego.get_game_state()['pause']:
				# si el juego esta pausado, muestro msj en pantalla
				self._pantallaPausa.display(juego.screen)
				self.initial_pic_post_pause = True
			else:
				if self.initial_pic_post_pause:
					pygame.mixer.unpause()
					self._pantallaPausa._sound_pause_out.play()
					self.initial_pic_post_pause = False
					self._pantallaPausa.initial_pic = True

			self.display_total_score(juego.screen) # dibujo el score
			pygame.display.update() # actualizo la pantalla

			# reviso si el jugador está vivo
			self._enJuego = juego.get_game_state()['alive']

			# si el jugador perdió
			if self._enJuego == False:
				self.game_over_clip.play()
				for i in range(0,6):
					self._clock.tick(12)
					juego.display_frame()
					self.display_total_score(juego.screen)
					juego.screen.blit(self._array_transicion[i], (0,0))
					pygame.display.update()
				juego.screen.fill(color.BLACK)
				pygame.display.update()
				self._clock.tick(2)


	def display_total_score(self, screen):

		score_str = str(self._total_score)
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


	def _cargar_ruido(self):
		lista_img = []
		for i in range(0,7):
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r0.png"))
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r1.png"))
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r2.png"))
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r3.png"))
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r4.png"))
			lista_img.append(pygame.image.load("data\\img\\ruido_transicion\\r5.png"))
		return lista_img

	def getLoopContador(self):
		return self._loopContador

	def getEnJuego(self):
		return self._enJuego

	def getScore(self):
		return self._total_score

	def iniciarNuevoLoop(self):
		self._sound_new_loop.play()
		self._loopContador += 1

	def set_restart(self):
		self._enJuego = True
		self._loopContador = -1
		self._total_score = 0