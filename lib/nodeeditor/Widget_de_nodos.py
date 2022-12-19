import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from lib.nodeeditor.GraficosVista import GraficosdelaVistaVP
from lib.nodeeditor.Escena import Escena, InvalidFile
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Conexiones import Conexion, recta, bezier
from lib.nodeeditor.Utilidades import CuadroDialogo, dump_exception


class EditorDeNodos(QWidget):
	ClaseEscena = Escena
	ClaseGraficosVista = GraficosdelaVistaVP

	def __init__(self, elemento_padre = None):
		super().__init__(elemento_padre)

		# La subclases QLayout posicionan los subwidgets en el espacio que toman de su elemento superior.
		self.organizador = QVBoxLayout()
		# La clase QGraphicsScene proporciona una superficie para contener una gran cantidad de gráficos 2D.
		self.escena = self.__class__.ClaseEscena()
		# La clase QGraphicsView muestra el contenido de una clase QGraphicsScene en una ventana desplazable.
		self.graficador_visual = self.__class__.ClaseGraficosVista(self.escena.graficador_de_la_escena, self)

		self.filename = None

		self.interfaz()

	def interfaz(self):
		self.organizador.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.organizador)
		self.organizador.addWidget(self.graficador_visual)

		# self.añadir_contenido_de_prueba()

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
			CuadroDialogo(
							self, "Warning", "Error al abrir %s" % (os.path.basename(filename)),
							"¡%s no existe!" % (os.path.basename(filename))
							)
			return False
		except InvalidFile as e:
			dump_exception(e)
			# QApplication.restoreOverrideCursor()
			CuadroDialogo(
							self, "Warning", "Error al abrir %s" % (os.path.basename(filename)),
							"%s no es un archivo JSON válido" % (os.path.basename(filename))
							)
			return False
		finally:
			QApplication.restoreOverrideCursor()

	def guardararchivo(self, filename = None):
		# Cuando se llame sin parámetros no podremos almacenar el nombre de archivo.
		if filename is not None:
			self.filename = filename
		QApplication.setOverrideCursor(Qt.WaitCursor)
		self.escena.guardarArchivo(self.filename)
		QApplication.restoreOverrideCursor()
		return True

	def agregadodenodos(self):
		nodo1 = Nodo(self.escena, "Mi asombroso nodo 1", entradas = [0, 0, 0], salidas = [1])
		nodo2 = Nodo(self.escena, "Mi asombroso nodo 2", entradas = [3, 3, 3], salidas = [1])
		nodo3 = Nodo(self.escena, "Mi asombroso nodo 3", entradas = [2, 2, 2], salidas = [1])
		nodo1.definirposicion(-350, -250)
		nodo2.definirposicion(-75, 0)
		nodo3.definirposicion(200, -200)

		Conexion(self.escena, nodo1.salidas[0], nodo2.entradas[0])
		Conexion(self.escena, nodo2.salidas[0], nodo3.entradas[0])
		Conexion(self.escena, nodo1.salidas[0], nodo3.entradas[2])

		self.escena.historial.marcaInicialdelHistorial()

	def añadir_contenido_de_prueba(self):
		relleno_verde = QBrush(QColorConstants.Green)
		lápiz_de_contorno = QPen(QColorConstants.Black)
		lápiz_de_contorno.setWidth(2)

		rectángulo = self.escena.graficador_de_la_escena.addRect(
				-100, -100, 80, 100, lápiz_de_contorno,
				relleno_verde
				)
		rectángulo.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

		texto = self.escena.graficador_de_la_escena.addText("¡Este es mi impresionante texto!", QFont("Ubuntu"))
		texto.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
		texto.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		texto.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

		boton = QPushButton("¡Hola, mundo!")
		widget_1 = self.escena.graficador_de_la_escena.addWidget(boton)
		widget_1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		widget_1.setPos(0, 30)

		editor = QTextEdit()
		widget_2 = self.escena.graficador_de_la_escena.addWidget(editor)
		widget_2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
		widget_2.setPos(0, 60)

		línea = self.escena.graficador_de_la_escena.addLine(-200, -200, 400, 100, lápiz_de_contorno)
		línea.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		línea.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
