from PyQt5.QtWidgets import *


class ContenidoDelNodo(QWidget):
	def __init__(self, nodo, parent=None):
		self.nodo = nodo
		super().__init__(parent)
		
		self.initui()
		
	def initui(self):
		self.lienzo = QVBoxLayout()
		self.lienzo.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.lienzo)
		
		self.wdg_label = QLabel("Some title")
		self.lienzo.addWidget(self.wdg_label)
		self.lienzo.addWidget(EditordeTexto("Mira, un texto"))
		
	def ConfigEdicion(self, value):
		self.nodo.escena.GraficosEsc.views()[0].eventoedicion = value
		
class EditordeTexto(QTextEdit):
	def focusInEvent(self, event):
		self.parentWidget().ConfigEdicion(True)
		super().focusInEvent(event)
	
	def focusOutEvent(self, event):
		self.parentWidget().ConfigEdicion(False)
		super().focusOutEvent(event)