from GraficosdelNodo import QDMGraphicsNode


class Nodo:
	def __init__(self, scene, title="Nodo desconocido"):
		self.scene = scene
		self.title = title
		
		self.Nodograficas = QDMGraphicsNode(self, self.title)
		
		self.scene.agregarnodo(self)
		self.scene.GraficosEsc.addItem(self.Nodograficas)
		
		self.inputs = []
		self.outputs = []
