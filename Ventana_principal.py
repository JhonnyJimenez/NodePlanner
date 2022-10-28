from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GraficosdelaVista_vp import GraficosdelaVistaVP
from Escena import Escena
from Nodo import Nodo


class EditorDeNodos(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.stylesheet_filename = 'EstiloNodo.qss'
		self.loadStylesheet(self.stylesheet_filename)
		
		# Tamaño de la ventana
		self.setGeometry(100, 100, 800, 600)
		
		# Administrador de espacio en pantalla
		self.AdminDeEspEnPan = QVBoxLayout()
		self.AdminDeEspEnPan.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.AdminDeEspEnPan)
		
		# Gráficos (Escena)
		self.escena = Escena()
		# Gráficos (Vista)
		self.Vista = GraficosdelaVistaVP(self.escena.GraficosEsc, self)
		self.AdminDeEspEnPan.addWidget(self.Vista)
		
		Nodo(self.escena, "Nodo de personaje")
		
		self.setWindowTitle("NodePlanner - Versión alpha")
		self.show()

	def loadStylesheet(self, filename):
		print('Style loading:', filename)
		file = QFile(filename)
		file.open(QFile.ReadOnly | QFile.Text)
		stylesheet = file.readAll()
		QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))