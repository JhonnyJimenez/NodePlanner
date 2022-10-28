from PyQt5.QtWidgets import *


class ContenidoDelNodo(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.initui()
		
	def initui(self):
		self.lienzo = QVBoxLayout()
		self.lienzo.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.lienzo)
		
		self.wdg_label = QLabel("Some title")
		self.lienzo.addWidget(self.wdg_label)
		self.lienzo.addWidget(QTextEdit("Mira, un texto"))