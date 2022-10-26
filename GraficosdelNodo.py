from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsNode(QGraphicsItem):
	def __init__(self, Nodo, title='Node Graphics Item', parent=None):
		super().__init__(parent)
		
		self._ColorDelTitulo = Qt.white
		self._FuenteDelTitulo = QFont("Rounded Mgen+ 1c regular", 9)
		
		self.ancho_nodo = 180
		self.alto_nodo = 240
		self.redondez_nodo = 10.0
		self.altura_titulo_nodo = 24.0
		self._sangria = 4.0
		
		self._nodo_no_seleccionado = QPen(QColor("#7F000000"))
		self._nodo_seleccionado = QPen(QColor("#FFFFFFFF"))
		
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))
		self._relleno_fondo_nodo = QBrush(QColor("#E3303030"))
		
		self.titulo_del_nodo()
		self.nombre = title
		
		self.initui()
	
	def boundingRect(self):
		return QRectF(
			0,
			0,
			2 * self.redondez_nodo + self.ancho_nodo,
			2 * self.redondez_nodo + self.alto_nodo
		).normalized()
	
	def initui(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setFlag(QGraphicsItem.ItemIsMovable)
	
	def titulo_del_nodo(self):
		self.titulo_del_objeto = QGraphicsTextItem(self)
		self.titulo_del_objeto.setDefaultTextColor(self._ColorDelTitulo)
		self.titulo_del_objeto.setFont(self._FuenteDelTitulo)
		self.titulo_del_objeto.setPos(self._sangria, 0)
		self.titulo_del_objeto.setTextWidth(
			self.ancho_nodo
			- 2 * self._sangria
		)
	
	@property
	def nombre(self): return self.nombre
	
	@nombre.setter
	def nombre(self, valor):
		self._titulo = valor
		self.titulo_del_objeto.setPlainText(self._titulo)
	
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		
		# Título
		dibujado_del_titulo = QPainterPath()
		dibujado_del_titulo.setFillRule(Qt.WindingFill)
		dibujado_del_titulo.addRoundedRect(0, 0, self.ancho_nodo, self.altura_titulo_nodo, self.redondez_nodo, self.redondez_nodo)
		dibujado_del_titulo.addRect(0, self.altura_titulo_nodo - self.redondez_nodo, self.redondez_nodo, self.redondez_nodo)
		dibujado_del_titulo.addRect(self.ancho_nodo - self.redondez_nodo, self.altura_titulo_nodo - self.redondez_nodo, self.redondez_nodo, self.redondez_nodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_titulo_nodo)
		painter.drawPath(dibujado_del_titulo.simplified())
	
		# Contenido
		dibujado_del_contenido = QPainterPath()
		dibujado_del_contenido.setFillRule(Qt.WindingFill)
		dibujado_del_contenido.addRoundedRect(0, self.altura_titulo_nodo, self.ancho_nodo, self.alto_nodo - self.altura_titulo_nodo, self.redondez_nodo, self.redondez_nodo)
		dibujado_del_contenido.addRect(0, self.altura_titulo_nodo, self.redondez_nodo, self.redondez_nodo)
		dibujado_del_contenido.addRect(self.ancho_nodo - self.redondez_nodo, self.altura_titulo_nodo, self.redondez_nodo, self.redondez_nodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_fondo_nodo)
		painter.drawPath(dibujado_del_contenido.simplified())
		
		# Contorno
		dibujado_del_contorno = QPainterPath()
		dibujado_del_contorno.addRoundedRect(0, 0, self.ancho_nodo, self.alto_nodo, self.redondez_nodo, self.redondez_nodo)
		painter.setPen(self._nodo_no_seleccionado if not self.isSelected() else self._nodo_seleccionado)
		painter.setBrush(Qt.NoBrush)
		painter.drawPath(dibujado_del_contorno.simplified())
