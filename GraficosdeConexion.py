from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosdeConexion(QGraphicsPathItem):
	def __init__(self, linea, parent=None):
		super().__init__(parent)
		
		self.linea = linea
		
		self._color = QColor("#001000")
		self._color_seleccionado = QColor("#00ff00")
		self._pen = QPen(self._color)
		self._pen_seleccionado = QPen(self._color_seleccionado)
		self._pen.setWidth(2)
		self._pen_seleccionado.setWidth(2)
		
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		
		self.setZValue(-1)
		
		self.posicion_origen = [0, 0]
		self.posicion_destino = [200, 100]
		
	def punto_origen(self, x, y):
		self.posicion_origen = [x, y]
	
	def punto_destino(self, x, y):
		self.posicion_destino = [x, y]
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		self.ruta_actualizada()
		
		painter.setPen(self._pen if not self.isSelected() else self._pen_seleccionado)
		painter.setBrush(Qt.NoBrush)
		painter.drawPath(self.path())
		
	def ruta_actualizada(self):
		# Para controlar el dibujo de las conexiones entre nodos.
		raise NotImplemented("Este metodo tiene que ser sobreescrito en las clases hijas")
	
class ConexionLRecta(GraficosdeConexion):
	def ruta_actualizada(self):
		ruta = QPainterPath(QPointF(self.posicion_origen[0], self.posicion_origen[1]))
		ruta.lineTo(self.posicion_destino[0], self.posicion_destino[1])
		self.setPath(ruta)
	
class ConexionLBezier(GraficosdeConexion):
	def ruta_actualizada(self):
		o = self.posicion_origen
		d = self.posicion_destino
		dist = (d[0] - o[0]) * 0.5
		if o[0] > d[0]: dist *= -1
		
		ruta = QPainterPath(QPointF(self.posicion_origen[0], self.posicion_origen[1]))
		ruta.cubicTo(o[0] + dist, o[1], d[0] - dist, d[1], self.posicion_destino[0], self.posicion_destino[1])
		self.setPath(ruta)
	