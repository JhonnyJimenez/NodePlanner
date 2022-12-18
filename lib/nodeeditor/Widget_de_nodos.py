import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lib.nodeeditor.GraficosVista import GraficosdelaVistaVP
from lib.nodeeditor.Escena import Escena, InvalidFile
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Conexiones import Conexion, recta, bezier
from lib.nodeeditor.Utilidades import CuadroDialogo, dump_exception


class EditorDeNodos(QWidget):
	ClaseEscena = Escena
	ClaseGraficosVista = GraficosdelaVistaVP
	
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.filename = None
		
		self.initUI()
		
	def initUI(self):
		# Administrador de espacio en pantalla
		self.AdminDeEspEnPan = QVBoxLayout()
		self.AdminDeEspEnPan.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.AdminDeEspEnPan)
		
		# Gráficos (Escena)
		self.escena = self.__class__.ClaseEscena()
		
		# Gráficos (Vista)
		self.Vista = self.__class__.ClaseGraficosVista(self.escena.GraficosEsc, self)
		self.AdminDeEspEnPan.addWidget(self.Vista)

	def haycambios(self):
		return self.escena.haycambios()

	def hayNombredeArchivo(self):
		return self.filename is not None
	
	def objetosSeleccionados(self):
		return self.escena.objetosSeleccionados()
	
	def hayAlgoSeleccionado(self):
		return self.objetosSeleccionados() != []
	
	def habilitarDeshacer(self):
		return self.escena.historial.habilitarDeshacer()
	
	def habilitarRehacer(self):
		return self.escena.historial.habilitarRehacer()
	
	def obtenerNombreAmigablealUsuario(self):
		nombre = os.path.basename(self.filename) if self.hayNombredeArchivo() else "Nuevo archivo"
		return nombre + ("*" if self.haycambios() else "")
	
	def nuevoarchivo(self):
		self.escena.limpiarEscena()
		self.filename = None
		self.escena.historial.historial_nuevo()
		self.escena.historial.marcaInicialdelHistorial()
	
	def leerarchivo(self, filename):
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			self.escena.abrirArchivo(filename)
			self.filename = filename
			self.escena.historial.historial_nuevo()
			self.escena.historial.marcaInicialdelHistorial()
			return True
		except FileNotFoundError as e:
			dump_exception(e)
			CuadroDialogo(self, "Warning", "Error al abrir %s" % (os.path.basename(filename)),
						  "¡%s no existe!" % (os.path.basename(filename)))
			return False
		except InvalidFile as e:
			dump_exception(e)
			# QApplication.restoreOverrideCursor()
			CuadroDialogo(self, "Warning", "Error al abrir %s" % (os.path.basename(filename)),
						  "%s no es un archivo JSON válido" % (os.path.basename(filename)))
			return False
		finally:
			QApplication.restoreOverrideCursor()
	
	def guardararchivo(self, filename=None):
		# Cuando se llame sin parámetros no podremos almacenar el nombre de archivo.
		if filename is not None: self.filename = filename
		QApplication.setOverrideCursor(Qt.WaitCursor)
		self.escena.guardarArchivo(self.filename)
		QApplication.restoreOverrideCursor()
		return True
	
	def agregadodenodos(self):
		nodo1 = Nodo(self.escena, "Mi asombroso nodo 1", entradas=[0, 0, 0], salidas=[1])
		nodo2 = Nodo(self.escena, "Mi asombroso nodo 2", entradas=[3, 3, 3], salidas=[1])
		nodo3 = Nodo(self.escena, "Mi asombroso nodo 3", entradas=[2, 2, 2], salidas=[1])
		nodo1.definirposicion(-350, -250)
		nodo2.definirposicion(-75, 0)
		nodo3.definirposicion(200, -200)
		
		conexion1 = Conexion(self.escena, nodo1.salidas[0], nodo2.entradas[0])
		conexion2 = Conexion(self.escena, nodo2.salidas[0], nodo3.entradas[0])
		conexion3 = Conexion(self.escena, nodo1.salidas[0], nodo3.entradas[2])
		
		self.escena.historial.marcaInicialdelHistorial()
		