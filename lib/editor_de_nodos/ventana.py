from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit
from PyQt6.QtGui import QBrush, QPen, QColorConstants, QFont, QColor
from graficador_de_la_escena import GraficadorDeLaEscena
from graficador_visual import GraficadorVisual


class EditorDeNodos(QWidget):
	def __init__(self, elemento_padre=None):
		super().__init__(elemento_padre)

		# La subclases QLayout posicionan los subwidgets en el espacio que toman de su elemento superior.
		self.organizador = QVBoxLayout()
		# La clase QGraphicsScene proporciona una superficie para contener una gran cantidad de gráficos 2D.
		self.graficador_de_la_escena = GraficadorDeLaEscena()
		# La clase QGraphicsView muestra el contenido de una clase QGraphicsScene en una ventana desplazable.
		self.graficador_visual = GraficadorVisual(self.graficador_de_la_escena, self)

		self.interfaz()

	def interfaz(self):
		# Ventana
		self.setWindowTitle('Editor de nodos')
		self.setGeometry(565, 101, 800, 600)

		self.organizador.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.organizador)
		self.organizador.addWidget(self.graficador_visual)

		# «self.show» siempre va al final, porque las cosas se organizan antes de monstrarse.
		self.show()

		self.añadir_contenido_de_prueba()

	def añadir_contenido_de_prueba(self):
		relleno_verde = QBrush(QColorConstants.Green)
		lápiz_de_contorno = QPen(QColorConstants.Black)
		lápiz_de_contorno.setWidth(2)

		rectángulo = self.graficador_de_la_escena.addRect(-100, -100, 80, 100, lápiz_de_contorno, relleno_verde)
		rectángulo.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

		texto = self.graficador_de_la_escena.addText("¡Este es mi impresionante texto!", QFont("Ubuntu"))
		texto.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
		texto.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		texto.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

		boton = QPushButton("¡Hola, mundo!")
		widget_1 = self.graficador_de_la_escena.addWidget(boton)
		widget_1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		widget_1.setPos(0, 30)

		editor = QTextEdit()
		widget_2 = self.graficador_de_la_escena.addWidget(editor)
		widget_2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
		widget_2.setPos(0, 60)

		línea = self.graficador_de_la_escena.addLine(-200, -200, 400, 100, lápiz_de_contorno)
		línea.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		línea.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
