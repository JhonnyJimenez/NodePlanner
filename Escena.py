import json
from collections import OrderedDict
from Seriabilizador import Serializable
from GraficosdelaEscena_vp import GraficosdelaEscenaVP
from Nodo import Nodo
from Conexiones import Conexion


class Escena(Serializable):
	def __init__(self):
		super().__init__()
		self.Nodos = []
		self.Conexiones = []
		
		self.Escena_Ancho = 64000
		self.Escena_Alto = 64000
		
		self.GraficosEsc = GraficosdelaEscenaVP(self)
		self.GraficosEsc.config_esc(self.Escena_Ancho, self.Escena_Alto)
	
	def agregarnodo(self, nodo):
		self.Nodos.append(nodo)
	
	def agregarconexion(self, conexion):
		self.Conexiones.append(conexion)
	
	def eliminarnodo(self, nodo):
		self.Nodos.remove(nodo)
	
	def eliminarconexion(self, conexion):
		self.Conexiones.remove(conexion)
		
	def limpiarEscena(self):
		while len(self.Nodos) > 0:
			self.Nodos[0].quitar()
	
	def guardarArchivo(self, archivo):
		with open(archivo, "w") as file:
			file.write( json.dumps( self.serializacion(), indent=4 ) )
		print("Guardado exitosamente en", archivo)
			
	def abrirArchivo(self, archivo):
		with open(archivo, "r") as file:
			raw_data = file.read()
			data = json.loads(raw_data)
			# En el tutorial en la linea 45 añade un «enconding='utf-8'», pero al añadirla yo,
			# el parametro encoding no aparece, y ejecutar este codigo al presionar las respectivas
			# teclas da error. Decidí eliminarlo y dejar esta nota por si surge algún error luego por esto.
			self.deserializacion(data)
	
	
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
	
	def deserializacion(self, data, hashmap={}):
		print("Deserializando datos de", data)
		
		self.limpiarEscena()
		hashmap = {}
		
		# Creación de nodos.
		for nodo_data in data['Nodos']:
			Nodo(self).deserializacion(nodo_data, hashmap)
		
		# Creación de conexiones.
		for datos_conexion in data['Conexiones']:
			Conexion(self).deserializacion(datos_conexion, hashmap)
		
		return True