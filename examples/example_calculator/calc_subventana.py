from PyQt5.QtCore import *
from nodeeditor.Widget_de_nodos import EditorDeNodos


class SubVenCalc(EditorDeNodos):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self.definirtitulo()
		
		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		
		self._close_event_listeners = []
		
	def definirtitulo(self):
		self.setWindowTitle(self.obtenerNombreAmigablealUsuario())
		
	def agregarCloseEventListeners(self, callback):
		self._close_event_listeners.append(callback)
		
	def closeEvent(self, event):
		for callback in self._close_event_listeners: callback(self, event)
		