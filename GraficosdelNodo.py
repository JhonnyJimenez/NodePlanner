from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosdelNodo(QGraphicsItem):
	def __init__(self, nodo, parent=None):
		super().__init__(parent)
		self.nodo = nodo
		self.contenido = self.nodo.contenido
		
		self._ColorDelTitulo = Qt.white
		self._FuenteDelTitulo = QFont("Rounded Mgen+ 1c regular", 9)
		
		self.anchoNodo = 180
		self.altoNodo = 240
		self.redondezNodo = 10.0
		self.alturaTituloNodo = 24.0
		self._sangria = 4.0
		
		self._nodo_no_seleccionado = QPen(QColor("#7F000000"))
		self._nodo_seleccionado = QPen(QColor("#FFFFFFFF"))
		
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))
		self._relleno_fondo_nodo = QBrush(QColor("#E3303030"))
		
		# init titulos
		self.titulo_del_nodo()
		self.nombre = self.nodo.titulo
		
		# init entradas y salidas
		self.initzocalos()
		
		# init contenido
		self.initContenido()
		
		self.initui()
		
	def mouseMoveEvent(self, evento):
		super().mouseMoveEvent(evento)
		self.nodo.actualizarconexiones()
	
	@property
	def nombre(self): return self.nombre
	
	@nombre.setter
	def nombre(self, valor):
		self._titulo = valor
		self.titulo_del_objeto.setPlainText(self._titulo)

	def boundingRect(self):
		return QRectF(
			0,
			0,
			self.anchoNodo,
			self.altoNodo
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
			self.anchoNodo
			- 2 * self._sangria
		)
	
	def initContenido(self):
		self.GraficosContenidoNodo = QGraphicsProxyWidget(self)
		self.contenido.setGeometry(int(self.redondezNodo), int(self.alturaTituloNodo + self.redondezNodo), self.anchoNodo - int((2 * self.redondezNodo)), self.altoNodo - int((2 * self.redondezNodo) + self.alturaTituloNodo))
		self.GraficosContenidoNodo.setWidget(self.contenido)
		
	def initzocalos(self):
		pass
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		
		# Título
		dibujado_del_titulo = QPainterPath()
		dibujado_del_titulo.setFillRule(Qt.WindingFill)
		dibujado_del_titulo.addRoundedRect(0, 0, self.anchoNodo, self.alturaTituloNodo, self.redondezNodo, self.redondezNodo)
		dibujado_del_titulo.addRect(0, self.alturaTituloNodo - self.redondezNodo, self.redondezNodo, self.redondezNodo)
		dibujado_del_titulo.addRect(self.anchoNodo - self.redondezNodo, self.alturaTituloNodo - self.redondezNodo, self.redondezNodo, self.redondezNodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_titulo_nodo)
		painter.drawPath(dibujado_del_titulo.simplified())
	
		# Contenido
		dibujado_del_contenido = QPainterPath()
		dibujado_del_contenido.setFillRule(Qt.WindingFill)
		dibujado_del_contenido.addRoundedRect(0, self.alturaTituloNodo, self.anchoNodo, self.altoNodo - self.alturaTituloNodo, self.redondezNodo, self.redondezNodo)
		dibujado_del_contenido.addRect(0, self.alturaTituloNodo, self.redondezNodo, self.redondezNodo)
		dibujado_del_contenido.addRect(self.anchoNodo - self.redondezNodo, self.alturaTituloNodo, self.redondezNodo, self.redondezNodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_fondo_nodo)
		painter.drawPath(dibujado_del_contenido.simplified())
		
		# Contorno
		dibujado_del_contorno = QPainterPath()
		dibujado_del_contorno.addRoundedRect(0, 0, self.anchoNodo, self.altoNodo, self.redondezNodo, self.redondezNodo)
		painter.setPen(self._nodo_no_seleccionado if not self.isSelected() else self._nodo_seleccionado)
		painter.setBrush(Qt.NoBrush)
		painter.drawPath(dibujado_del_contorno.simplified())
