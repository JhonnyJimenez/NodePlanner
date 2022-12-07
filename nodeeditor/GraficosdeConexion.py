import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from nodeeditor.Zocalos import *

Conexion_CP_Redondez = 100


class GraficosdeConexion(QGraphicsPathItem):
	def __init__(self, linea, parent=None):
		super().__init__(parent)
		
		self.linea = linea
		
		self._color = QColor("#001000")
		self._color_seleccionado = QColor("#00ff00")
		self._pen = QPen(self._color)
		self._pen_seleccionado = QPen(self._color_seleccionado)
		self._pen_dibujo = QPen(self._color)
		self._pen_dibujo.setStyle(Qt.DashLine)
		self._pen.setWidth(2)
		self._pen_seleccionado.setWidth(2)
		self._pen_dibujo.setWidth(2)
		
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		
		self.setZValue(-1)
		
		self.posicion_origen = [0, 0]
		self.posicion_destino = [200, 100]
		
	def punto_origen(self, x, y):
		self.posicion_origen = [x, y]
	
	def punto_destino(self, x, y):
		self.posicion_destino = [x, y]
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		self.setPath(self.calculo_de_ruta())
		
		if self.linea.zocalo_final is None:
			painter.setPen(self._pen_dibujo)
		else:
			painter.setPen(self._pen if not self.isSelected() else self._pen_seleccionado)
		painter.setBrush(Qt.NoBrush)
		painter.drawPath(self.path())
		
	def cruzadocon(self, p1, p2):
		ruta_de_recorte = QPainterPath(p1)
		ruta_de_recorte.lineTo(p2)
		ruta = self.calculo_de_ruta()
		return ruta_de_recorte.intersects(ruta)
		
	def calculo_de_ruta(self):
		# Para controlar el dibujo de las conexiones entre nodos.
		raise NotImplemented("Este metodo tiene que ser sobreescrito en las clases hijas")
	
	def retangulo_delimitador(self):
		return self.shape().boundingRect()
	
	def shape(self):
		return self.calculo_de_ruta()
	
class ConexionLRecta(GraficosdeConexion):
	def calculo_de_ruta(self):
		ruta = QPainterPath(QPointF(self.posicion_origen[0], self.posicion_origen[1]))
		ruta.lineTo(self.posicion_destino[0], self.posicion_destino[1])
		return ruta
	
class ConexionLBezier(GraficosdeConexion):
	def calculo_de_ruta(self):
		o = self.posicion_origen
		d = self.posicion_destino
		dist = (d[0] - o[0]) * 0.5
		
		cpx_o = +dist
		cpx_d = -dist
		cpy_o = 0
		cpy_d = 0
		
		if self.linea.zocalo_origen is not None:
			zocalo_inicial_pos = self.linea.zocalo_origen.posicion
			
			if (o[0] > d[0] and zocalo_inicial_pos in (Derecha_arriba, Derecha_abajo)) or (o[0] < d[0] and zocalo_inicial_pos in (Izquierda_arriba, Izquierda_abajo)):
				cpx_d *= -1
				cpx_o *= -1
				
				cpy_d = (
					(o[1] - d[1]) / math.fabs(
						(o[1] - d[1]) if (o[1] - d[1]) != 0 else 0.00001
					)
				) * Conexion_CP_Redondez
				cpy_o = (
					(d[1] - o[1]) / math.fabs(
						(d[1] - o[1]) if (d[1] - o[1]) != 0 else 0.00001
					)
				) * Conexion_CP_Redondez
		
		ruta = QPainterPath(QPointF(self.posicion_origen[0], self.posicion_origen[1]))
		ruta.cubicTo(o[0] + cpx_o, o[1] + cpy_o, d[0] + cpx_d, d[1] + cpy_d, self.posicion_destino[0], self.posicion_destino[1])
		return ruta
	