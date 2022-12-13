from collections import OrderedDict
from nodeeditor.GraficosdeConexion import GraficosdeConexion
from nodeeditor.Nodo import Nodo
from nodeeditor.Conexiones import Conexion


DEBUG = True


class PortapapelesEscena:
	def __init__(self, escena):
		self.escena = escena
		
	def serializacionSeleccionado(self, delete=False):
		if DEBUG: print("-- COPY TO CLIPBOARD ---")
		
		sel_nodos, sel_lineas, sel_zocalos = [], [], {}
		
		# Ordenar líneas y zócalos.
		for item in self.escena.GraficosEsc.selectedItems():
			if hasattr(item, 'nodo'):
				sel_nodos.append(item.nodo.serializacion())
				for zocalos in (item.nodo.entradas + item.nodo.salidas):
					sel_zocalos[zocalos.id] = zocalos
			elif isinstance(item, GraficosdeConexion):
				sel_lineas.append(item.linea)
				
		
		# Debug
		if DEBUG:
			print("    NODOS\n     ", sel_nodos)
			print("    LINEAS\n     ", sel_lineas)
			print("    ZOCALOS\n      ", sel_zocalos)
			
		# Quitar todos las lineas no conectadas a otro nodo en la lista.
		lineas_a_quitar = []
		for linea in sel_lineas:
			if linea.zocalo_origen.id in sel_zocalos and linea.zocalo_final.id in sel_zocalos:
			#	if DEBUG: print("La línea está bien, está conectada en ambos extremos.")
				pass
			else:
				if DEBUG: print("La línea", linea, "no está conectado en ambos extremos.")
				lineas_a_quitar.append(linea)
		for linea in lineas_a_quitar:
			sel_lineas.remove(linea)
			
		# Creación de la lista final de líneas.
		lineas_finales = []
		for linea in sel_lineas:
			lineas_finales.append(linea.serializacion())
		
		data = OrderedDict([
			('Nodos', sel_nodos),
			('Conexiones', lineas_finales),
		])
		
		# Si corta (mejor conocido como Delete), quitar el objeto.
		if delete:
			self.escena.obtenerVista().eliminarSeleccionado()
			# Guardado en el historial.
			self.escena.historial.almacenarHistorial("Elementos cortados de la escena", setModified=True)
		
		return data
	
	def deserializacionDesdePortapapeles(self, data):
	
		hashmap = {}
		
		# Calcular la posición en la escena del puntero del mouse.
		vista = self.escena.obtenerVista()
		mouse_scene_pos = vista.ultima_posicion_mouse_escena
		
		# Calcular el contorno delimitador de los objetos seleccionados y su centro.
		minx, maxx, miny, maxy = 0, 0, 0, 0
		for data_nodos in data['Nodos']:
			x, y = data_nodos['Pos_x'], data_nodos['Pos_y']
			if x < minx: minx = x
			if x > maxx: maxx = x
			if y < miny: miny = y
			if y > maxy: maxy = y
		centro_x_contenedor = (minx + maxx) / 2
		centro_y_contenedor = (miny + maxy) / 2
		
		# (Gracias a Dios :v) centro = view.mapToScene(view.rect().center())
		
		# Calcular el offset tehe de los nuevos nodos que se crearán.
		offset_x = mouse_scene_pos.x() - centro_x_contenedor
		offset_y = mouse_scene_pos.y() - centro_y_contenedor
		
		# Creación de cada nodo.
		for data_nodos in data['Nodos']:
			nuevo_nodo = self.escena.obtener_clase_del_nodo_de_datos(data_nodos)(self.escena)
			nuevo_nodo.deserializacion(data_nodos, hashmap, restaure_id=False)
			
			# Reajuste de posición para el nuevo nodo.
			pos = nuevo_nodo.pos
			nuevo_nodo.definirposicion(pos.x() + offset_x, pos.y() + offset_y)
		
		# Creación de cada conexion.
		if 'Conexiones' in data:
			for data_conexion in data['Conexiones']:
				nueva_conexion = Conexion(self.escena)
				nueva_conexion.deserializacion(data_conexion, hashmap, restaure_id=False)
		
		# Guardar historial.
		self.escena.historial.almacenarHistorial("Elementos pegados del portapapeles.", setModified=True)
		
