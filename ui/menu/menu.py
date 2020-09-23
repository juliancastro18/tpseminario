import pygame, sys
from pygame.locals import *
from minijuegos.scene import *
from minijuegos.gubicadorpong import *
from minijuegos.constantes import tamformas, configuration

class Menu(Scene):

	def __init__(self):

		super().__init__()
		self.opcion = 1
		self.pos_inicial_bola = (225,175)
		self._font_titulo = pygame.font.Font('data\\font\\dpcomic.ttf', 70)
		self._font_text = pygame.font.Font('data\\font\\dpcomic.ttf', 45)
		self._img_controles = pygame.image.load("data\\img\\ctrl.png")
		self.ubicador_pong = None

		self._desp_x = 0
		self._desplazamiento = False
		self._rect_titulo = pygame.Rect(0,0,0,0) #valores aux

		self._sonido_move = pygame.mixer.Sound('data\\sound\\menu\\move.wav')
		self._sonido_select = pygame.mixer.Sound('data\\sound\\menu\\select.wav')

	def main(self):

		self.ubicador_pong = ubicadorpong.UbicadorPong(190, fondo_transparente = True, bloqueo = True, tick = False)

		while self.get_game_state()['playing']:

			self.screen.fill(color.BLACK)
			self.process()
			self.display_frame()

			if self.pos_inicial_bola[0]+self._desp_x < configuration.SCREEN_WIDTH/2 - tamformas.BOLA_RADIO:
				self.ubicador_pong.set_posicion_bola( (self.pos_inicial_bola[0]+self._desp_x, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*self.opcion)) )
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
		self.desplazar()
		self._rect_titulo = self._draw_text_center(self._font_titulo, "5in1", configuration.SCREEN_WIDTH/2+int(self._desp_x), configuration.SCREEN_HEIGHT/2-70)
		altura_bola = self.pos_inicial_bola[1]+(tamformas.BOLA_RADIO*2)
		self._draw_text(self._font_text, "START", self._rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*1)-3)
		self._draw_text(self._font_text, "HISCORE", self._rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*2)-3)
		self._draw_text(self._font_text, "HOWTO", self._rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*3)-3)
		self._draw_text(self._font_text, "EXIT", self._rect_titulo.left, self.pos_inicial_bola[1]+((tamformas.BOLA_RADIO*2+5)*4)-3)


	def _draw_text_center(self, font, text : str, x : int, y : int):
		text_Obj = font.render(text,0,color.WHITE,self.screen)
		text_rect = text_Obj.get_rect()
		text_rect.center = (x,y)
		self.screen.blit(text_Obj, text_rect)
		return text_rect

	def seleccionar_opcion(self):
		if self.opcion == 1:
			self._desplazamiento = True
		if self.opcion == 3:
			self.transicion()
			ubicadorctrl = self.controles()
			self.transicion(ubicador=ubicadorctrl, funcion = self.imprimir_controles, bola_visible = False)
		if self.opcion == 4:
			self.transicion()
			pygame.quit()
			sys.exit()

	def desplazar(self):
		if self._desplazamiento:
			if self._desp_x == 0:
				self._desp_x = 1
			else:
				self._desp_x *= 1.2
		if self._rect_titulo.left > self.ubicador_pong._barra_derecha.getPosXY()[0]:
			self._state['playing'] = False

	def controles(self):
		ubicador_controles= ubicadorpong.UbicadorPong(190, fondo_transparente = True, bloqueo = True, tick = False)
		ubicador_controles.ocultar_bola()
		tecla_presionada = False
		while tecla_presionada != True:
			self.screen.fill(color.BLACK)
			self.imprimir_controles()
			ubicador_controles.process()
			ubicador_controles.display_frame()
			pygame.display.update()
			tecla_presionada = self.detectar_key()
		return ubicador_controles

	def imprimir_controles(self):
		self.screen.blit(self._img_controles, (210,140))

	def transicion(self, ubicador = None, funcion = None, bola_visible = True):
		if ubicador is None:
			ubicador = self.ubicador_pong

		ubicador_transicion = ubicadorpong.UbicadorPong(bola_param = ubicador.get_bola(),
			barras = ubicador.get_barras(), fondo_transparente = True, bloqueo = True)

		if bola_visible == False:
			ubicador_transicion.ocultar_bola()

		while ubicador_transicion.get_game_state()['playing']:
			self.screen.fill(color.BLACK)

			if funcion is None:
				self.display_frame()
			else:
				funcion()

			ubicador_transicion.process()
			ubicador_transicion.display_frame()
			pygame.display.update()

	def detectar_key(self):
		self._clock.tick(self._fps)

		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				return True
			else:
				return False