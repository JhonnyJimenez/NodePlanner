from GraficosdelNodo import GraficosdelNodo
from ContenidodelNodo import ContenidoDelNodo


class Nodo:
	def __init__(self, escena, titulo="Nodo desconocido"):
		self.escena = escena
		self.titulo = titulo
		
		self.contenido = ContenidoDelNodo()
		
		self.Nodograficas = GraficosdelNodo(self)
		
		self.escena.agregarnodo(self)
		self.escena.GraficosEsc.addItem(self.Nodograficas)
		
		self.inputs = []
		self.outputs = []
