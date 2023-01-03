from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColorConstants, QFont, QColor, QPen, QBrush, QPainterPath


class GraficosdelNodo(QGraphicsItem):
	def __init__(self, nodo, parent=None):
		super().__init__(parent)
		self.nodo = nodo
		
		# init de señales
		self.con_efecto_hover = False
		self._elemento_movido = False
		self._ultimo_estado_de_seleccion = False
		
		self.init_sizes()
		self.init_assets()
		self.init_ui()
	
	@property
	def contenido(self):
		return self.nodo.contenido if self.nodo else None
	
	@property
	def nombre(self):
		return self._titulo
	
	@nombre.setter
	def nombre(self, valor):
		self._titulo = valor
		self.título_del_objeto.setPlainText(self._titulo)
	
	def init_ui(self):
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
		self.setAcceptHoverEvents(True)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		
		# init titulos
		self.titulo_del_nodo()
		self.nombre = self.nodo.titulo
		
		self.init_contenido()
		
	def init_sizes(self):
		self.redondez_del_nodo = 10.0
		self.márgen = 10.0
		self.altura_del_título = 24.0
		self.sangría_del_título = 4.0
		self.sangría_vertical_del_título = 4.0
		self.anchura_del_nodo = 180
		self.altura_del_nodo = 240

	def init_assets(self):
		self._color_del_título = QColorConstants.White
		self._fuente_del_título = QFont("Ubuntu", 9)
		
		self._color = QColor("#7F000000")
		self._color_seleccionado = QColor("#FFFFA637")
		self._color_hovered = QColor("#FF37A6FF")
		
		self._lápiz_por_defecto = QPen(self._color)
		self._lápiz_por_defecto.setWidthF(2.0)
		self._lápiz_para_selección = QPen(self._color_seleccionado)
		self._lápiz_para_selección.setWidthF(2.0)
		self._efecto_hover = QPen(self._color_hovered)
		self._efecto_hover.setWidthF(3.0)
		
		self._relleno_del_título = QBrush(QColor("#FF313131"))
		self._relleno_del_fondo = QBrush(QColor("#E3212121"))
	
	def seleccionado(self):
		self.nodo.escena.graficador_de_la_escena.objeto_seleccionado.emit()
		
	def hacer_selección(self, nuevo_estado=True):
		self.setSelected(nuevo_estado)
		self._ultimo_estado_de_seleccion = nuevo_estado
		if nuevo_estado: self.seleccionado()
		
	def mouseMoveEvent(self, evento):
		super().mouseMoveEvent(evento)

		# ¡Optimízame! ¡Solo actualizo los nodos seleccionados!
		for nodo in self.scene().escena.nodos:
			if nodo.Nodograficas.isSelected():
				nodo.actualizar_conexiones()
		self._elemento_movido = True
		
	def mouseReleaseEvent(self, evento):
		super().mouseReleaseEvent(evento)
		
		# Control para cuando se mueve el nodo.
		if self._elemento_movido:
			self._elemento_movido = False
			self.nodo.escena.historial.almacenar_historial("Nodo movido", set_modified =True)
			
			self.nodo.escena.restaurar_último_estado_de_selección()
			# ToDo: Esta función ↓↓↓ hace que el historial almacene el cambio de seleccion que de hecho, se quiere evitar
			#  al mover el nodo. Lo desactivé hasta hallar la solución en futuros tutoriales o para solucionarlo yo
			#  mismo. El punto es que la señal que emite la variable en GraficadordelaEscena activa el almacenamiento
			#  del historia por alguna razón.
			# self.hacer_selección()
			
			# Necesitamos almacenar el último estado de selección porque mover nodos también los selecciona.
			self.nodo.escena._ultimos_objetos_seleccionados = self.nodo.escena.objetos_seleccionados()
			
			# Ahora queremos saltarnos el almacenamiento en el historial de la selección.
			return
			
		# Control para cuando se selecciona el nodo.
		if self._ultimo_estado_de_seleccion != self.isSelected() or self.nodo.escena._ultimos_objetos_seleccionados != self.nodo.escena.objetos_seleccionados():
			self.nodo.escena.restaurar_último_estado_de_selección()
			self._ultimo_estado_de_seleccion = self.isSelected()
			self.seleccionado()
			
	def mouseDoubleClickEvent(self, event):
		self.nodo.doble_cliqueo(event)
	
	def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.con_efecto_hover = True
		self.update()
	
	def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
		self.con_efecto_hover = False
		self.update()

	def boundingRect(self):
		return QRectF(
			0,
			0,
			self.anchura_del_nodo,
			self.altura_del_nodo
		).normalized()
	
	def titulo_del_nodo(self):
		self.título_del_objeto = QGraphicsTextItem(self)
		self.título_del_objeto.nodo = self.nodo
		self.título_del_objeto.setDefaultTextColor(self._color_del_título)
		self.título_del_objeto.setFont(self._fuente_del_título)
		self.título_del_objeto.setPos(self.sangría_del_título, 0)
		self.título_del_objeto.setTextWidth(
			self.anchura_del_nodo
			- 2 * self.sangría_del_título
		)
	
	def init_contenido(self):
		if self.contenido is not None:
			self.contenido.setGeometry(int(self.márgen), int(self.altura_del_título + self.márgen),
			                           self.anchura_del_nodo - int(2 * self.márgen), self.altura_del_nodo - int((2 * self.márgen) + self.altura_del_título))
			
		# Obtener el QGraphicsProxy cuando está insertado en los gráficos de la escena.
		self.GraficosContenidoNodo = self.nodo.escena.graficador_de_la_escena.addWidget(self.contenido)
		self.GraficosContenidoNodo.setParentItem(self)

	def paint(self, dibujante, estilo: QStyleOptionGraphicsItem, widget=None):
		# Título
		etiqueta_del_título = QPainterPath()
		etiqueta_del_título.setFillRule(Qt.FillRule.WindingFill)
		etiqueta_del_título.addRoundedRect(
				0, 0, self.anchura_del_nodo, self.altura_del_título,
				self.redondez_del_nodo, self.redondez_del_nodo
				)
		etiqueta_del_título.addRect(
				0, self.altura_del_título - self.redondez_del_nodo, self.anchura_del_nodo,
				self.redondez_del_nodo
				)
		dibujante.setPen(Qt.PenStyle.NoPen)
		dibujante.setBrush(self._relleno_del_título)
		dibujante.drawPath(etiqueta_del_título.simplified())
	
		# Relleno
		relleno = QPainterPath()
		relleno.setFillRule(Qt.FillRule.WindingFill)
		relleno.addRoundedRect(
				0, self.altura_del_título, self.anchura_del_nodo,
				self.altura_del_nodo - self.altura_del_título, self.redondez_del_nodo,
				self.redondez_del_nodo
				)
		relleno.addRect(0, self.altura_del_título, self.anchura_del_nodo, self.redondez_del_nodo)
		dibujante.setPen(Qt.PenStyle.NoPen)
		dibujante.setBrush(self._relleno_del_fondo)
		dibujante.drawPath(relleno.simplified())
		
		# Contorno
		contorno = QPainterPath()
		contorno.addRoundedRect(
				-1, -1, self.anchura_del_nodo + 2, self.altura_del_nodo + 2, self.redondez_del_nodo,
				self.redondez_del_nodo
				)
		dibujante.setBrush(Qt.BrushStyle.NoBrush)
		if self.con_efecto_hover:
			dibujante.setPen(self._efecto_hover)
			dibujante.drawPath(contorno.simplified())
			dibujante.setPen(self._lápiz_por_defecto)
			dibujante.drawPath(contorno.simplified())
		else:
			dibujante.setPen(self._lápiz_por_defecto if not self.isSelected() else self._lápiz_para_selección)
			dibujante.drawPath(contorno.simplified())
