import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lib.nodeeditor.GraficosVista import GraficadorVisual
from lib.nodeeditor.Escena import Escena, InvalidFile
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Conexiones import Conexion, recta, bezier
from lib.nodeeditor.Utilidades import CuadroDialogo, dump_exception


class EditordeNodos(QWidget):
	ClaseEscena = Escena
	ClaseGraficosVista = GraficadorVisual
	
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.filename = None
		
		self.init_ui()
		
	def init_ui(self):
		# Administrador de espacio en pantalla
		self.administrador_de_espacio_en_pantalla = QVBoxLayout()
		self.administrador_de_espacio_en_pantalla.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.administrador_de_espacio_en_pantalla)
		
		# Gráficos (Escena)
		self.escena = self.__class__.ClaseEscena()
		
		# Gráficos (Vista)
		self.Vista = self.__class__.ClaseGraficosVista(self.escena.graficador_de_la_escena, self)
		self.administrador_de_espacio_en_pantalla.addWidget(self.Vista)

	def haycambios(self):
		return self.escena.hay_cambios()

	def hay_nombre_de_archivo(self):
		return self.filename is not None
	
	def objetos_seleccionados(self):
		return self.escena.objetos_seleccionados()
	
	def hay_algo_seleccionado(self):
		return self.objetos_seleccionados() != []
	
	def habilitar_deshacer(self):
		return self.escena.historial.habilitar_deshacer()
	
	def habilitar_rehacer(self):
		return self.escena.historial.habilitar_rehacer()
	
	def obtener_nombre_amigable_al_usuario(self):
		nombre = os.path.basename(self.filename) if self.hay_nombre_de_archivo() else "Nuevo archivo"
		return nombre + ("*" if self.haycambios() else "")
	
	def nuevo_archivo(self):
		self.escena.limpiar_escena()
		self.filename = None
		self.escena.historial.historial_nuevo()
		self.escena.historial.marca_inicial_del_historial()
	
	def leer_archivo(self, filename):
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			self.escena.abrir_archivo(filename)
			self.filename = filename
			self.escena.historial.historial_nuevo()
			self.escena.historial.marca_inicial_del_historial()
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
	
	def guardar_archivo(self, filename=None):
		# Cuando se llame sin parámetros no podremos almacenar el nombre de archivo.
		if filename is not None: self.filename = filename
		QApplication.setOverrideCursor(Qt.WaitCursor)
		self.escena.guardar_archivo(self.filename)
		QApplication.restoreOverrideCursor()
		return True
	
	def agregado_de_nodos(self):
		nodo1 = Nodo(self.escena, "Mi asombroso nodo 1", entradas=[0, 0, 0], salidas=[1])
		nodo2 = Nodo(self.escena, "Mi asombroso nodo 2", entradas=[3, 3, 3], salidas=[1])
		nodo3 = Nodo(self.escena, "Mi asombroso nodo 3", entradas=[2, 2, 2], salidas=[1])
		nodo1.definir_posición(-350, -250)
		nodo2.definir_posición(-75, 0)
		nodo3.definir_posición(200, -200)
		
		conexion1 = Conexion(self.escena, nodo1.salidas[0], nodo2.entradas[0])
		conexion2 = Conexion(self.escena, nodo2.salidas[0], nodo3.entradas[0])
		conexion3 = Conexion(self.escena, nodo1.salidas[0], nodo3.entradas[2])
		
		self.escena.historial.marca_inicial_del_historial()
		