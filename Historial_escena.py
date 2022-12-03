from GraficosdeConexion import GraficosdeConexion


DEBUG = False


class HistorialEscena:
	def __init__(self, escena):
		self.escena = escena
		
		self.listado_historial = []
		self.pos_act_historial = -1
		self.limite_historial = 32
	
	def deshacer(self):
		if DEBUG: print("Undo")
		
		if self.pos_act_historial > 0:
			self.pos_act_historial -= 1
			self.restaurarHistorial()
		
	def rehacer(self):
		if DEBUG: print("Redo")
		
		if self.pos_act_historial + 1 < len(self.listado_historial):
			self.pos_act_historial += 1
			self.restaurarHistorial()
		
	def restaurarHistorial(self):
		if DEBUG: print("Restaurando historial",
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		self.MarcaRestaurarHistorial(self.listado_historial[self.pos_act_historial])


	def almacenarHistorial(self, desc, setModified=False):
		if setModified:
			self.escena.elementos_modificados = True
		
		if DEBUG: print("Almacenando historial", '"%s"' % desc,
						".... posición actual: @%d" % self.pos_act_historial,
						"(%d)" % len(self.listado_historial))
		
		# Si la posición actual del historial no es el último de la lista.
		if self.pos_act_historial - 1 < len(self.listado_historial):
			self.listado_historial = self.listado_historial[0:self.pos_act_historial+1]
		
		# Historial fuera del límite.
		if self.pos_act_historial + 1 >= self.limite_historial:
			self.listado_historial = self.listado_historial[1:]
			self.pos_act_historial -= 1
		
		hs = self.crear_Marca_Historial(desc)
		
		self.listado_historial.append(hs)
		self.pos_act_historial += 1
		if DEBUG: print(" == configurando posición a:", self.pos_act_historial)
		
		
	def crear_Marca_Historial(self, desc):
		sel_obj = {
			'nodos': [],
			'conexiones': [],
		}
		
		for objetos in self.escena.GraficosEsc.selectedItems():
			if hasattr(objetos, 'Nodo'):
				sel_obj['nodos'].append(objetos.nodo.id)
			elif isinstance(objetos, GraficosdeConexion):
				sel_obj['conexiones'].append(objetos.linea.id)
		
		marca_historial = {
			'desc': desc,
			'snapshot': self.escena.serializacion(),
			'selection': sel_obj,
		}
		return marca_historial
		
	def MarcaRestaurarHistorial(self, marca_historial):
		if DEBUG: print("RHS:", marca_historial['desc'])
		
		self.escena.deserializacion(marca_historial['snapshot'])
		
		# restaurar selección.
		for conexion_id in marca_historial['selection']['conexiones']:
			for conexion in self.escena.Conexiones:
				if conexion.id == conexion_id:
					conexion.GraficosDeConexion.setSelected(True)
					break
		
		for nodo_id in marca_historial['selection']['nodos']:
			for nodo in self.escena.nodos:
				if nodo.id == nodo_id:
					nodo.Nodograficas.setSelected(True)
					break
