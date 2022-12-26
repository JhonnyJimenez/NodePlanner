from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from lib.nodeeditor.GraficosRutaConexion import EnrutadorRecto, EnrutadorBezier


class GraficosdeConexion(QGraphicsPathItem):
	def __init__(self, linea, parent=None):
		super().__init__(parent)
		
		self.linea = linea
		
		# Crear instancia de nuestra clase de lineas.
		self.enrutador = self.definirClasedeEnrutador()(self)
		
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
		
	def crearCalculadordeRutadeConexion(self):
		self.enrutador = self.definirClasedeEnrutador()(self)
		return self.enrutador
		
	def definirClasedeEnrutador(self):
		from lib.nodeeditor.Conexiones import bezier, recta
		if self.linea.tipo_de_conexion == bezier:
			return EnrutadorBezier
		if self.linea.tipo_de_conexion == recta:
			return EnrutadorRecto
		else:
			return EnrutadorBezier
		
	def hacerNoSeleccionable(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable, False)
		self.setAcceptHoverEvents(False)
	
	def cambiarColor(self, color):
		self._color = QColor(color) if type(color) == str else color
		self._pen = QPen(self._color)
		self._pen.setWidthF(3.0)


	# Esta método es adición mía.
	def cambiarColorGradiente(self, color_1, color_2):
		origen_x = self.linea.zocalo_origen.nodo.obtenerPosiciondeZocaloenEscena(self.linea.zocalo_origen)[0]
		origen_y = self.linea.zocalo_origen.nodo.obtenerPosiciondeZocaloenEscena(self.linea.zocalo_origen)[1]
		final_x = self.linea.zocalo_final.nodo.obtenerPosiciondeZocaloenEscena(self.linea.zocalo_final)[0]
		final_y = self.linea.zocalo_final.nodo.obtenerPosiciondeZocaloenEscena(self.linea.zocalo_final)[1]

		gradiente = QLinearGradient(origen_x, origen_y, final_x, final_y)

		nuevo_color_1 = QColor(color_1) if type(color_1) == str else color_1
		nuevo_color_2 = QColor(color_2) if type(color_2) == str else color_2

		gradiente.setColorAt(0.49, nuevo_color_1)
		gradiente.setColorAt(0.51, nuevo_color_2)

		self._color = gradiente
		self._brush = QBrush(self._color)
		self._pen = QPen(self._brush, 3.0)
		#self._pen.setWidthF(3.0)

	
	def definirColordesdeelZocalo(self):
		tipo_zocalo_origen = self.linea.zocalo_origen.tipo_zocalo
		# Esta es la línea original: tipo_zocalo_origen = self.linea.zocalo_inicial_de_dibujado.tipo_zocalo
		tipo_zocalo_final = self.linea.zocalo_final.tipo_zocalo
		if tipo_zocalo_origen != tipo_zocalo_final:
			return self.cambiarColorGradiente(
					self.linea.zocalo_origen.GraficosZocalos.obtenerColorparaelZocalo(tipo_zocalo_origen),
					self.linea.zocalo_origen.GraficosZocalos.obtenerColorparaelZocalo(tipo_zocalo_final)
					)
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
		return self.enrutador.calculo_de_ruta()
	
	def retangulo_delimitador(self):
		return self.shape().boundingRect()
	
	def shape(self):
		return self.calculo_de_ruta()
