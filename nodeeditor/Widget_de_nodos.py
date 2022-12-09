import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.GraficosdelaVista_vp import GraficosdelaVistaVP
from nodeeditor.Escena import Escena
from nodeeditor.Nodo import Nodo
from nodeeditor.Conexiones import Conexion, recta, bezier


class EditorDeNodos(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.filename = None
		
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

	def haycambios(self):
		return self.escena.elementos_modificados

	def confirmarsihaynombredearchivo(self):
		return self.filename is not None
	
	def obtenerNombreAmigablealUsuario(self):
		nombre = os.path.basename(self.filename) if self.confirmarsihaynombredearchivo() else "Nuevo archivo"
		return nombre + ("*" if self.haycambios() else "")
	
	def agregadodenodos(self):
		nodo1 = Nodo(self.escena, "Nodo cronista", entradas=[0, 0, 0], salidas=[1])
		nodo2 = Nodo(self.escena, "Nodo de personaje", entradas=[3, 3, 3], salidas=[1])
		nodo3 = Nodo(self.escena, "Nodo de juguete", entradas=[2, 2, 2], salidas=[1])
		nodo1.definirposicion(-350, -250)
		nodo2.definirposicion(-75, 0)
		nodo3.definirposicion(200, -150)
		
		conexion1 = Conexion(self.escena, nodo1.salidas[0], nodo2.entradas[0])
		conexion2 = Conexion(self.escena, nodo2.salidas[0], nodo3.entradas[0])
		