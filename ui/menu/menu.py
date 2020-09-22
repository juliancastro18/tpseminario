import pygame, sys
from pygame.locals import *
from minijuegos.scene import *
from minijuegos.gubicadorpong import *
from minijuegos.constantes import tamformas, configuration

class Menu(Scene):

	def __init__(self):

		super().__init__()
		self.opcion = 1
		self.pressed = False
		self.pos_inicial_bola = (225,175)
		self._font_titulo = pygame.font.Font('data\\font\\dpcomic.ttf', 70)
		self._font_text = pygame.font.Font('data\\font\\dpcomic.ttf', 45)
		self.ubicador_pong = None

		self._sonido_move = pygame.mixer.Sound('data\\sound\\menu\\move.wav')
		self._sonido_select = pygame.mixer.Sound('data\\sound\\menu\\select.wav')

	def main(self):

		self.ubicador_pong = ubicadorpong.UbicadorPong(190, fondo_transparente = True, bloqueo = True, tick = False)

		while self.get_game_state()['playing']:

			self.screen.fill(color.BLACK)
			self.process()
			self.display_frame()

			self.ubicador_pong.set_posicion_bola( (self.pos_inicial_bola[0], self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*self.opcion)) )
			self.ubicador_pong.process()
			self.ubicador_pong.display_frame()
			#tupla_barras = self.ubicador_pong.get_barras()

			pygame.display.update()


	def process(self):

		self._clock.tick(self._fps)

		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_UP:
					if self.opcion > 1:
						self._sonido_move.play()
						self.opcion -= 1
				if evento.key == pygame.K_DOWN:
					if self.opcion < 4:
						self._sonido_move.play()
						self.opcion += 1
				if evento.key == pygame.K_RETURN:
					self._sonido_select.play()
					self.seleccionar_opcion()

	def display_frame(self):
		rect_titulo = self._draw_text_center(self._font_titulo, "5in1", configuration.SCREEN_WIDTH/2, configuration.SCREEN_HEIGHT/2-70)
		altura_bola = self.pos_inicial_bola[1]+(tamformas.BOLA_RADIO*2)
		self._draw_text(self._font_text, "START", rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*1))
		self._draw_text(self._font_text, "HISCORE", rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*2))
		self._draw_text(self._font_text, "HOWTO", rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*3))
		self._draw_text(self._font_text, "EXIT", rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*4))


	def _draw_text_center(self, font, text : str, x : int, y : int):
		text_Obj = font.render(text,0,color.WHITE,self.screen)
		text_rect = text_Obj.get_rect()
		text_rect.center = (x,y)
		self.screen.blit(text_Obj, text_rect)
		return text_rect

	def seleccionar_opcion(self):
		if self.opcion == 1:
			self._state['playing'] = False
		if self.opcion == 4:
			self.salir()

	def salir(self):
		ubicador_salida = ubicadorpong.UbicadorPong(bola_param = self.ubicador_pong.get_bola(),
			barras = self.ubicador_pong.get_barras(), fondo_transparente = True, bloqueo = True)
		while ubicador_salida.get_game_state()['playing']:
			self.screen.fill(color.BLACK)
			self.display_frame()
			ubicador_salida.process()
			ubicador_salida.display_frame()
			pygame.display.update()
		pygame.quit()
		sys.exit()