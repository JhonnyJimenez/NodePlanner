from nodeeditor.GraficosdeConexion import GraficosdeConexion
from nodeeditor.GraficosdelNodo import GraficosdelNodo

from nodeeditor.Utilidades import dump_exception

DEBUG = False
DEBUG_SELECCION = False


class HistorialEscena:
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
		
	def marcaInicialdelHistorial(self):
		self.almacenarHistorial("Marca inicial del historial")
		
	def agregarmodificadoresdelhistorialisteners(self, callback):
		self._modificadores_del_historial_listeners.append(callback)
		
	def agregaralmacenadodelhistorialisteners(self, callback):
		self._almacenado_del_historial_listeners.append(callback)
		
	def agregarrestauradodelhistorialisteners(self, callback):
		self._restaurado_del_historial_listeners.append(callback)
		
	def habilitarDeshacer(self):
		return self.pos_act_historial > 0
	
	def habilitarRehacer(self):
		return self.pos_act_historial + 1 < len(self.listado_historial)
	
	def deshacer(self):
		if DEBUG: print("Undo")
		
		if self.habilitarDeshacer():
			self.pos_act_historial -= 1
			self.restaurarHistorial()
			self.escena.elementos_modificados = True
		
	def rehacer(self):
		if DEBUG: print("Redo")
		
		if self.habilitarRehacer():
			self.pos_act_historial += 1
			self.restaurarHistorial()
			self.escena.elementos_modificados = True
		
	def restaurarHistorial(self):
		if DEBUG: print("Restaurando historial",
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		self.RestaurarMarcaHistorial(self.listado_historial[self.pos_act_historial])
		for callback in self._modificadores_del_historial_listeners: callback()
		for callback in self._restaurado_del_historial_listeners: callback()


	def almacenarHistorial(self, desc, setModified=False):
		if setModified:
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
		
		hs = self.crear_Marca_Historial(desc)
		
		self.listado_historial.append(hs)
		self.pos_act_historial += 1
		if DEBUG: print(" == configurando posición a:", self.pos_act_historial)
		
		for callback in self._modificadores_del_historial_listeners: callback()
		for callback in self._almacenado_del_historial_listeners: callback()
		
	def capturarSeleccionActual(self):
		sel_obj = {
			'nodos': [],
			'conexiones': [],
		}
		
		for objeto in self.escena.GraficosEsc.selectedItems():
			if isinstance(objeto, GraficosdelNodo):
				sel_obj['nodos'].append(objeto.nodo.id)
			elif isinstance(objeto, GraficosdeConexion):
				sel_obj['conexiones'].append(objeto.linea.id)
		return sel_obj
	
	def crear_Marca_Historial(self, desc):
		marca_historial = {
			'desc': desc,
			'snapshot': self.escena.serializacion(),
			'selection': self.capturarSeleccionActual(),
		}
		return marca_historial
		
	def RestaurarMarcaHistorial(self, marca_historial):
		if DEBUG: print("RHS:", marca_historial['desc'])
		
		try:
			self.deshacer_seleccion_ha_cambiado = False
			seleccion_anterior = self.capturarSeleccionActual()
			if DEBUG_SELECCION: print("Nodos seleccionados antes de restaurar:", seleccion_anterior['nodos'])
			
			self.escena.deserializacion(marca_historial['snapshot'])
			
			# Restaurar selección.
			# Primero se limpia la seleccion.
			for conexion in self.escena.Conexiones: conexion.GraficosDeConexion.setSelected(False)
			# Luego, se restauran las selecciones desde el historial.
			for conexion_id in marca_historial['selection']['conexiones']:
				for conexion in self.escena.Conexiones:
					if conexion.id == conexion_id:
						conexion.GraficosDeConexion.setSelected(True)
						break
			
			for nodo in self.escena.Nodos: nodo.Nodograficas.setSelected(False)
			for nodo_id in marca_historial['selection']['nodos']:
				for nodo in self.escena.Nodos:
					if nodo.id == nodo_id:
						nodo.Nodograficas.setSelected(True)
						break
			
			seleccion_actual = self.capturarSeleccionActual()
			if DEBUG_SELECCION: print("Nodos seleccionados después de restaurar:", seleccion_actual['nodos'])
			
			self.escena._ultimos_objetos_seleccionados = self.escena.objetosSeleccionados()
			
			# Si la selección es diferente antes y después, activar flag.
			if seleccion_actual['nodos'] != seleccion_anterior['nodos'] or seleccion_actual['conexiones'] != seleccion_anterior['conexiones']:
				if DEBUG_SELECCION: print("\nESCENA: La seleccion ha cambiado")
				self.deshacer_seleccion_ha_cambiado = True
						
		except Exception as e: dump_exception(e)
		