from GraficosDeZocalos import GraficosDeZocalos


Izquierda_arriba = 1
Izquierda_abajo = 2
Derecha_arriba = 3
Derecha_abajo = 4

DEBUG = False

class Zocalo:
	def __init__(self, nodo, indice, posicion, tipo_zocalo=1):
		
		self.nodo = nodo
		self.indice = indice
		self.posicion = posicion
		self.tipo_zocalo = tipo_zocalo
		
		if DEBUG:
			self.debugnames(posicion)
			print("Zócalo", self.indice, "ubicado", self.nposition, "del", self.nodo.titulo, self.nodo, )
		
		self.GraficosZocalos = GraficosDeZocalos(self, self.tipo_zocalo)
		
		self.GraficosZocalos.setPos(*self.nodo.obtener_posicion_zocalo(indice, posicion))
		
		self.conexion = None
	
	def __str__(self):
		return "<Zócalo %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
	
	def posicion_zocalo(self):
		if DEBUG: print("   GSP:", self.indice, self.posicion, "Nodo:", self.nodo)
		res =  self.nodo.obtener_posicion_zocalo(self.indice, self.posicion)
		if DEBUG: print("   res:", res)
		return res
		
	def conexion_conectada(self, conexion=None):
		self.conexion = conexion
		
	if DEBUG:
		def debugnames(self, posicion):
			if self.posicion == 1:
				self.nposition = "arriba a la izquierda"
			elif posicion == 2:
				self.nposition = "abajo a la izquierda"
			elif self.posicion == 3:
				self.nposition = "arriba a la derecha"
			elif self.posicion == 4:
				self.nposition = "abajo a la derecha"
			else:
				self.nposition = "en una posición desconocida"
				
	def tieneconexiones(self):
		return self.conexion is not None