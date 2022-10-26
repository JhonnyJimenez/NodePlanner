# Vista gráfica (Ventana principal).
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraficosdelaVistaVP(QGraphicsView):
	def __init__(self, escena, parent=None):
		super().__init__(parent)
		self.escena = escena
		
		self.initui()
		
		self.setScene(self.escena)
		
		self.FactorAcercamiento = 1.25
		self.ZoomClamp = True
		self.Zoom = 10
		self.NiveldeZoom = 1
		self.RangodeZoom = [0, 10]
		
	def initui(self):
		self.setRenderHints(
			QPainter.Antialiasing |
			QPainter.HighQualityAntialiasing |
			QPainter.TextAntialiasing |
			QPainter.SmoothPixmapTransform
		)
		
		self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

	def mousePressEvent(self, event):
		if event.button() == Qt.MiddleButton:
			self.middleMouseButtonPress(event)
		elif event.button() == Qt.LeftButton:
			self.leftMouseButtonPress(event)
		elif event.button() == Qt.RightButton:
			self.rightMouseButtonPress(event)
		else:
			super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MiddleButton:
			self.middleMouseButtonRelease(event)
		elif event.button() == Qt.LeftButton:
			self.leftMouseButtonRelease(event)
		elif event.button() == Qt.RightButton:
			self.rightMouseButtonRelease(event)
		else:
			super().mouseReleaseEvent(event)

	def middleMouseButtonPress(self, event):
		soltado_del_mouse = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
		super().mouseReleaseEvent(soltado_del_mouse)
		self.setDragMode(QGraphicsView.ScrollHandDrag)
		click_falso = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
		super().mousePressEvent(click_falso)

	def middleMouseButtonRelease(self, event):
		click_falso = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
		super().mouseReleaseEvent(click_falso)
		self.setDragMode(QGraphicsView.NoDrag)

	def leftMouseButtonPress(self, event):
		return super().mousePressEvent(event)

	def leftMouseButtonRelease(self, event):
		return super().mouseReleaseEvent(event)

	def rightMouseButtonPress(self, event):
		return super().mousePressEvent(event)

	def rightMouseButtonRelease(self, event):
		return super().mouseReleaseEvent(event)

	def wheelEvent(self, event):
		# Cálculo del factor de zoom.
		factoralejamiento = 1 / self.FactorAcercamiento
		
		# Cálculo del zoom
		if event.angleDelta().y() > 0:
			factor_de_zoom = self.FactorAcercamiento
			self.Zoom += self.NiveldeZoom
		else:
			factor_de_zoom = factoralejamiento
			self.Zoom -= self.NiveldeZoom
		
		clamped = False
		if self.Zoom < self.RangodeZoom[0]:
			self.Zoom, clamped = self.RangodeZoom[0], True
		if self.Zoom > self.RangodeZoom[1]:
			self.Zoom, clamped = self.RangodeZoom[1], True
		
		# Configuración de la escala de la escena.
		if not clamped or self.ZoomClamp is False:
			self.scale(factor_de_zoom, factor_de_zoom)
