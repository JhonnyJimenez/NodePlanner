DEBUG = True


class HistorialEscena():
	def __init__(self, escena):
		self.escena = escena
		
		self.listado_historial = []
		self.pos_act_historial = -1
		self.limite_historial = 8
	
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


	def almacenarHistorial(self, desc):
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
		return desc
		
	def MarcaRestaurarHistorial(self, marca_historial):
		if DEBUG: print("RHS:", marca_historial)
