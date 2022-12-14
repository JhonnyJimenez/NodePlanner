from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosdelNodo(QGraphicsItem):
	def __init__(self, nodo, parent=None):
		super().__init__(parent)
		self.nodo = nodo
		
		# init de señales
		self.hovered = False
		self._elemento_movido = False
		self._ultimo_estado_de_seleccion = False
		
		self.initSizes()
		self.initAssets()
		self.initUI()
	
	@property
	def contenido(self):
		return self.nodo.contenido if self.nodo else None
	
	@property
	def nombre(self):
		return self._titulo
	
	@nombre.setter
	def nombre(self, valor):
		self._titulo = valor
		self.titulo_del_objeto.setPlainText(self._titulo)
	
	def initUI(self):
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setAcceptHoverEvents(True)
		self.setFlag(QGraphicsItem.ItemIsMovable)
		
		# init titulos
		self.titulo_del_nodo()
		self.nombre = self.nodo.titulo
		
		self.initContenido()
		
	def initSizes(self):
		self.anchoNodo = 180
		self.altoNodo = 240
		self.redondezdelaOrilladelNodo = 10.0
		self.sangria_de_la_orilla = 10.0
		self.alturaTituloNodo = 24.0
		self.sangria_del_titulo = 4.0
		self.sangria_vertical_del_titulo = 4.0
		
	def initAssets(self):
		self._ColorDelTitulo = Qt.white
		self._FuenteDelTitulo = QFont("Rounded Mgen+ 1c regular", 9)
		
		self._color = QColor("#7F000000")
		self._color_seleccionado = QColor("#FFFFFFFF")
		self._color_hovered = QColor("#FF37A6FF")
		
		self._pen_default = QPen(self._color)
		self._pen_default.setWidthF(2.0)
		self._pen_seleccionado = QPen(self._color_seleccionado)
		self._pen_seleccionado.setWidthF(2.0)
		self._pen_hovered = QPen(self._color_hovered)
		self._pen_hovered.setWidthF(3.0)
		
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))
		self._relleno_fondo_nodo = QBrush(QColor("#E3303030"))
	
	def seleccionado(self):
		self.nodo.escena.GraficosEsc.objetoSeleccionado.emit()
		
	def hacerSeleccion(self, nuevo_estado=True):
		self.setSelected(nuevo_estado)
		self._ultimo_estado_de_seleccion = nuevo_estado
		if nuevo_estado: self.seleccionado()
		
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
			self.hacerSeleccion()
			
			# Necesitamos almacenar el último estado de selección porque mover nodos también los selecciona.
			self.nodo.escena._ultimos_objetos_seleccionados = self.nodo.escena.objetosSeleccionados()
			
			# Ahora queremos saltarnos la selección de almacenamiento.
			return
			
		# Control para cuando se selecciona el nodo.
		if self._ultimo_estado_de_seleccion != self.isSelected() or self.nodo.escena._ultimos_objetos_seleccionados != self.nodo.escena.objetosSeleccionados():
			self.nodo.escena.restaurarUltimoEstadodeSeleccion()
			self._ultimo_estado_de_seleccion = self.isSelected()
			self.seleccionado()
			
	def mouseDoubleClickEvent(self, event):
		self.nodo.DobleCliqueo(event)
	
	def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.hovered = True
		self.update()
	
	def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.hovered = False
		self.update()

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
		self.titulo_del_objeto.setPos(self.sangria_del_titulo, 0)
		self.titulo_del_objeto.setTextWidth(
			self.anchoNodo
			- 2 * self.sangria_del_titulo
		)
	
	def initContenido(self):
		if self.contenido is not None:
			self.contenido.setGeometry(int(self.sangria_de_la_orilla), int(self.alturaTituloNodo + self.sangria_de_la_orilla),
									   self.anchoNodo - int((2 * self.sangria_de_la_orilla)), self.altoNodo - int((2 * self.sangria_de_la_orilla) + self.alturaTituloNodo))
			
		# Obtener el QGraphicsProxy cuando está insertado en los gráficos de la escena.
		self.GraficosContenidoNodo = self.nodo.escena.GraficosEsc.addWidget(self.contenido)
		self.GraficosContenidoNodo.setParentItem(self)

	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		
		# Título
		dibujado_del_titulo = QPainterPath()
		dibujado_del_titulo.setFillRule(Qt.WindingFill)
		dibujado_del_titulo.addRoundedRect(0, 0, self.anchoNodo, self.alturaTituloNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		dibujado_del_titulo.addRect(0, self.alturaTituloNodo - self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		dibujado_del_titulo.addRect(self.anchoNodo - self.redondezdelaOrilladelNodo, self.alturaTituloNodo - self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_titulo_nodo)
		painter.drawPath(dibujado_del_titulo.simplified())
	
		# Contenido
		dibujado_del_contenido = QPainterPath()
		dibujado_del_contenido.setFillRule(Qt.WindingFill)
		dibujado_del_contenido.addRoundedRect(0, self.alturaTituloNodo, self.anchoNodo, self.altoNodo - self.alturaTituloNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		dibujado_del_contenido.addRect(0, self.alturaTituloNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		dibujado_del_contenido.addRect(self.anchoNodo - self.redondezdelaOrilladelNodo, self.alturaTituloNodo, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self._relleno_fondo_nodo)
		painter.drawPath(dibujado_del_contenido.simplified())
		
		# Contorno
		dibujado_del_contorno = QPainterPath()
		dibujado_del_contorno.addRoundedRect(-1, -1, self.anchoNodo + 2, self.altoNodo + 2, self.redondezdelaOrilladelNodo, self.redondezdelaOrilladelNodo)
		painter.setBrush(Qt.NoBrush)
		if self.hovered:
			painter.setPen(self._pen_hovered)
			painter.drawPath(dibujado_del_contorno.simplified())
			painter.setPen(self._pen_default)
			painter.drawPath(dibujado_del_contorno.simplified())
		else:
			painter.setPen(self._pen_default if not self.isSelected() else self._pen_seleccionado)
			painter.drawPath(dibujado_del_contorno.simplified())
