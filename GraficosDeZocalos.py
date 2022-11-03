from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class GraficosDeZocalos(QGraphicsItem):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		#Usa números enteros, porque con decimales, el programa no funcionará (Y PyCharm no te dará ninguna pista de porqué falla.
		self.radio = 6
		self.grosor_contorno = 1
		self._color_de_fondo = QColor("#FFFF7700")
		self._color_contorno = QColor("#FF000000")
		
		self._pen = QPen(self._color_contorno)
		self._pen.setWidth(self.grosor_contorno)
		self._brush = QBrush(self._color_de_fondo)
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		# Dibujando el círculo
		painter.setBrush(self._brush)
		painter.setPen(self._pen)
		painter.drawEllipse(-self.radio, -self.radio, 2 * self.radio, 2 * self.radio)
	
	def boundingRect(self):
		return QRectF(
			-self.radio - self.grosor_contorno,
			-self.radio - self.grosor_contorno,
			2 * (self.radio + self.grosor_contorno),
			2 * (self.radio + self.grosor_contorno),
		)
	