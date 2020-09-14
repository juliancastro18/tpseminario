import pygame
from minijuegos.meta import pause

class Administrador():

	def __init__(self):

		self._enJuego = True
		self._loopContador = 0
		self._pantallaPausa = pause.Pause()
		self._score = 0
		self._subscore = 0

	def ejecutarJuego(self, juego):

	    while self._enJuego and juego.get_game_state()['playing']:
	        juego.process()
	        juego.display_frame()
	        self.display_score() # IMPLEMENTAR!
	        if juego.get_game_state()['pause']:
	            self._pantallaPausa.display(juego.screen)
	        else:
	        	self.update_score()
	        self._enJuego = juego.get_game_state()['alive']

	def display_score(self):
		pass

	def update_score(self):
		self._subscore += 1
		if self._subscore >= 30:
			self._subscore = 0
			self._score += self._loopContador * 10

	def getLoopContador(self):
		return self._loopContador

	def getEnJuego(self):
		return self._enJuego

	def agregarLoopContador(self):
		self._loopContador += 1