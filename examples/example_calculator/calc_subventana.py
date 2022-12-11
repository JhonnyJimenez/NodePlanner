from PyQt5.QtCore import *
from nodeeditor.Widget_de_nodos import EditorDeNodos


class SubVenCalc(EditorDeNodos):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self.definirtitulo()
		
		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		
	def definirtitulo(self):
		self.setWindowTitle(self.obtenerNombreAmigablealUsuario())