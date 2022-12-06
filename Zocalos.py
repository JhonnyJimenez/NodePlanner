from collections import OrderedDict
from Seriabilizador import Serializable
from GraficosDeZocalos import GraficosDeZocalos


Izquierda_arriba = 1
Izquierda_abajo = 2
Derecha_arriba = 3
Derecha_abajo = 4

DEBUG = False

class Zocalo(Serializable):
	def __init__(self, nodo, indice, posicion, tipo_zocalo=1, multiconexion=True):
		super().__init__()
		
		self.nodo = nodo
		self.indice = indice
		self.posicion = posicion
		self.tipo_zocalo = tipo_zocalo
		self.esmulticonexion = multiconexion
		
		if DEBUG:
			self.debugnames(posicion)
			print("Zócalo", self.indice, "ubicado", self.nposition, "del", self.nodo.titulo, self.nodo, )
		
		self.GraficosZocalos = GraficosDeZocalos(self, self.tipo_zocalo)
		
		self.GraficosZocalos.setPos(*self.nodo.obtener_posicion_zocalo(indice, posicion))
		
		self.Zocaloconexiones = []
	
	def __str__(self):
		return "<Zócalo %s %s..%s>" % ("multiconexion" if self.esmulticonexion else "de conexion única", hex(id(self))[2:5], hex(id(self))[-3:])
	
	def posicion_zocalo(self):
		if DEBUG: print("   GSP:", self.indice, self.posicion, "Nodo:", self.nodo)
		res =  self.nodo.obtener_posicion_zocalo(self.indice, self.posicion)
		if DEBUG: print("   res:", res)
		return res
		
	def agregar_conexion(self, conexion):
		self.Zocaloconexiones.append(conexion)
	
	def quitar_conexiones(self, conexion):
		if conexion in self.Zocaloconexiones: self.Zocaloconexiones.remove(conexion)
		else: print("!A:", "Zocalo::QuitarConexion", "Se desea remover la conexion", conexion, "de self.conexiones, pero no está en la lista")
		
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
				
	def quitar_todas_las_conexiones(self):
		while self.Zocaloconexiones:
			conexion = self.Zocaloconexiones.pop(0)
			conexion.quitar()
		#self.Zocaloconexiones.clear()
		
				
	# def tieneconexiones(self):
	#	return self.conexiones is not None
	
	def serializacion(self):
		return OrderedDict([
			('id', self.id),
			('Indice', self.indice),
			('Multiconexion', self.esmulticonexion),
			('Posicion', self.posicion),
			('Tipo_de_zocalo', self.tipo_zocalo),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		if restaure_id: self.id = data['id']
		self.esmulticonexion = data['Multiconexion']
		hashmap[data['id']] = self
		return True