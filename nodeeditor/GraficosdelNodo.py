from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosdelNodo(QGraphicsItem):
	def __init__(self, nodo, parent=None):
		super().__init__(parent)
		self.nodo = nodo
		self.contenido = self.nodo.contenido
		
		# init de señales
		self._elemento_movido = False
		self._ultimo_estado_de_seleccion = False
		
		self.initSizes()
		self.initAssets()
		self.initUI()
	
	def initUI(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setFlag(QGraphicsItem.ItemIsMovable)
		
		# init titulos
		self.titulo_del_nodo()
		self.nombre = self.nodo.titulo
		
		self.initzocalos()
		self.initContenido()
		
	def initSizes(self):
		self.anchoNodo = 180
		self.altoNodo = 240
		self.redondezNodo = 10.0
		self.alturaTituloNodo = 24.0
		self._sangria = 4.0
		
	def initAssets(self):
		self._ColorDelTitulo = Qt.white
		self._FuenteDelTitulo = QFont("Rounded Mgen+ 1c regular", 9)
		
		self._nodo_no_seleccionado = QPen(QColor("#7F000000"))
		self._nodo_seleccionado = QPen(QColor("#FFFFFFFF"))
		
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))
		self._relleno_fondo_nodo = QBrush(QColor("#E3303030"))
	
	def seleccionado(self):
		self.nodo.escena.GraficosEsc.objetoSeleccionado.emit()
		
	def mouseMoveEvent(self, evento):
		super().mouseMoveEvent(evento)

		# ¡Optimízame! ¡Solo actualizo los nodos seleccionados!
		for nodo in self.scene().escena.Nodos:
			if nodo.Nodograficas.isSelected():
				nodo.actualizarconexiones()
		self._elemento_movido = True
		
	def mouseReleaseEvent(self, evento):
		super().mouseReleaseEvent(evento)
		
		# Control para cuando se mueve el nodo.
		if self._elemento_movido:
			self._elemento_movido = False
			self.nodo.escena.historial.almacenarHistorial("Nodo movido", setModified=True)
			
			self.nodo.escena.restaurarUltimoEstadodeSeleccion()
			self._ultimo_estado_de_seleccion = True
			
			# Necesitamos almacenar el último estado de selección porque mover nodos también los selecciona.
			self.nodo.escena._ultimos_objetos_seleccionados = self.nodo.escena.objetosSeleccionados()
			
			# Ahora queremos saltarnos la selección de almacenamiento.
			return
			
		# Control para cuando se selecciona el nodo.
		if self._ultimo_estado_de_seleccion != self.isSelected() or self.nodo.escena._ultimos_objetos_seleccionados != self.nodo.escena.objetosSeleccionados():
			self.nodo.escena.restaurarUltimoEstadodeSeleccion()
			self._ultimo_estado_de_seleccion = self.isSelected()
			self.seleccionado()
	
	@property
	def nombre(self): return self._titulo
	
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
	
	def titulo_del_nodo(self):
		self.titulo_del_objeto = QGraphicsTextItem(self)
		self.titulo_del_objeto.nodo = self.nodo
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
