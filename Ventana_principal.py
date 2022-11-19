from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from GraficosdelaVista_vp import GraficosdelaVistaVP
from Escena import Escena
from Nodo import Nodo
from Conexiones import Conexion, recta, bezier


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
		
		self.agregadodenodos()
		
		self.setWindowTitle("NodePlanner - Versión alpha")
		self.show()

	def loadStylesheet(self, filename):
		print('Style loading:', filename)
		file = QFile(filename)
		file.open(QFile.ReadOnly | QFile.Text)
		stylesheet = file.readAll()
		QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
		
	def agregadodenodos(self):
		nodo1 = Nodo(self.escena, "Nodo cronista", entradas=[0, 0, 0], salidas=[1])
		nodo2 = Nodo(self.escena, "Nodo de personaje", entradas=[3, 3, 3], salidas=[1])
		nodo3 = Nodo(self.escena, "Nodo de juguete", entradas=[2, 2, 2], salidas=[1])
		nodo1.definirposicion(-350, -250)
		nodo2.definirposicion(-75, 0)
		nodo3.definirposicion(200, -150)
		
		conexion1 = Conexion(self.escena, nodo1.salidas[0], nodo2.entradas[0])
		conexion2 = Conexion(self.escena, nodo2.salidas[0], nodo3.entradas[0])