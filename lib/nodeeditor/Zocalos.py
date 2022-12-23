from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficosDeZocalos import GraficosDeZocalos
from lib.nodeeditor.Utilidades import debugnames


Izquierda_arriba = 1
Izquierda_centro = 2
Izquierda_abajo = 3
Derecha_arriba = 4
Derecha_centro = 5
Derecha_abajo = 6

DEBUG = False
DEBUG_REMOVE_WARNINGS = False


class Zocalo(Serializable):
	ClaseGraficadeZocalos = GraficosDeZocalos
	
	def __init__(
			self, nodo, indice, posicion, tipo_zocalo=1, multiconexion=True, cantidad_en_el_lado_actual=1,
			esEntrada=False
			):
		super().__init__()
		
		self.nodo = nodo
		self.posicion = posicion
		self.indice = indice
		self.tipo_zocalo = tipo_zocalo
		self.cantidad_en_el_lado_actual = cantidad_en_el_lado_actual
		self.esmulticonexion = multiconexion
		self.esEntrada = esEntrada
		self.esSalida = not self.esEntrada
		
		if DEBUG:
			print("Zócalo", self.indice, "ubicado", debugnames(posicion), "del", self.nodo.titulo, self.nodo)
			
		self.GraficosZocalos = self.__class__.ClaseGraficadeZocalos(self)
		
		self.definir_posicion_del_zocalo()
		
		self.Zocaloconexiones = []
	
	def __str__(self):
		return "<Zócalo #%d %s %s..%s>" % (
			self.indice, "multiconexion" if self.esmulticonexion else "de conexion única",
			hex(id(self))[2:5], hex(id(self))[-3:]
		)
	
	def eliminarzocalo(self):
		self.GraficosZocalos.setParentItem(None)
		self.nodo.escena.GraficosEsc.removeItem(self.GraficosZocalos)
		del self.GraficosZocalos
		
	def cambiarTipoZocalo(self, nuevo_tipo_zocalo):
		if self.tipo_zocalo != nuevo_tipo_zocalo:
			self.tipo_zocalo = nuevo_tipo_zocalo
			self.GraficosZocalos.cambiarTipoZocalo()
			return True
		return False
	
	def definir_posicion_del_zocalo(self):
		self.GraficosZocalos.setPos(*self.nodo.obtener_posicion_zocalo(self.indice, self.posicion, self.cantidad_en_el_lado_actual))
	
	def posicion_zocalo(self):
		if DEBUG: print("   GSP:", self.indice, self.posicion, "Editor de nodos:", self.nodo)
		res =  self.nodo.obtener_posicion_zocalo(self.indice, self.posicion, self.cantidad_en_el_lado_actual)
		if DEBUG: print("   res:", res)
		return res
	
	def tiene_alguna_conexion(self):
		return len(self.Zocaloconexiones) > 0
	
	def estaConectado(self, conexion):
		return conexion in self.Zocaloconexiones
		
	def agregar_conexion(self, conexion):
		self.Zocaloconexiones.append(conexion)
	
	def quitar_conexiones(self, conexion):
		if conexion in self.Zocaloconexiones: self.Zocaloconexiones.remove(conexion)
		else:
			if DEBUG_REMOVE_WARNINGS:
				print("!A:", "Zocalo::QuitarConexion", "Se desea remover la conexion", conexion,
					  "de self.conexiones, pero no está en la lista")
				
	def quitar_todas_las_conexiones(self, silencioso=False):
		while self.Zocaloconexiones:
			conexion = self.Zocaloconexiones.pop(0)
			if silencioso:
				conexion.quitar(zocalo_silenciado=self)
			else:
				conexion.quitar()
				
	def determinarmulticonexion(self, data):
		if 'Multiconexion' in data:
			return data['Multiconexion']
		else:
			# Probablemente una versión antigua del archivo, por lo tanto, hacer los zócalos derechos como multiconexión por defecto.
			return data['Posicion'] in (Derecha_abajo, Derecha_arriba)
	
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
		self.esmulticonexion = self.determinarmulticonexion(data)
		self.cambiarTipoZocalo(data['Tipo_de_zocalo'])
		hashmap[data['id']] = self
		return True