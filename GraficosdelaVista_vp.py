# Vista gráfica (Ventana principal).
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from GraficosDeZocalos import GraficosDeZocalos
from GraficosdeConexion import GraficosdeConexion
from Conexiones import Conexion, bezier


MODO_NORMAL = 1
MODO_DIBUJO = 2

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True


class GraficosdelaVistaVP(QGraphicsView):
	def __init__(self, escena, parent=None):
		super().__init__(parent)
		self.escena = escena
		
		self.initui()
		
		self.setScene(self.escena)
		
		self.modo = MODO_NORMAL
		
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
		# Obtener el objeto donde se cliqueó.
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		# Almacenamiento de la posición del último click izquierdo.
		self.ultimo_clic = self.mapToScene(event.pos())
		
		# Lógica.
		if type(objeto) is GraficosDeZocalos:
			if self.modo == MODO_NORMAL:
				self.modo = MODO_DIBUJO
				self.ComenzarDibujadoConexion(objeto)
				return

		if self.modo == MODO_DIBUJO:
			res = self.FinalizarDibujadoConexion(objeto)
			if res: return
		
		super().mousePressEvent(event)
	
	def leftMouseButtonRelease(self, event):
		# Obtener el objeto sobre el que se suelta el clic.
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		# Lógica.
		if self.modo == MODO_DIBUJO:
			if self.DistanciaEntreClicksEsCero(event):
				res = self.FinalizarDibujadoConexion(objeto)
				if res: return
		
		super().mouseReleaseEvent(event)

	def rightMouseButtonPress(self, event):
		super().mousePressEvent(event)
		
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		if DEBUG:
			if isinstance(objeto, GraficosdeConexion): print('RMB DEBUG:', 'La', objeto.linea, 'conecta',
															 'el', objeto.linea.zocalo_origen, 'con el', objeto.linea.zocalo_final)
			if type(objeto) is GraficosDeZocalos: print('RMB DEBUG:', 'El', objeto.zocalo, 'tiene la', objeto.zocalo.conexion)
			
			if objeto is None:
				print('Escena:')
				print('   Nodo:')
				for nodo in self.escena.escena.Nodos: print('     ', nodo)
				print('   Conexión:')
				for conexion in self.escena.escena.Conexiones: print('     ', conexion)

	def rightMouseButtonRelease(self, event):
		super().mouseReleaseEvent(event)
		
	def mouseMoveEvent(self, event):
		if self.modo == MODO_DIBUJO:
			pos = self.mapToScene(event.pos())
			self.dibujarconexion.GraficosDeConexion.punto_destino(pos.x(), pos.y())
			self.dibujarconexion.GraficosDeConexion.update()
		
		super().mouseMoveEvent(event)
		
	def ConseguirObjetoAlCliquear(self, event):
		# Devuelve el objeto sobre el que se ha clicado.
		posicion = event.pos()
		objeto = self.itemAt(posicion)
		return objeto
	
	def ComenzarDibujadoConexion(self, objeto):
		if DEBUG: print('Vista: CDibujadoConexion - Comienza a dibujar la conexión.')
		if DEBUG: print('Vista: CDibujadoConexion -  Zócalo inicial asignado a:', objeto.zocalo)
		self.conexion_anterior = objeto.zocalo.conexion
		self.ultimo_zocalo_inicial = objeto.zocalo
		self.dibujarconexion = Conexion(self.escena.escena, objeto.zocalo, None, bezier)
		if DEBUG: print('Vista: CDibujadoConexion - Dibujado:', self.dibujarconexion)
	
	def FinalizarDibujadoConexion(self, objeto):
		# Devuelve verdadero si se salta el resto del código
		self.modo = MODO_NORMAL
		
		if type(objeto) is GraficosDeZocalos:
			if DEBUG: print('Vista: FDibujadoConexion -  conexion anterior', self.conexion_anterior)
			if objeto.zocalo.tieneconexiones():
				objeto.zocalo.conexion.quitar()
			if DEBUG: print('Vista: FDibujadoConexion -  Zócalo final asignado', objeto.zocalo)
			if self.conexion_anterior is not None: self.conexion_anterior.quitar()
			if DEBUG: print('Vista: FDibujadoConexion - Conexion anterior eliminada')
			self.dibujarconexion.zocalo_origen = self.ultimo_zocalo_inicial
			self.dibujarconexion.zocalo_final = objeto.zocalo
			self.dibujarconexion.zocalo_origen.conexion_conectada(self.dibujarconexion)
			self.dibujarconexion.zocalo_final.conexion_conectada(self.dibujarconexion)
			if DEBUG: print('Vista: FDibujadoConexion -  Zócalo inicial y final reasignados')
			self.dibujarconexion.posiciones_actualizadas()
			return True
		
		if DEBUG: print('Vista: FDibujadoConexion - Termina de dibujar la conexión.')
		self.dibujarconexion.quitar()
		self.dibujarconexion = None
		if DEBUG: print('Vista: FDibujadoConexion - Sobre configurar el zocalo al anterior:', self.conexion_anterior)
		if self.conexion_anterior is not None:
			self.conexion_anterior.zocalo_origen.conexion = self.conexion_anterior
		if DEBUG: print('Vista: FDibujadoConexion - Todo bien')
		
		return False
	
	def DistanciaEntreClicksEsCero(self, event):
		# Medidas si nosotros estamos muy lejos de la posición del último clic dado.
		nuevo_ultimo_clic = self.mapToScene(event.pos())
		dist_de_clics = nuevo_ultimo_clic - self.ultimo_clic
		edge_drag_threshold = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
		return (dist_de_clics.x() * dist_de_clics.x() + dist_de_clics.y() * dist_de_clics.y()) > edge_drag_threshold

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
