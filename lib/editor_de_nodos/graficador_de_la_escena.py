import math
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import QLineF
from PyQt6.QtGui import QColor, QPen

# Estas dos variables siempre son números enteros.
TAMAÑO_DE_LA_CUADRÍCULA = 20
CANTIDAD_DE_CUADROS_EN_LA_CUADRICULA = 5


class GraficadorDeLaEscena(QGraphicsScene):
	def __init__(self, elemento_superior = None):
		super().__init__(elemento_superior)

		# Declaraciones:
		#   Tamaño de la escena.
		self.anchura_de_la_escena, self.altura_de_la_escena = 64000, 64000

		#   Configuraciones de la cuadrícula.
		self.tamaño_de_la_cuadrícula = int(TAMAÑO_DE_LA_CUADRÍCULA)
		self.cantidad_de_cuadros_en_la_cuadrícula = int(CANTIDAD_DE_CUADROS_EN_LA_CUADRICULA)

		#   Colores.
		self._color_para_el_fondo = QColor("#393939")
		self._color_claro = QColor("#2f2f2f")
		self._color_oscuro = QColor("#292929")

		#   Lapíces.
		self._lápiz_claro = QPen(self._color_claro)
		self._lápiz_oscuro = QPen(self._color_oscuro)

		# Configuraciones.
		#   Configuraciones de los lápices.
		self._lápiz_claro.setWidthF(1)
		self._lápiz_oscuro.setWidthF(3)

		# Rectángulo de la escena.
		#   La escena comienza desde la mitad de su tamaño negativo para terminar en la mitad positiva.
		#   La doble barra hace division devolviendo un número entero.
		self.setSceneRect(
							(self.anchura_de_la_escena // -2), (self.altura_de_la_escena // -2),
							self.anchura_de_la_escena, self.altura_de_la_escena
							)

		#   Rellenado del fondo.
		self.setBackgroundBrush(self._color_para_el_fondo)

	def drawBackground(self, dibujante, rectángulo):
		super().drawBackground(dibujante, rectángulo)

		# Rectángulo de dibujado.
		izquierda = int(math.floor(rectángulo.left()))
		derecha = int(math.ceil(rectángulo.right()))
		arriba = int(math.floor(rectángulo.top()))
		abajo = int(math.ceil(rectángulo.bottom()))

		límite_izquierdo = izquierda - (izquierda % self.tamaño_de_la_cuadrícula)
		límite_superior = arriba - (arriba % self.tamaño_de_la_cuadrícula)

		líneas_delgadas, líneas_gruesas = [], []

		#   Verticales.
		for valor_x in range(límite_izquierdo, derecha, self.tamaño_de_la_cuadrícula):
			if (valor_x % (self.cantidad_de_cuadros_en_la_cuadrícula * self.tamaño_de_la_cuadrícula)) != 0:
				líneas_delgadas.append(QLineF(valor_x, arriba, valor_x, abajo))
			else:
				líneas_gruesas.append(QLineF(valor_x, arriba, valor_x, abajo))

		#   Horizontales.
		for valor_y in range(límite_superior, abajo, self.tamaño_de_la_cuadrícula):
			if (valor_y % (self.cantidad_de_cuadros_en_la_cuadrícula * self.tamaño_de_la_cuadrícula)) != 0:
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
