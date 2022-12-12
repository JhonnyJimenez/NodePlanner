from nodeeditor.GraficosdeConexion import GraficosdeConexion
from nodeeditor.GraficosdelNodo import GraficosdelNodo

from nodeeditor.Utilidades import dump_exception

DEBUG = False


class HistorialEscena:
	def __init__(self, escena):
		self.escena = escena
		
		self.historial_nuevo()
		self.limite_historial = 32
		
		self._modificadores_del_historial_listeners = []
		
	def historial_nuevo(self):
		self.listado_historial = []
		self.pos_act_historial = -1
		
	def marcaInicialdelHistorial(self):
		self.almacenarHistorial("Marca inicial del historial")
		
	def habilitarDeshacer(self):
		return self.pos_act_historial > 0
	
	def habilitarRehacer(self):
		return self.pos_act_historial + 1 < len(self.listado_historial)
	
	def deshacer(self):
		if DEBUG: print("Undo")
		
		if self.habilitarDeshacer():
			self.pos_act_historial -= 1
			self.restaurarHistorial()
			self.escena._elementos_modificados = True
		
	def rehacer(self):
		if DEBUG: print("Redo")
		
		if self.habilitarRehacer():
			self.pos_act_historial += 1
			self.restaurarHistorial()
			self.escena._elementos_modificados = True
			
	def agregarmodificadoresdelhistorialisteners(self, callback):
		self._modificadores_del_historial_listeners.append(callback)
		
	def restaurarHistorial(self):
		if DEBUG: print("Restaurando historial",
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		self.RestaurarMarcaHistorial(self.listado_historial[self.pos_act_historial])
		for callback in self._modificadores_del_historial_listeners: callback()


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
		
	def crear_Marca_Historial(self, desc):
		sel_obj = {
			'nodos': [],
			'conexiones': [],
		}
		
		for objeto in self.escena.GraficosEsc.selectedItems():
			if isinstance(objeto, GraficosdelNodo):
				sel_obj['nodos'].append(objeto.nodo.id)
			elif isinstance(objeto, GraficosdeConexion):
				sel_obj['conexiones'].append(objeto.linea.id)
		
		marca_historial = {
			'desc': desc,
			'snapshot': self.escena.serializacion(),
			'selection': sel_obj,
		}
		return marca_historial
		
	def RestaurarMarcaHistorial(self, marca_historial):
		if DEBUG: print("RHS:", marca_historial['desc'])
		
		try:
			self.escena.deserializacion(marca_historial['snapshot'])
			
			# restaurar selección.
			for conexion_id in marca_historial['selection']['conexiones']:
				for conexion in self.escena.Conexiones:
					if conexion.id == conexion_id:
						conexion.GraficosDeConexion.setSelected(True)
						break
			
			for nodo_id in marca_historial['selection']['nodos']:
				for nodo in self.escena.Nodos:
					if nodo.id == nodo_id:
						nodo.Nodograficas.setSelected(True)
						break
						
		except Exception as e: dump_exception(e)