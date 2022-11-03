from GraficosdelNodo import GraficosdelNodo
from ContenidodelNodo import ContenidoDelNodo
from Zocalos import *


class Nodo:
	def __init__(self, escena, titulo="Nodo desconocido", entradas=[], salidas=[]):
		self.escena = escena
		self.titulo = titulo
		
		self.contenido = ContenidoDelNodo()
		
		self.Nodograficas = GraficosdelNodo(self)
		
		self.escena.agregarnodo(self)
		self.escena.GraficosEsc.addItem(self.Nodograficas)
		
		self.espaciadoconectores = 22
		
		# Creación de conectores para entradas y salidas de nodos.
		self.entradas = []
		self.salidas = []
		contador = 0
		for item in entradas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Izquierda_abajo)
			contador += 1
			self.entradas.append(zocalos)
			
		contador = 0
		for item in salidas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Derecha_arriba)
			contador += 1
			self.salidas.append(zocalos)
			
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