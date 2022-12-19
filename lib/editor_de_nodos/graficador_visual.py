from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QMouseEvent, QWheelEvent
from PyQt6.QtCore import Qt, QEvent

BLOQUEO_AUTOMÁTICO_DE_ZOOM = True
NIVELES_DE_AJUSTE_AL_ZOOM = 1
ZOOM_GUIADO_POR_EL_MOUSE = False


class GraficadorVisual(QGraphicsView):
	def __init__(self, graficador_de_la_escena, elemento_superior = None):
		super().__init__(elemento_superior)

		self.graficador_de_la_escena = graficador_de_la_escena

		self.setScene(self.graficador_de_la_escena)

		self.factor_de_acercamiento = 1.25
		self.zoom_bloqueado = False
		self.nivel_de_zoom_actual = 10
		self.niveles_de_ajuste_al_zoom = 1
		self.nivel_de_zoom_mínimo_y_máximo = [0, 10]
		self.zoom_guiado_por_el_mouse = False

		self.interfaz()

	def interfaz(self):
		# QPainter.RenderHint.HighQualityAntialiasing —presente en PyQt5— ya no está presente en PyQt6.
		self.setRenderHints(
							QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing |
							QPainter.RenderHint.SmoothPixmapTransform
							)

		self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

		if self.zoom_guiado_por_el_mouse:
			self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

	def mousePressEvent(self, evento: QMouseEvent):
		if evento.button() == Qt.MouseButton.LeftButton:
			self.clic_izquierdo_presionado(evento)
		elif evento.button() == Qt.MouseButton.MiddleButton:
			self.clic_central_presionado(evento)
		elif evento.button() == Qt.MouseButton.RightButton:
			self.clic_derecho_presionado(evento)
		else:
			super().mousePressEvent(evento)

	def mouseReleaseEvent(self, evento: QMouseEvent):
		if evento.button() == Qt.MouseButton.LeftButton:
			self.clic_izquierdo_soltado(evento)
		elif evento.button() == Qt.MouseButton.MiddleButton:
			self.clic_central_soltado(evento)
		elif evento.button() == Qt.MouseButton.RightButton:
			self.clic_derecho_soltado(evento)
		else:
			super().mousePressEvent(evento)

	def clic_izquierdo_presionado(self, evento: QMouseEvent):
		return super().mousePressEvent(evento)

	def clic_izquierdo_soltado(self, evento: QMouseEvent):
		return super().mouseReleaseEvent(evento)

	def clic_central_presionado(self, evento: QMouseEvent):
		# localPos y screenPos en PyQt5 fueron reemplazados por las funciones usadas en el código en PyQt6.
		soltado_falso_del_mouse = QMouseEvent(
												QEvent.Type.MouseButtonRelease, evento.position(),
												evento.globalPosition(), Qt.MouseButton.LeftButton,
												Qt.MouseButton.NoButton, evento.modifiers()
												)
		super().mouseReleaseEvent(soltado_falso_del_mouse)
		self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
		evento_falso_del_mouse = QMouseEvent(
												evento.type(), evento.position(), evento.globalPosition(),
												Qt.MouseButton.LeftButton, evento.buttons() | Qt.MouseButton.LeftButton,
												evento.modifiers()
												)
		super().mousePressEvent(evento_falso_del_mouse)

	def clic_central_soltado(self, evento: QMouseEvent):
		evento_falso_del_mouse = QMouseEvent(
												evento.type(), evento.position(), evento.globalPosition(),
												Qt.MouseButton.LeftButton, evento.buttons() | Qt.MouseButton.LeftButton,
												evento.modifiers()
												)
		super().mousePressEvent(evento_falso_del_mouse)
		self.setDragMode(QGraphicsView.DragMode.NoDrag)

	def clic_derecho_presionado(self, evento: QMouseEvent):
		return super().mousePressEvent(evento)

	def clic_derecho_soltado(self, evento: QMouseEvent):
		return super().mouseReleaseEvent(evento)

	def wheelEvent(self, evento: QWheelEvent):
		factor_de_alejamiento = 1 / self.factor_de_acercamiento
		zoom_bloqueado = False

		# Cálculo del zoom.
		#   Esta función de angleDelta devuelve un valor dependiendo de la rotación de la rueda del mouse. Se usa «y»
		#   para ruedas verticales y «x» para ruedas horizontales.
		if evento.angleDelta().y() > 0:
			factor_de_zoom = self.factor_de_acercamiento
			self.nivel_de_zoom_actual += self.niveles_de_ajuste_al_zoom
		else:
			factor_de_zoom = factor_de_alejamiento
			self.nivel_de_zoom_actual -= self.niveles_de_ajuste_al_zoom

		#   El primer valor (con índice 0) de la lista self.nivel_de_zoom_mínimo_y_máximo es el nivel mínimo de zoom.
		if self.nivel_de_zoom_actual < self.nivel_de_zoom_mínimo_y_máximo[0]:
			self.nivel_de_zoom_actual = self.nivel_de_zoom_mínimo_y_máximo[0]
			zoom_bloqueado = True

		#   El segundo valor (con índice 1) de la lista self.nivel_de_zoom_mínimo_y_máximo es el nivel máximo de zoom.
		elif self.nivel_de_zoom_actual > self.nivel_de_zoom_mínimo_y_máximo[1]:
			self.nivel_de_zoom_actual = self.nivel_de_zoom_mínimo_y_máximo[1]
			zoom_bloqueado = True

		# Aplicado del zoom calculado.
		if not zoom_bloqueado or self.zoom_bloqueado is False:
			self.scale(factor_de_zoom, factor_de_zoom)
