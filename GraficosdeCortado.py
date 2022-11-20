from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Recortado(QGraphicsItem):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.linea_puntos = []
		
		self._pen = QPen(Qt.white)
		self._pen.setWidth(2)
		self._pen.setDashPattern([3, 3])
		
		self.setZValue(2)
	
	def boundingRect(self):
		return QRectF(0, 0, 1, 1)
	
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setBrush(Qt.NoBrush)
		painter.setPen(self._pen)
		
		poly = QPolygonF(self.linea_puntos)
		painter.drawPolyline(poly)
		