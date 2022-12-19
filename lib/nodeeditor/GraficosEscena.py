import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosEscena(QGraphicsScene):
	objetoSeleccionado = pyqtSignal()
	objetosNoSeleccionados = pyqtSignal()
	
	def __init__(self, escena, elemento_superior=None):
		super().__init__(elemento_superior)
		
		self.escena = escena

		# Declaraciones
		#   Configuraciones de la cuadrícula.
		self.tamaño_de_la_cuadrícula = 20
		self.cantidad_de_cuadros_en_la_cuadrícula = 5

		#   Colores.
		self._color_para_el_fondo = QColor("#393939")
		self._color_claro = QColor("#2f2f2f")
		self._color_oscuro = QColor("#292929")

		#   Lápices.
		self._lápiz_claro = QPen(self._color_claro)

		self._lápiz_oscuro = QPen(self._color_oscuro)

		# Configuraciones.
		#   Configuraciones de los lápices.
		self._lápiz_claro.setWidth(1)
		self._lápiz_oscuro.setWidth(3)

		#   Rellenado del fondo.
		self.setBackgroundBrush(self._color_para_el_fondo)
		
	# El evento de arrastre (arrastrar y soltar) no funcionará hasta que dragMoveEvent sea sobreescrito.
	def dragMoveEvent(self, event):
		pass
		
	def config_esc(self, width, height):
		# Rectángulo de la escena.
		#   La escena comienza desde la mitad de su tamaño negativo para terminar en la mitad positiva.
		#   La doble barra hace division devolviendo un número entero.
		self.setSceneRect(-width // 2, -height // 2, width, height)

	def drawBackground(self, dibujante, rectángulo):
		super().drawBackground(dibujante, rectángulo)
		
		# Rectángulo donde se dibujará.
		izquierda = int(math.floor(rectángulo.left()))
		derecha = int(math.ceil(rectángulo.right()))
		arriba = int(math.floor(rectángulo.top()))
		abajo = int(math.ceil(rectángulo.bottom()))
		
		límite_izquierdo = izquierda - (izquierda % self.tamaño_de_la_cuadrícula)
		límite_superior = arriba - (arriba % self.tamaño_de_la_cuadrícula)

		líneas_delgadas, líneas_gruesas = [], []

		# Cálculo las líneas a dibujar.
		for valor_x in range(límite_izquierdo, derecha, self.tamaño_de_la_cuadrícula):
			if valor_x % (self.cantidad_de_cuadros_en_la_cuadrícula * self.tamaño_de_la_cuadrícula) != 0:
				líneas_delgadas.append(QLineF(valor_x, arriba, valor_x, abajo))
			else:
				líneas_gruesas.append(QLineF(valor_x, arriba, valor_x, abajo))

		for valor_y in range(límite_superior, abajo, self.tamaño_de_la_cuadrícula):
			if valor_y % (self.cantidad_de_cuadros_en_la_cuadrícula * self.tamaño_de_la_cuadrícula) != 0:
				líneas_delgadas.append(QLineF(izquierda, valor_y, derecha, valor_y))
			else:
				líneas_gruesas.append(QLineF(izquierda, valor_y, derecha, valor_y))
				
		#   Hay situaciones que posibilitan que alguna lista quede vacía (como usar números decimales en las
		#   configuraciones o hacer un nivel exagerado de zoom). Si el método drawLines no tiene datos con los que
		#   trabajar, dará error y cerrará el programa. Aprovechando que el método reitera, el codigo abajo evita
		#   llamar el método si una lista queda vacía.
		if len(líneas_delgadas) != 0:
			dibujante.setPen(self._lápiz_claro)
			dibujante.drawLines(*líneas_delgadas)

		if len(líneas_gruesas) != 0:
			dibujante.setPen(self._lápiz_oscuro)
			dibujante.drawLines(*líneas_gruesas)
