# esta clase que se estructura como un juego, toma por parametro 2 barras y 1 bola
# y las mueve desde su posicion actual hasta la posicion indicada
# realizando un efecto de aceleración/desaceleración
# si no se le pasan elementos, por defecto los crea en el centro
import pygame, sys, math
from pygame.locals import *
from minijuegos.scene import *
from minijuegos.formas import *
from minijuegos.constantes import color, tamformas, configuration


class UbicadorPong(Scene):

	# distancia_final_screen_left es la distancia a la que quedará la barra izq del borde izq de la pantalla
	# fondo_transparente True se usa si se combina con otra screen
	# bloqueo se usa cuando se combina con otra screen y se quiere tapar lo que esta atrás al juntarse las barras
	def __init__(self, distancia_final_screen_left = None, barras : tuple = None, bola_param = None,
		        fondo_transparente = False, bloqueo = False, tick = True, barras_desde_afuera = False):

		super().__init__()
		self._barra_izquierda = None
		self._barra_derecha = None
		self._barras_desde_afuera = barras_desde_afuera
		self._set_barras(barras)

		self._bloqueo_izq = None
		self._bloqueo_der = None
		self._set_bloqueo(bloqueo)

		self._pos_inicial_izq = self._barra_izquierda.getRect().left
		self._pos_final_izq = None
		if distancia_final_screen_left is not None:
			self._pos_final_izq = distancia_final_screen_left
		else:
			self._pos_final_izq = (configuration.SCREEN_WIDTH/2) - (tamformas.BARRA_LADO_MENOR/2)

		self._vel_actual = 0
		self._vel_max = 4
		self._distancia_aceleracion = 40
		self._porcentaje_vel = 0

		self._bola = None
		self._set_bola(bola_param)
		self._bola_visible = True
		
		self._tick = tick
		self._fondo_transparente = fondo_transparente
		self._in_out = True

		if self._barra_izquierda.getRect().left < self._pos_final_izq:
			self._in_out = False

	def process(self):

		if self._tick:
			self._clock.tick(self._fps)  # defino 60 frames por segundo como maximo

        # para cada evento que reciba pygame...
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

		self.mover_formas()
		
		if self._pos_final_izq == self._barra_izquierda.getRect().left:
			self._state['playing'] = False
		


	def display_frame(self):

		if not self._fondo_transparente:
			self.screen.fill(color.BLACK)

		if self._bola_visible:
			self._bola.draw(self.screen)

		if self._bloqueo_izq is not None:
			pygame.draw.rect(self.screen, color.BLACK, self._bloqueo_izq)
			pygame.draw.rect(self.screen, color.BLACK, self._bloqueo_der)

		self._barra_izquierda.draw(self.screen)
		self._barra_derecha.draw(self.screen)


	def _set_barras(self, barras):
		if barras == None:
			if self._barras_desde_afuera:
				centro_barra_x = -tamformas.BARRA_LADO_MENOR
			else:
				centro_barra_x = (configuration.SCREEN_WIDTH/2) - (tamformas.BARRA_LADO_MENOR/2)

			centro_barra_y = (configuration.SCREEN_HEIGHT/2) - (tamformas.BARRA_LADO_MAYOR/2)

			self._barra_izquierda = barra.Barra(True,(centro_barra_x, centro_barra_y))

			if self._barras_desde_afuera:
				centro_barra_x = configuration.SCREEN_WIDTH

			self._barra_derecha = barra.Barra(True,(centro_barra_x, centro_barra_y))

		else:

			if barras[0].getPosXY()[0] < barras[1].getPosXY()[0]:
				self._barra_izquierda = barras[0]
				self._barra_derecha = barras[1]
			else:
				self._barra_izquierda = barras[1]
				self._barra_derecha = barras[0]

	def _set_bola(self, bola_param):

		if bola_param == None:
			bola_x = (configuration.SCREEN_WIDTH/2) - tamformas.BOLA_RADIO
			bola_y = (configuration.SCREEN_HEIGHT/2) - tamformas.BOLA_RADIO
			self._bola = bola.Bola((bola_x,bola_y))
		else:
			self._bola = bola_param

	def _set_bloqueo(self, bloqueo):
		if bloqueo:
			self._bloqueo_izq = self._barra_izquierda.getRect().copy().inflate(500,0)
			self._bloqueo_der = self._barra_derecha.getRect().copy().inflate(500,0)


	def calcular_velocidad_in_out(self):
		fin_aceleracion_pos = self._pos_inicial_izq - self._distancia_aceleracion
		inicio_desaceleracion_pos = self._pos_final_izq + self._distancia_aceleracion

		if fin_aceleracion_pos <= self._barra_izquierda.getRect().left:
			self._porcentaje_vel = (self._barra_izquierda.getRect().left - fin_aceleracion_pos) / self._distancia_aceleracion
			if self._porcentaje_vel == 1:
				self._porcentaje_vel = 0.95
			self._porcentaje_vel = 1 - self._porcentaje_vel

		elif inicio_desaceleracion_pos >= self._barra_izquierda.getRect().left:
			self._porcentaje_vel = (self._barra_izquierda.getRect().left - self._pos_final_izq) / self._distancia_aceleracion

		#print(self._porcentaje_vel)
		return self._porcentaje_vel * self._vel_max

	def calcular_velocidad_out_in(self):
		fin_aceleracion_pos = self._pos_inicial_izq + self._distancia_aceleracion
		inicio_desaceleracion_pos = self._pos_final_izq - self._distancia_aceleracion

		if fin_aceleracion_pos >= self._barra_izquierda.getRect().left:
			self._porcentaje_vel = (fin_aceleracion_pos - self._barra_izquierda.getRect().left) / self._distancia_aceleracion
			if self._porcentaje_vel == 1:
				self._porcentaje_vel = 0.95
			self._porcentaje_vel = 1 - self._porcentaje_vel

		elif inicio_desaceleracion_pos <= self._barra_izquierda.getRect().left:
			self._porcentaje_vel = (self._pos_final_izq - self._barra_izquierda.getRect().left) / self._distancia_aceleracion

		#print(self._porcentaje_vel)
		return self._porcentaje_vel * self._vel_max

	def mover_formas(self):

		if self._in_out == True:
			self._vel_actual = self.calcular_velocidad_in_out() 
			self._barra_izquierda.getRect().left -= math.ceil(self._vel_actual)
			self._barra_derecha.getRect().right += math.ceil(self._vel_actual)
		else:
			self._vel_actual = self.calcular_velocidad_out_in()
			self._barra_izquierda.getRect().left += math.ceil(self._vel_actual)
			self._barra_derecha.getRect().right -= math.ceil(self._vel_actual)			

		if self._bloqueo_izq is not None:
			self._bloqueo_izq.right = self._barra_izquierda.getRect().left + 2
			self._bloqueo_der.left = self._barra_derecha.getRect().right - 2
		#print(self._vel_actual, " // ", self._barra_izquierda.getRect().left, " // ", self._barra_derecha.getRect().right)

	def get_barras(self):
		return (self._barra_izquierda, self._barra_derecha)


	def set_posicion_bola(self, posXY):
		self._bola.setPosicionXY(posXY)

	def get_posicion_bola(self):
		return self._bola.getPosicionXY()

	def desplazar_bola_x(self, x):
		self._bola.rect.left += x

	def get_bola(self):
		return self._bola

	def mostrar_bola(self):
		self._bola_visible = True

	def ocultar_bola(self):
		self._bola_visible = False

	def getIsPaused(self):
		return self._state['pause']