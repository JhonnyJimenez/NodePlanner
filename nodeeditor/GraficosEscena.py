# Gráficos de la escena (Ventana_principal).
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosEscena(QGraphicsScene):
	objetoSeleccionado = pyqtSignal()
	objetosNoSeleccionados = pyqtSignal()
	
	def __init__(self, escena, parent=None):
		super().__init__(parent)
		
		self.escena = escena
		
		# Configuraciones
		self.GrillaSize = 20
		self.GrillaCuadros = 5
		
		self._ColordeFondo = QColor("#393939")
		self._ColorClaro = QColor("#2f2f2f")
		self._ColorOscuro = QColor("#292929")
		
		self._LapizClaro = QPen(self._ColorClaro)
		self._LapizClaro.setWidth(1)
		self._LapizOscuro = QPen(self._ColorOscuro)
		self._LapizOscuro.setWidth(2)
		
		self.setBackgroundBrush(self._ColordeFondo)
		
	# El evento de arrastre (arrastrar y soltar) no funcionará hasta que dragMoveEvent sea sobreescrito.
	def dragMoveEvent(self, event):
		pass
		
	def config_esc(self, width, height):
		self.setSceneRect(-width // 2, -height // 2, width, height)

	def drawBackground(self, painter, rect):
		super().drawBackground(painter, rect)
		
		# La grilla.
		izquierda = int(math.floor(rect.left()))
		derecha = int(math.ceil(rect.right()))
		techo = int(math.floor(rect.top()))
		piso = int(math.ceil(rect.bottom()))
		
		marco_izq = izquierda - (izquierda % self.GrillaSize)
		marco_techo = techo - (techo % self.GrillaSize)
		
		# Cálculo las líneas a dibujar.
		lineas_claras, lineas_oscuras = [], []
		for x in range(marco_izq, derecha, self.GrillaSize):
			if x % (self.GrillaSize * self.GrillaCuadros) != 0:
				lineas_claras.append(QLine(x, techo, x, piso))
			else:
				lineas_oscuras.append(QLine(x, techo, x, piso))
		for y in range(marco_techo, piso, self.GrillaSize):
			if y % (self.GrillaSize * self.GrillaCuadros) != 0:
				lineas_claras.append(QLine(izquierda, y, derecha, y))
			else:
				lineas_oscuras.append(QLine(izquierda, y, derecha, y))
				
		# Las líneas.
		painter.setPen(self._LapizClaro)
		painter.drawLines(*lineas_claras)
		
		painter.setPen(self._LapizOscuro)
		painter.drawLines(*lineas_oscuras)
