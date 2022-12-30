import os
import json
from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficadordelaEscena import GraficadordelaEscena
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Conexiones import Conexion
from lib.nodeeditor.Historial_escena import Historial
from lib.nodeeditor.Portapapeles import Portapapeles
from lib.nodeeditor.Utilidades import dump_exception, pp

DEBUG_REMOVE_WARNINGS = False

class InvalidFile(Exception): pass


class Escena(Serializable):
	def __init__(self):
		super().__init__()
		self.nodos = []
		self.conexiones = []
		
		self.nombre_de_archivo = None
		
		self.anchura_de_la_escena = 64000
		self.altura_de_la_escena = 64000
		
		self._eventos_de_selección_silenciosa = False
		
		self._elementos_modificados = False
		self._ultimos_objetos_seleccionados = None
		
		# Inicializado de los listeners.
		self._elementos_modificados_listeners = []
		self._objeto_seleccionado_listeners = []
		self._objetos_no_seleccionados_listeners = []
		
		# Aquí podremos almacenar llamadas para obtener la clase de los nodos.
		self.selector_de_clases_de_nodos = None
		
		self.init_ui()
		self.historial = Historial(self)
		self.portapapeles = Portapapeles(self)
		
		self.graficador_de_la_escena.objeto_seleccionado.connect(self.objeto_seleccionado)
		self.graficador_de_la_escena.objetos_no_seleccionados.connect(self.objetos_no_seleccionados)
	
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
		
	def init_ui(self):
		self.graficador_de_la_escena = GraficadordelaEscena(self)
		self.graficador_de_la_escena.config_esc(self.anchura_de_la_escena, self.altura_de_la_escena)
		
	def obtener_nodo_por_el_id(self, id_nodo):
		for nodo in self.nodos:
			if nodo.id == id_nodo:
				return nodo
		return None
		
	def configurar_eventos_de_selección_silenciosa(self, valor=True):
		self._eventos_de_selección_silenciosa = valor
		
	def objeto_seleccionado(self, silencioso=False):
		if self._eventos_de_selección_silenciosa: return
		
		objetos_seleccionados_actualmente = self.objetos_seleccionados()
		if objetos_seleccionados_actualmente != self._ultimos_objetos_seleccionados:
			self._ultimos_objetos_seleccionados = objetos_seleccionados_actualmente
			if not silencioso:
				for callback in self._objeto_seleccionado_listeners: callback()
				self.historial.almacenar_historial("La selección ha cambiado.")
		
	def objetos_no_seleccionados(self, silencioso=False):
		seleccion_actual = self.objetos_seleccionados()
		if seleccion_actual == self._ultimos_objetos_seleccionados:
			return
		self.restaurar_último_estado_de_selección()
		if seleccion_actual == []:
			self._ultimos_objetos_seleccionados = []
			if not silencioso:
				self.historial.almacenar_historial("Todos los objetos se han deseleccionado.")
				for callback in self._objetos_no_seleccionados_listeners: callback()
		
	def hay_cambios(self):
		return self.elementos_modificados
	
	def objetos_seleccionados(self):
		return self.graficador_de_la_escena.selectedItems()
	
	def hacer_deseleccionar_objetos(self, silencioso=False):
		for objeto in self.objetos_seleccionados():
			objeto.setSelected(False)
		if not silencioso:
			self.objetos_no_seleccionados()
		
	# Funciones de ayuda para los listeners.
	def agregar_elementos_modificados_listener(self, callback):
		self._elementos_modificados_listeners.append(callback)
		
	def agregar_objeto_seleccionado_listener(self, callback):
		self._objeto_seleccionado_listeners.append(callback)
	
	def agregar_objetos_no_seleccionados_listener(self, callback):
		self._objetos_no_seleccionados_listeners.append(callback)
		
	def agregar_dragenter_listener(self, callback):
		self.obtener_vista().agregar_dragenter_listener(callback)
		
	def agregar_drop_listener(self, callback):
		self.obtener_vista().agregar_drop_listener(callback)
	
	# Señales para detectar si algún nodo o conexión a sido seleccionado.
	def restaurar_último_estado_de_selección(self):
		for nodo in self.nodos:
			nodo.Nodograficas._ultimo_estado_de_seleccion = False
		for conexion in self.conexiones:
			conexion.graficador_de_conexiones._ultimo_estado_de_seleccion = False
	
	def obtener_vista(self):
		return self.graficador_de_la_escena.views()[0]
	
	def obtener_objeto_en_la_posición(self, pos):
		return self.obtener_vista().itemAt(pos)
	
	def agregar_nodo(self, nodo):
		self.nodos.append(nodo)
	
	def agregar_conexión(self, conexion):
		self.conexiones.append(conexion)
	
	def eliminar_nodo(self, nodo):
		if nodo in self.nodos: self.nodos.remove(nodo)
		else:
			if DEBUG_REMOVE_WARNINGS: print("!A:", "Escena::eliminar_nodo", "Se desea remover el nodo", nodo,
											"de self.nodos, pero no está en la lista")
	
	def eliminar_conexión(self, conexion):
		if conexion in self.conexiones: self.conexiones.remove(conexion)
		else:
			if DEBUG_REMOVE_WARNINGS: print("!A:", "Escena::eliminar_conexión:", "Se desea remover la conexion",
											conexion, "de self.conexiones, pero no está en la lista.")
		
	def limpiar_escena(self):
		while len(self.nodos) > 0:
			self.nodos[0].quitar()
			
		self.elementos_modificados = False
	
	def guardar_archivo(self, archivo):
		with open(archivo, "w") as file:
			file.write(json.dumps(self.serialización(), indent=4))
			print("Guardado exitosamente en", archivo)
			
			self.elementos_modificados = False
			self.nombre_de_archivo = archivo
			
	def abrir_archivo(self, archivo):
		with open(archivo, "r") as file:
			raw_data = file.read()
			try:
				data = json.loads(raw_data)
				# En el tutorial añade un «enconding='utf-8'», pero al añadirla yo,
				# el parametro encoding no aparece, y ejecutar este codigo al presionar las respectivas
				# teclas da error. Decidí eliminarlo y dejar esta nota por si surge algún error luego por esto.
				self.nombre_de_archivo = archivo
				self.deserialización(data)
				self.elementos_modificados = False
			except json.JSONDecodeError:
				raise InvalidFile("%s no es un archivo JSON válido." % os.path.basename(archivo))
			except Exception as e:
				dump_exception(e)
				
	def obtener_clase_de_conexión(self):
		return Conexion

	def definir_selector_de_clases_de_nodos(self, funcion_selectora_de_clases):
		# Cuando está configurada la función self.selector_de_clases_de_nodos, podremos usar diferentes clases de nodos.
		self.selector_de_clases_de_nodos = funcion_selectora_de_clases
		
	def obtener_clase_del_nodo_de_datos(self, data):
		return Nodo if self.selector_de_clases_de_nodos is None else self.selector_de_clases_de_nodos(data)
	
	def serialización(self):
		nodos, conexiones = [], []
		for nodo in self.nodos: nodos.append(nodo.serialización())
		for conexión in self.conexiones: conexiones.append(conexión.serialización())
		return OrderedDict([
			('ID', self.id),
			('Anchura de la escena', self.anchura_de_la_escena),
			('Altura de la escena', self.altura_de_la_escena),
			('Nodos', nodos),
			('Conexiones', conexiones),
		])
	
	def deserialización(self, data, hashmap={}, restaure_id=True, *args, **kwargs):
		hashmap = {}
		
		if restaure_id: self.id = data['ID']
		
		# nodos
		todos_los_nodos = self.nodos.copy()
		
		for datos_nodo in data['Nodos']:
			encontrado = False
			for nodo in todos_los_nodos:
				if nodo.id == datos_nodo['ID']:
					encontrado = nodo
					break
			
			if not encontrado:
				try:
					nuevo_nodo = self.obtener_clase_del_nodo_de_datos(datos_nodo)(self)
					nuevo_nodo.deserialización(datos_nodo, hashmap, restaure_id, *args, **kwargs)
					nuevo_nodo.al_deserializar(datos_nodo)
				except:
					dump_exception()
			else:
				try:
					encontrado.deserializacion(datos_nodo, hashmap, restaure_id, *args, **kwargs)
					encontrado.al_deserializar(datos_nodo)
					todos_los_nodos.remove(encontrado)
				except: dump_exception()
					
		while todos_los_nodos != []:
			nodo = todos_los_nodos.pop()
			nodo.quitar()
			
		# conexiones.
		todas_las_conexiones = self.conexiones.copy()
		
		for datos_conexion in data['Conexiones']:
			encontrado = False
			for conexion in todas_las_conexiones:
				if conexion.id == datos_conexion['ID']:
					encontrado = conexion
					break
			
			if not encontrado:
				nueva_conexion = Conexion(self).deserialización(datos_conexion, hashmap, restaure_id, *args, **kwargs)
			else:
				encontrado.deserializacion(datos_conexion, hashmap, restaure_id, *args, **kwargs)
				todas_las_conexiones.remove(encontrado)
				
		while todas_las_conexiones != []:
			conexion = todas_las_conexiones.pop()
			conexion.quitar()
		
		return True