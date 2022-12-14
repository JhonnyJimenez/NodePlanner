import os
import json
from collections import OrderedDict
from nodeeditor.Seriabilizador import Serializable
from nodeeditor.GraficosEscena import GraficosEscena
from nodeeditor.Nodo import Nodo
from nodeeditor.Conexiones import Conexion
from nodeeditor.Historial_escena import HistorialEscena
from nodeeditor.Portapapeles import PortapapelesEscena
from nodeeditor.Utilidades import dump_exception

DEBUG_REMOVE_WARNINGS = False

class InvalidFile(Exception): pass


class Escena(Serializable):
	def __init__(self):
		super().__init__()
		self.Nodos = []
		self.Conexiones = []
		
		self.Escena_Ancho = 64000
		self.Escena_Alto = 64000
		
		self._eventos_de_seleccion_silenciosa = False
		self._elementos_modificados = False
		self._ultimos_objetos_seleccionados = []
		
		# Inicializado de los listeners.
		self._elementos_modificados_listeners = []
		self._objeto_seleccionado_listeners = []
		self._objetos_no_seleccionados_listeners = []
		
		# Aquí podremos almacenar llamadas para obtener la clase de los nodos.
		self.selector_de_clases_de_nodos = None
		
		self.initUI()
		self.historial = HistorialEscena(self)
		self.portapapeles = PortapapelesEscena(self)
		
		self.GraficosEsc.objetoSeleccionado.connect(self.objetoSeleccionado)
		self.GraficosEsc.objetosNoSeleccionados.connect(self.objetosNoSeleccionados)
	
	@property
	def elementos_modificados(self):
		return self._elementos_modificados
	
	@elementos_modificados.setter
	def elementos_modificados(self, value):
		if not self._elementos_modificados and value:
			# Configurándolo ahora, porque se leerá el dato pronto.
			self._elementos_modificados = value
			
			# Llama todos los listeners registrados.
			for callback in self._elementos_modificados_listeners: callback()
		
		self._elementos_modificados = value
		
	def initUI(self):
		self.GraficosEsc = GraficosEscena(self)
		self.GraficosEsc.config_esc(self.Escena_Ancho, self.Escena_Alto)
		
	def configEventosdeSeleccionSilenciosa(self, valor=True):
		self._eventos_de_seleccion_silenciosa = valor
		
	def objetoSeleccionado(self, silencioso=False):
		if self._eventos_de_seleccion_silenciosa: return
		
		objetos_seleccionados_actualmente = self.objetosSeleccionados()
		if objetos_seleccionados_actualmente != self._ultimos_objetos_seleccionados:
			self._ultimos_objetos_seleccionados = objetos_seleccionados_actualmente
			if not silencioso:
				self.historial.almacenarHistorial("La selección ha cambiado.")
				for callback in self._objeto_seleccionado_listeners: callback()
		
	def objetosNoSeleccionados(self, silencioso=False):
		self.restaurarUltimoEstadodeSeleccion()
		if self._ultimos_objetos_seleccionados != []:
			self._ultimos_objetos_seleccionados = []
			if not silencioso:
				self.historial.almacenarHistorial("Todos los objetos se han deseleccionado.")
				for callback in self._objetos_no_seleccionados_listeners: callback()
		
	def haycambios(self):
		return self.elementos_modificados
	
	def objetosSeleccionados(self):
		return self.GraficosEsc.selectedItems()
	
	def hacerDeseleccionarObjetos(self, silencioso=False):
		for objeto in self.objetosSeleccionados():
			objeto.setSelected(False)
		if not silencioso:
			self.objetosNoSeleccionados()
		
	# Funciones de ayuda para los listeners.
	def agregarElementosModificadosListener(self, callback):
		self._elementos_modificados_listeners.append(callback)
		
	def agregarObjetoSeleccionadoListener(self, callback):
		self._objeto_seleccionado_listeners.append(callback)
	
	def agregarObjetosNoSeleccionadosListener(self, callback):
		self._objetos_no_seleccionados_listeners.append(callback)
		
	def agregarDragEnterListener(self, callback):
		self.obtenerVista().agregarDragEnterListener(callback)
		
	def agregarDropListener(self, callback):
		self.obtenerVista().agregarDropListener(callback)
	
	# Señales para detectar si algún nodo o conexión a sido seleccionado.
	def restaurarUltimoEstadodeSeleccion(self):
		for nodo in self.Nodos:
			nodo.Nodograficas._ultimo_estado_de_seleccion = False
		for conexion in self.Conexiones:
			conexion.GraficosDeConexion._ultimo_estado_de_seleccion = False
	
	def obtenerVista(self):
		return self.GraficosEsc.views()[0]
	
	def obtenerObjetoAl(self, pos):
		return self.obtenerVista().itemAt(pos)
	
	def agregarnodo(self, nodo):
		self.Nodos.append(nodo)
	
	def agregarconexion(self, conexion):
		self.Conexiones.append(conexion)
	
	def eliminarnodo(self, nodo):
		if nodo in self.Nodos: self.Nodos.remove(nodo)
		else:
			if DEBUG_REMOVE_WARNINGS: print("!A:", "Escena::eliminarnodo", "Se desea remover el nodo", nodo,
											"de self.Nodos, pero no está en la lista")
	
	def eliminarconexion(self, conexion):
		if conexion in self.Conexiones: self.Conexiones.remove(conexion)
		else:
			if DEBUG_REMOVE_WARNINGS: print("!A:", "Escena::eliminarconexion:", "Se desea remover la conexion",
											conexion, "de self.Conexiones, pero no está en la lista.")
		
	def limpiarEscena(self):
		while len(self.Nodos) > 0:
			self.Nodos[0].quitar()
			
		self.elementos_modificados = False
	
	def guardarArchivo(self, archivo):
		with open(archivo, "w") as file:
			file.write(json.dumps(self.serializacion(), indent=4))
			print("Guardado exitosamente en", archivo)
			
			self.elementos_modificados = False
			
	def abrirArchivo(self, archivo):
		with open(archivo, "r") as file:
			raw_data = file.read()
			try:
				data = json.loads(raw_data)
				# En el tutorial añade un «enconding='utf-8'», pero al añadirla yo,
				# el parametro encoding no aparece, y ejecutar este codigo al presionar las respectivas
				# teclas da error. Decidí eliminarlo y dejar esta nota por si surge algún error luego por esto.
				self.deserializacion(data)
				self.elementos_modificados = False
			except json.JSONDecodeError:
				raise InvalidFile("%s no es un archivo JSON válido." % os.path.basename(archivo))
			except Exception as e:
				dump_exception(e)

	def definirSelectordeClasesdeNodos(self, funcion_selectora_de_clases):
		# Cuando está configurada la función self.selector_de_clases_de_nodos, podremos usar diferentes clases de nodos.
		self.selector_de_clases_de_nodos = funcion_selectora_de_clases
		
	def obtener_clase_del_nodo_de_datos(self, data):
		return Nodo if self.selector_de_clases_de_nodos is None else self.selector_de_clases_de_nodos(data)
	
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
			self.obtener_clase_del_nodo_de_datos(nodo_data)(self).deserializacion(nodo_data, hashmap, restaure_id)
		
		# Creación de conexiones.
		for datos_conexion in data['Conexiones']:
			Conexion(self).deserializacion(datos_conexion, hashmap, restaure_id)
		
		return True