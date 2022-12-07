import json
from collections import OrderedDict
from nodeeditor.Seriabilizador import Serializable
from nodeeditor.GraficosdelaEscena_vp import GraficosdelaEscenaVP
from nodeeditor.Nodo import Nodo
from nodeeditor.Conexiones import Conexion
from nodeeditor.Historial_escena import HistorialEscena
from nodeeditor.Portapapeles import PortapapelesEscena


class Escena(Serializable):
	def __init__(self):
		super().__init__()
		self.Nodos = []
		self.Conexiones = []
		
		self.Escena_Ancho = 64000
		self.Escena_Alto = 64000
		
		self._elementos_modificados = False
		self._elementos_modificados_listeners = []
		
		self.GraficosEsc = GraficosdelaEscenaVP(self)
		self.GraficosEsc.config_esc(self.Escena_Ancho, self.Escena_Alto)
		
		self.historial = HistorialEscena(self)
		self.portapapeles = PortapapelesEscena(self)
		
	@property
	def elementos_modificados(self):
		return self._elementos_modificados
	
	@elementos_modificados.setter
	def elementos_modificados(self, value):
		if not self._elementos_modificados and value:
			self._elementos_modificados = value
			
			# llamar a todos los listeners
			for callback in self._elementos_modificados_listeners:
				callback()
		
		self._elementos_modificados = value
		
	def addelementosmodificadoslistener(self, callback):
		self._elementos_modificados_listeners.append(callback)
	
	def agregarnodo(self, nodo):
		self.Nodos.append(nodo)
	
	def agregarconexion(self, conexion):
		self.Conexiones.append(conexion)
	
	def eliminarnodo(self, nodo):
		self.Nodos.remove(nodo)
		# if nodo in self.Nodos: self.Nodos.remove(nodo)
		# else: print("!A:", "Escena::eliminarnodo", "Se desea remover el nodo", nodo, "de self.Nodos, pero no está en la lista")
	
	def eliminarconexion(self, conexion):
		self.Conexiones.remove(conexion)
		# if conexion in self.Conexiones: self.Conexiones.remove(conexion)
		# else: print("!A:", "Escena::eliminarconexion:", "Se desea remover la conexion", conexion, "de self.Conexiones, pero no está en la lista.")
		
	def limpiarEscena(self):
		while len(self.Nodos) > 0:
			self.Nodos[0].quitar()
			
		self.elementos_modificados = False
	
	def guardarArchivo(self, archivo):
		with open(archivo, "w") as file:
			file.write( json.dumps( self.serializacion(), indent=4 ) )
			print("Guardado exitosamente en", archivo)
			
			self.elementos_modificados = False
			
	def abrirArchivo(self, archivo):
		with open(archivo, "r") as file:
			raw_data = file.read()
			data = json.loads(raw_data)
			# En el tutorial en la linea 45 añade un «enconding='utf-8'», pero al añadirla yo,
			# el parametro encoding no aparece, y ejecutar este codigo al presionar las respectivas
			# teclas da error. Decidí eliminarlo y dejar esta nota por si surge algún error luego por esto.
			self.deserializacion(data)
			
			self.elementos_modificados = False
	
	
	def serializacion(self):
		nodos, conexiones = [], []
		for Nodo in self.Nodos: nodos.append(Nodo.serializacion())
		for Conexion in self.Conexiones: conexiones.append(Conexion.serializacion())
		return OrderedDict([
			('id', self.id),
			('Escena_Ancho', self.Escena_Ancho),
			('Escena_Alto', self.Escena_Alto),
			('Nodos', nodos),
			('Conexiones', conexiones),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		self.limpiarEscena()
		hashmap = {}
		
		if restaure_id: self.id = data['id']
		
		# Creación de nodos.
		for nodo_data in data['Nodos']:
			Nodo(self).deserializacion(nodo_data, hashmap, restaure_id)
		
		# Creación de conexiones.
		for datos_conexion in data['Conexiones']:
			Conexion(self).deserializacion(datos_conexion, hashmap, restaure_id)
		
		return True