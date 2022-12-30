from lib.nodeeditor.GraficosdeConexion import GraficosdeConexion
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo

from lib.nodeeditor.Utilidades import dump_exception

DEBUG = False
DEBUG_SELECCION = False


class Historial:
	def __init__(self, escena):
		self.escena = escena
		
		self.historial_nuevo()
		self.limite_historial = 32
		
		self.deshacer_seleccion_ha_cambiado = False
		
		# listeners
		self._modificadores_del_historial_listeners = []
		self._almacenado_del_historial_listeners = []
		self._restaurado_del_historial_listeners = []
		
	def historial_nuevo(self):
		self.listado_historial = []
		self.pos_act_historial = -1
		
	def marca_inicial_del_historial(self):
		self.almacenar_historial("Marca inicial del historial")
		
	def agregar_modificadores_del_historial_listeners(self, callback):
		self._modificadores_del_historial_listeners.append(callback)
		
	def agregar_almacenado_del_historial_listeners(self, callback):
		self._almacenado_del_historial_listeners.append(callback)
		
	def agregar_restaurado_del_historial_listeners(self, callback):
		self._restaurado_del_historial_listeners.append(callback)
		
	def habilitar_deshacer(self):
		return self.pos_act_historial > 0
	
	def habilitar_rehacer(self):
		return self.pos_act_historial + 1 < len(self.listado_historial)
	
	def deshacer(self):
		if DEBUG: print("Undo")
		
		if self.habilitar_deshacer():
			self.pos_act_historial -= 1
			self.restaurar_historial()
			self.escena.elementos_modificados = True
		
	def rehacer(self):
		if DEBUG: print("Redo")
		
		if self.habilitar_rehacer():
			self.pos_act_historial += 1
			self.restaurar_historial()
			self.escena.elementos_modificados = True
		
	def restaurar_historial(self):
		if DEBUG: print("Restaurando historial",
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		self.restaurar_marca_del_historial(self.listado_historial[self.pos_act_historial])
		for callback in self._modificadores_del_historial_listeners: callback()
		for callback in self._restaurado_del_historial_listeners: callback()


	def almacenar_historial(self, desc, set_modified=False):
		if set_modified:
			self.escena.elementos_modificados = True
		
		if DEBUG: print("Almacenando historial", '"%s"' % desc,
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		
		# Si la posición actual del historial no es el último de la lista.
		if self.pos_act_historial + 1 < len(self.listado_historial):
			self.listado_historial = self.listado_historial[0:self.pos_act_historial + 1]
		
		# Historial superior del límite.
		if self.pos_act_historial + 1 >= self.limite_historial:
			self.listado_historial = self.listado_historial[1:]
			self.pos_act_historial -= 1
		
		hs = self.crear_marca_en_el_historial(desc)
		
		self.listado_historial.append(hs)
		self.pos_act_historial += 1
		if DEBUG: print(" == configurando posición a:", self.pos_act_historial)
		
		for callback in self._modificadores_del_historial_listeners: callback()
		for callback in self._almacenado_del_historial_listeners: callback()
		
	def capturar_seleccion_actual(self):
		sel_obj = {
			'nodos': [],
			'conexiones': [],
		}
		
		for objeto in self.escena.graficador_de_la_escena.selectedItems():
			if isinstance(objeto, GraficosdelNodo):
				sel_obj['nodos'].append(objeto.nodo.id)
			elif isinstance(objeto, GraficosdeConexion):
				sel_obj['conexiones'].append(objeto.linea.id)
		return sel_obj
	
	def crear_marca_en_el_historial(self, desc):
		marca_en_el_historial = {
			'desc': desc,
			'snapshot': self.escena.serialización(),
			'selection': self.capturar_seleccion_actual(),
		}
		return marca_en_el_historial
		
	def restaurar_marca_del_historial(self, marca_historial):
		if DEBUG: print("RHS:", marca_historial['desc'])
		
		try:
			self.deshacer_seleccion_ha_cambiado = False
			seleccion_anterior = self.capturar_seleccion_actual()
			if DEBUG_SELECCION: print("nodos seleccionados antes de restaurar:", seleccion_anterior['nodos'])
			
			self.escena.deserialización(marca_historial['snapshot'])
			
			# Restaurar selección.
			# Primero se limpia la seleccion.
			for conexion in self.escena.conexiones: conexion.graficador_de_conexiones.setSelected(False)
			# Luego, se restauran las selecciones desde el historial.
			for conexion_id in marca_historial['selection']['conexiones']:
				for conexion in self.escena.conexiones:
					if conexion.id == conexion_id:
						conexion.graficador_de_conexiones.setSelected(True)
						break
			
			for nodo in self.escena.nodos: nodo.Nodograficas.setSelected(False)
			for nodo_id in marca_historial['selection']['nodos']:
				for nodo in self.escena.nodos:
					if nodo.id == nodo_id:
						nodo.Nodograficas.setSelected(True)
						break
			
			seleccion_actual = self.capturar_seleccion_actual()
			if DEBUG_SELECCION: print("nodos seleccionados después de restaurar:", seleccion_actual['nodos'])
			
			self.escena._ultimos_objetos_seleccionados = self.escena.objetos_seleccionados()
			
			# Si la selección es diferente antes y después, activar flag.
			if seleccion_actual['nodos'] != seleccion_anterior['nodos'] or seleccion_actual['conexiones'] != seleccion_anterior['conexiones']:
				if DEBUG_SELECCION: print("\nESCENA: La selección ha cambiado")
				self.deshacer_seleccion_ha_cambiado = True
						
		except Exception as e: dump_exception(e)
		