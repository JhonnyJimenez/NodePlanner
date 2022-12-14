import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

Conexion_CP_Redondez = 100


class GraficosdeConexion(QGraphicsPathItem):
	def __init__(self, linea, parent=None):
		super().__init__(parent)
		
		self.linea = linea
		
		# init de señales.
		self._ultimo_estado_de_seleccion = False
		self.hovered = False
		
		# init de variables.
		self.posicion_origen = [0, 0]
		self.posicion_destino = [200, 100]
		
		self.initAssets()
		self.initUI()

	def initUI(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setAcceptHoverEvents(True)
		self.setZValue(-1)
		
	def initAssets(self):
		self._color = self._default_color = QColor("#001000")
		self._color_seleccionado = QColor("#00ff00")
		self._color_hovered = QColor("#FF37A6FF")
		self._pen = QPen(self._color)
		self._pen_seleccionado = QPen(self._color_seleccionado)
		self._pen_dibujo = QPen(self._color)
		self._pen_hover = QPen(self._color_hovered)
		self._pen_dibujo.setStyle(Qt.DashLine)
		self._pen.setWidthF(3.0)
		self._pen_seleccionado.setWidthF(3.0)
		self._pen_dibujo.setWidthF(3.0)
		self._pen_hover.setWidthF(5.0)
		
	def hacerNoSeleccionable(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable, False)
		self.setAcceptHoverEvents(False)
	
	def cambiarColor(self, color):
		self._color = QColor(color) if type(color) == str else color
		self._pen = QPen(self._color)
		self._pen.setWidthF(3.0)
	
	def definirColordesdeelZocalo(self):
		tipo_zocalo_origen = self.linea.zocalo_inicial_de_dibujado.tipo_zocalo
		tipo_zocalo_final = self.linea.zocalo_final.tipo_zocalo
		if tipo_zocalo_origen != tipo_zocalo_final: return False
		self.cambiarColor(self.linea.zocalo_origen.GraficosZocalos.obtenerColorparaelZocalo(tipo_zocalo_origen))
		
	def seleccionado(self):
		self.linea.escena.GraficosEsc.objetoSeleccionado.emit()
		
	def hacerSeleccion(self, nuevo_estado=True):
		self.setSelected(nuevo_estado)
		self._ultimo_estado_de_seleccion = nuevo_estado
		if nuevo_estado: self.seleccionado()
		
	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if self._ultimo_estado_de_seleccion != self.isSelected():
			self.linea.escena.restaurarUltimoEstadodeSeleccion()
			self._ultimo_estado_de_seleccion = self.isSelected()
			self.seleccionado()
			
	def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.hovered = True
		self.update()
		
	def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.hovered = False
		self.update()
		
	def punto_origen(self, x, y):
		self.posicion_origen = [x, y]
	
	def punto_destino(self, x, y):
		self.posicion_destino = [x, y]
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		self.setPath(self.calculo_de_ruta())
		
		painter.setBrush(Qt.NoBrush)
		
		if self.hovered and self.linea.zocalo_final is not None:
			painter.setPen(self._pen_hover)
			painter.drawPath(self.path())
		
		if self.linea.zocalo_final is None:
			painter.setPen(self._pen_dibujo)
		else:
			painter.setPen(self._pen if not self.isSelected() else self._pen_seleccionado)
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
			zoc_ini = self.linea.zocalo_origen.esEntrada
			zoc_fin = self.linea.zocalo_origen.esSalida
			
			if (o[0] > d[0] and zoc_fin) or (o[0] < d[0] and zoc_ini):
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
	