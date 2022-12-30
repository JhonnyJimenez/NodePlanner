from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficosdeZocalos import GraficosdeZocalos
from lib.nodeeditor.Utilidades import debugnames


IZQUIERDA_ARRIBA = 1
IZQUIERDA_CENTRO = 2
IZQUIERDA_ABAJO = 3
DERECHA_ARRIBA = 4
DERECHA_CENTRO = 5
DERECHA_ABAJO = 6

DEBUG = False
DEBUG_REMOVE_WARNINGS = False


class Zocalo(Serializable):
	ClaseGraficadeZocalos = GraficosdeZocalos
	
	def __init__(
			self, nodo, indice, posicion, tipo_zocalo=1, multiconexion=True, cantidad_en_el_lado_actual=1,
			es_entrada=False
			):
		super().__init__()
		
		self.nodo = nodo
		self.posicion = posicion
		self.indice = indice
		self.tipo_zocalo = tipo_zocalo
		self.cantidad_en_el_lado_actual = cantidad_en_el_lado_actual
		self.es_multiconexion = multiconexion
		self.es_entrada = es_entrada
		self.es_salida = not self.es_entrada
		
		if DEBUG:
			print("Zócalo", self.indice, "ubicado", debugnames(posicion), "del", self.nodo.titulo, self.nodo)
			
		self.GraficosZocalos = self.__class__.ClaseGraficadeZocalos(self)
		
		self.definir_posicion_del_zocalo()
		
		self.Zocaloconexiones = []
	
	def __str__(self):
		return "<Zócalo #%d %s %s..%s>" % (
			self.indice, "multiconexion" if self.es_multiconexion else "de conexion única",
			hex(id(self))[2:5], hex(id(self))[-3:]
		)
	
	def eliminar_zocalo(self):
		self.GraficosZocalos.setParentItem(None)
		self.nodo.escena.graficador_de_la_escena.removeItem(self.GraficosZocalos)
		del self.GraficosZocalos
		
	def cambiar_tipo_de_zocalo(self, nuevo_tipo_zocalo):
		if self.tipo_zocalo != nuevo_tipo_zocalo:
			self.tipo_zocalo = nuevo_tipo_zocalo
			self.GraficosZocalos.cambiar_tipo_de_zocalo()
			return True
		return False
	
	def definir_posicion_del_zocalo(self):
		self.GraficosZocalos.setPos(*self.nodo.obtener_posicion_zocalo(self.indice, self.posicion, self.cantidad_en_el_lado_actual))
	
	def posicion_zocalo(self):
		if DEBUG: print("   GSP:", self.indice, self.posicion, "Editor de nodos:", self.nodo)
		res = self.nodo.obtener_posicion_zocalo(self.indice, self.posicion, self.cantidad_en_el_lado_actual)
		if DEBUG: print("   res:", res)
		return res
	
	def tiene_alguna_conexion(self):
		return len(self.Zocaloconexiones) > 0
	
	def está_conectado(self, conexion):
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
				
	def determinar_multiconexión(self, data):
		if 'Multiconexión' in data:
			return data['Multiconexión']
		else:
			# Probablemente una versión antigua del archivo, por lo tanto, hacer los zócalos derechos como multiconexión por defecto.
			return data['Posición'] in (DERECHA_ABAJO, DERECHA_ARRIBA)
	
	def serialización(self):
		return OrderedDict([
			('ID', self.id),
			('Índice', self.indice),
			('Multiconexión', self.es_multiconexion),
			('Posición', self.posicion),
			('Tipo de zócalo', self.tipo_zocalo),
		])
	
	def deserialización(self, data, hashmap={}, restaure_id=True):
		if restaure_id: self.id = data['ID']
		self.es_multiconexion = self.determinar_multiconexión(data)
		self.cambiar_tipo_de_zocalo(data['Tipo de zócalo'])
		hashmap[data['ID']] = self
		return True