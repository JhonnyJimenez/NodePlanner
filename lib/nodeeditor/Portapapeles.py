from collections import OrderedDict
from lib.nodeeditor.GraficosdeConexion import GraficosdeConexion
from lib.nodeeditor.Conexiones import Conexion


DEBUG = False
DEBUG_PASTING = False


class PortapapelesEscena:
	def __init__(self, escena):
		self.escena = escena
		
	def serializacionSeleccionado(self, delete=False):
		if DEBUG: print("-- COPY TO CLIPBOARD ---")
		
		sel_nodos, sel_lineas, sel_zocalos = [], [], {}
		
		# Ordenar líneas y zócalos.
		for objeto in self.escena.GraficosEsc.selectedItems():
			if hasattr(objeto, 'nodo'):
				sel_nodos.append(objeto.nodo.serializacion())
				for zocalos in (objeto.nodo.entradas + objeto.nodo.salidas):
					sel_zocalos[zocalos.id] = zocalos
			elif isinstance(objeto, GraficosdeConexion):
				sel_lineas.append(objeto.linea)
				
		
		# Debug
		if DEBUG:
			print("    NODOS\n     ", sel_nodos)
			print("    LINEAS\n     ", sel_lineas)
			print("    ZOCALOS\n      ", sel_zocalos)
			
		# Quitar todos las lineas no conectadas a un editor de nodos en la lista.
		lineas_a_quitar = []
		for linea in sel_lineas:
			if linea.zocalo_origen.id in sel_zocalos and linea.zocalo_final.id in sel_zocalos:
				# if DEBUG: print("La línea está bien, está conectada en ambos extremos.")
				pass
			else:
				# if DEBUG: print("La línea", linea, "no está conectado en ambos extremos.")
				lineas_a_quitar.append(linea)
		for linea in lineas_a_quitar:
			sel_lineas.remove(linea)
			
		# Creación de la lista final de líneas.
		lineas_finales = []
		for linea in sel_lineas:
			lineas_finales.append(linea.serializacion())
			
		if DEBUG: print("La lista final de conexiones es:", lineas_finales)
		
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
	
	def deserializacionDesdePortapapeles(self, data, *args, **kwargs):
	
		hashmap = {}
		
		# Calcular la posición en la escena del puntero del mouse.
		vista = self.escena.obtenerVista()
		mouse_scene_pos = vista.ultima_posicion_mouse_escena
		
		# Calcular el contorno delimitador de los objetos seleccionados y su centro.
		minx, maxx, miny, maxy = 10000000, -10000000, 10000000, -10000000
		for data_nodos in data['Nodos']:
			x, y = data_nodos['Pos_x'], data_nodos['Pos_y']
			if x < minx: minx = x
			if x > maxx: maxx = x
			if y < miny: miny = y
			if y > maxy: maxy = y
			
		# Agregar anchura y altura de un nodo.
		maxx -= 180
		maxy +- 100
		
		centro_x = (minx + maxx) / 2 - minx
		centro_y = (miny + maxy) / 2 - miny
		
		if DEBUG_PASTING:
			print(" *** PASTA:")
			print("Copied boudaries:\n\tX:", minx, maxx, "   Y:", miny, maxy)
			print("\tbbox_center:", centro_x, centro_y)
		
		# Calcular el offset tehe de los nuevos nodos que se crearán.
		mouse_x, mouse_y = mouse_scene_pos.x(), mouse_scene_pos.y()
		
		# Creación de cada nodo.
		nodos_creados = []
		
		self.escena.configEventosdeSeleccionSilenciosa()
		
		self.escena.hacerDeseleccionarObjetos()
		
		for data_nodos in data['Nodos']:
			nuevo_nodo = self.escena.obtener_clase_del_nodo_de_datos(data_nodos)(self.escena)
			nuevo_nodo.deserializacion(data_nodos, hashmap, restaure_id=False, *args, **kwargs)
			nodos_creados.append(nuevo_nodo)
			
			# Reajuste de posición para el nuevo nodo.
			
			# posición actual del nuevo nodo
			pos_x, pos_y = nuevo_nodo.pos.x(), nuevo_nodo.pos.y()
			nuevapos_x, nuevapos_y = mouse_x + pos_x - minx, mouse_y + pos_y - miny
			
			nuevo_nodo.definirposicion(nuevapos_x, nuevapos_y)
			
			nuevo_nodo.hacerSeleccion()
			
			if DEBUG_PASTING:
				print("** PASTA SUM:")
				print("\tMouse pos:", mouse_x, mouse_y)
				print("\tnew node pos:", pos_x, pos_y)
				print("\tFINAL:", nuevapos_x, nuevapos_y)
		
		# Creación de cada conexion.
		if 'Conexiones' in data:
			for data_conexion in data['Conexiones']:
				nueva_conexion = Conexion(self.escena)
				nueva_conexion.deserializacion(data_conexion, hashmap, restaure_id=False, *args, **kwargs)
				
		self.escena.configEventosdeSeleccionSilenciosa(False)
		
		# Guardar historial.
		self.escena.historial.almacenarHistorial("Elementos pegados del portapapeles.", setModified=True)
		
		return nodos_creados
