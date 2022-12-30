from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class ContenidoDelNodo(QWidget, Serializable):
	def __init__(self, nodo, parent=None):
		self.nodo = nodo
		super().__init__(parent)
		
		self.init_ui()
		
	def init_ui(self):
		self.lienzo = QVBoxLayout()
		self.lienzo.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.lienzo)
		
		self.etiqueta = QLabel("Algún título")
		self.lienzo.addWidget(self.etiqueta)
		self.lienzo.addWidget(EditordeTexto("Mira, un texto"))
		
	def configurar_edición(self, value):
		self.nodo.escena.obtener_vista().eventoedicion = value
		
	def serialización(self):
		return OrderedDict([
		
		])
	
	def deserialización(self, data, hashmap={}):
		return True
		
class EditordeTexto(QTextEdit):
	def focusInEvent(self, event):
		self.parentWidget().configurar_edición(True)
		super().focusInEvent(event)
	
	def focusOutEvent(self, event):
		self.parentWidget().configurar_edición(False)
		super().focusOutEvent(event)