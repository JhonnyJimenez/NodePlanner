from GraficosdelaEscena_vp import GraficosdelaEscenaVP


class Escena:
	def __init__(self):
		self.Nodos = []
		self.Conexiones = []
		
		self.Escena_Ancho = 64000
		self.Escena_Alto = 64000
		
		self.GraficosEsc = GraficosdelaEscenaVP(self)
		self.GraficosEsc.config_esc(self.Escena_Ancho, self.Escena_Alto)
	
	def agregarnodo(self, nodo):
		self.Nodos.append(nodo)
	
	def agregarconexion(self, conexion):
		self.Conexiones.append(conexion)
	
	def eliminarnodo(self, nodo):
		self.Nodos.remove(nodo)
	
	def eliminarconexion(self, conexion):
		self.Conexiones.remove(conexion)
