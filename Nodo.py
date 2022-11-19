from GraficosdelNodo import GraficosdelNodo
from ContenidodelNodo import ContenidoDelNodo
from Zocalos import *


DEBUG = False


class Nodo:
	def __init__(self, escena, titulo="Nodo desconocido", entradas=[], salidas=[]):
		self.escena = escena
		self.titulo = titulo
		
		self.contenido = ContenidoDelNodo(self)
		
		self.Nodograficas = GraficosdelNodo(self)
		
		self.escena.agregarnodo(self)
		self.escena.GraficosEsc.addItem(self.Nodograficas)
		
		self.espaciadoconectores = 22
		
		# Creación de conectores para entradas y salidas de nodos.
		self.entradas = []
		self.salidas = []
		contador = 0
		for item in entradas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Izquierda_abajo, tipo_zocalo=item)
			contador += 1
			self.entradas.append(zocalos)
			
		contador = 0
		for item in salidas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Derecha_arriba, tipo_zocalo=item)
			contador += 1
			self.salidas.append(zocalos)
	
	def __str__(self):
		return "<Nodo %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
	
	@property
	def pos(self):
		return self.Nodograficas.pos()		#QPoint
	def definirposicion(self, x, y):
		self.Nodograficas.setPos(x, y)
			
	def obtener_posicion_zocalo(self, indice, posicion):
		x = 0 if (posicion in (Izquierda_arriba, Izquierda_abajo)) else self.Nodograficas.anchoNodo
		
		if posicion in (Izquierda_abajo, Derecha_abajo):
			# Comenzando desde abajo.
			y = self.Nodograficas.altoNodo - self.Nodograficas._sangria - self.Nodograficas.redondezNodo - (indice * self.espaciadoconectores)
		else:
			# Comenzando desde arriba.
			y = self.Nodograficas.alturaTituloNodo + self.Nodograficas._sangria + self.Nodograficas.redondezNodo + (indice * self.espaciadoconectores)
		
		return [x, y]
	
	def actualizarconexiones(self):
		for zocalo in self.entradas + self.salidas:
			if zocalo.tieneconexiones():
				zocalo.conexion.posiciones_actualizadas()
				
	def quitar(self):
		if DEBUG: print('> Quitando el nodo', self)
		if DEBUG: print('	Quitando todos las conexiones de los zócalos.')
		for zocalo in (self.entradas + self.salidas):
			if zocalo.tieneconexiones():
				if DEBUG: print('		Quitando', zocalo.conexion, 'del', zocalo)
				zocalo.conexion.quitar()
		if DEBUG: print('	Quitando los gráficos del nodo.')
		self.escena.GraficosEsc.removeItem(self.Nodograficas)
		self.Nodograficas = None
		if DEBUG: print('	Quitando el nodo de la escena.')
		self.escena.eliminarnodo(self)
		if DEBUG: print('	Todo salió bien.')