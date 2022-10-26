from GraficosdelaEscena_vp import GraficosdelaEscenaVP


class Escena:
	def __init__(self):
		self.Nodos = []
		self.Bordes = []
		
		self.Escena_Ancho = 64000
		self.Escena_Alto = 64000
		
		self.GraficosEsc = GraficosdelaEscenaVP(self)
		self.GraficosEsc.config_esc(self.Escena_Ancho, self.Escena_Alto)
	
	def agregarnodo(self, nodo):
		self.Nodos.append(nodo)
	
	def agregarborde(self, borde):
		self.Bordes.append(borde)
	
	def eliminarnodo(self, nodo):
		self.Nodos.remove(nodo)
	
	def eliminarborde(self, borde):
		self.Bordes.remove(borde)
