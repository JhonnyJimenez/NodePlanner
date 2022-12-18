from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from lib.nodeeditor.GraficosDeZocalos import GraficosDeZocalos
from lib.nodeeditor.GraficosdeConexion import GraficosdeConexion
from lib.nodeeditor.Dibujado_de_conexion import DibujadodeConexion
from lib.nodeeditor.GraficosdeCortado import Recortado
from lib.nodeeditor.Utilidades import dump_exception

MODO_NORMAL = 1
MODO_DIBUJO = 2
MODO_CORTE = 3
MODO_REDIRECCION = 4

# Distancia para activar el modo dibujo al cliquear en un zócalo.
EDGE_DRAG_START_THRESHOLD = 50

DEBUG = False
DEBUG_CLIC_CENTRAL = True
DEBUG_CLIC_CENTRAL_ULTIMAS_SELECCIONES = False


class GraficosdelaVistaVP(QGraphicsView):
	cambioPosEscena = pyqtSignal(int, int)
	
	def __init__(self, escena, parent=None):
		super().__init__(parent)
		self.escena = escena
		
		self.initui()
		
		self.setScene(self.escena)
		
		self.modo = MODO_NORMAL
		self.eventoedicion = False
		self.rubberBandDraggingRectangle = False
		
		# Dibujado de conexiones.
		self.dibujado = DibujadodeConexion(self)
		
		# Cutline
		self.linea_de_recorte = Recortado()
		self.escena.addItem(self.linea_de_recorte)
		
		self.ultima_posicion_del_mouse = QPoint(0, 0)
		self.FactorAcercamiento = 1.25
		self.ZoomClamp = True
		self.Zoom = 10
		self.NiveldeZoom = 1
		self.RangodeZoom = [0, 10]
		
		# Listeners
		self._drag_enter_listeners = []
		self._drop_listeners = []
		
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
		self.setDragMode(QGraphicsView.RubberBandDrag)
		
		# Activado de arrastre y soltura de objetos.
		self.setAcceptDrops(True)
		
	def reiniciarModo(self):
		self.modo = MODO_NORMAL
		
	def dragEnterEvent(self, event):
		for callback in self._drag_enter_listeners: callback(event)
	
	def dropEvent(self, event):
		for callback in self._drop_listeners: callback(event)
		
	def agregarDragEnterListener(self, callback):
		self._drag_enter_listeners.append(callback)
	
	def agregarDropListener(self, callback):
		self._drop_listeners.append(callback)

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
		objeto = self.ConseguirObjetoAlCliquear(event)

		# DEBUG print.
		if DEBUG_CLIC_CENTRAL:
			if isinstance(objeto, GraficosdeConexion):
				print('MMB DEBUG: La', objeto.linea, "\n\t", objeto.linea.GraficosdeConexion if objeto.linea.GraficosdeConexion is not None else None)
				return
			
			if isinstance(objeto, GraficosDeZocalos):
				print("MMB DEBUG:", objeto.zocalo, "Tipo_de_zocalo:", objeto.zocalo.tipo_zocalo,
					  "¿tiene conexiones?:", "No" if objeto.zocalo.Zocaloconexiones == [] else "")
				if objeto.zocalo.Zocaloconexiones:
					for conexion in objeto.zocalo.Zocaloconexiones: print("\t", conexion)
				return
				
			
		if DEBUG_CLIC_CENTRAL and objeto is None:
			print('Escena:')
			print('   Nodo:')
			for nodo in self.escena.escena.Nodos: print("\t", nodo)
			print('   Conexión:')
			# for conexion in self.escena.escena.Conexiones: print("\t", conexion, "\n\t\tConexion:", conexion.GraficosDeConexion if conexion.GraficosDeConexion is not None else None)
			for conexion in self.escena.escena.Conexiones: print("\t", conexion)
			
			if event.modifiers() & Qt.CTRL:
				print("  Objetos graficos en la escena gráfica:")
				for objeto in self.escena.items():
					print('    ', objeto)
		
		if DEBUG_CLIC_CENTRAL_ULTIMAS_SELECCIONES and event.modifiers() & Qt.SHIFT:
			print("Escena _ultimos_objetos_seleccionados:", self.escena.escena._ultimos_objetos_seleccionados)
			return
		
		# Eventos falsos para activar el desplazamiento por la ventana.
		soltado_del_mouse = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
		super().mouseReleaseEvent(soltado_del_mouse)
		self.setDragMode(QGraphicsView.ScrollHandDrag)
		click_falso = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
		super().mousePressEvent(click_falso)

	def middleMouseButtonRelease(self, event):
		click_falso = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
		super().mouseReleaseEvent(click_falso)
		self.setDragMode(QGraphicsView.RubberBandDrag)

	def leftMouseButtonPress(self, event):
		# Obtener el objeto donde se cliqueó.
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		# Almacenamiento de la posición del último click izquierdo.
		self.ultimo_clic = self.mapToScene(event.pos())
		
		#if DEBUG: print(self.debug_modifiers(event),'click izquierdo presionando', objeto)
		
		# Lógica.
		if hasattr(objeto, "nodo") or isinstance(objeto, GraficosdeConexion) or objeto is None:
			if event.modifiers() & Qt.ShiftModifier:
				event.ignore()
				evento_falso = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
										   Qt.LeftButton, event.buttons() | Qt.LeftButton,
										   event.modifiers() | Qt.ControlModifier)
				super().mousePressEvent(evento_falso)
				return
			
				
		if isinstance(objeto, GraficosDeZocalos):
			if self.modo == MODO_NORMAL:
				self.modo = MODO_DIBUJO
				self.dibujado.ComenzarDibujadoConexion(objeto)
				return

		if self.modo == MODO_DIBUJO:
			res = self.dibujado.FinalizarDibujadoConexion(objeto)
			if res: return
			
		if objeto is None:
			if event.modifiers() & Qt.ControlModifier:
				self.modo = MODO_CORTE
				evento_falso = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
										   Qt.LeftButton, Qt.NoButton, event.modifiers())
				super().mouseReleaseEvent(evento_falso)
				QApplication.setOverrideCursor(Qt.CrossCursor)
				return
			else:
				self.rubberBandDraggingRectangle = True
		
		super().mousePressEvent(event)
	
	def leftMouseButtonRelease(self, event):
		# Obtener el objeto sobre el que se suelta el clic.
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		try:
			# Lógica.
			if hasattr(objeto, "nodo") or isinstance(objeto, GraficosdeConexion) or objeto is None:
				if event.modifiers() & Qt.ShiftModifier:
					event.ignore()
					evento_falso = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
											   Qt.LeftButton, Qt.NoButton,
											   event.modifiers() | Qt.ControlModifier)
					super().mouseReleaseEvent(evento_falso)
					return
				
			if self.modo == MODO_DIBUJO:
				if self.DistanciaEntreClicksEsCero(event):
					res = self.dibujado.FinalizarDibujadoConexion(objeto)
					if res: return
					
			if self.modo == MODO_CORTE:
				self.ConexionesCortadas()
				self.linea_de_recorte.linea_puntos = []
				self.linea_de_recorte.update()
				QApplication.setOverrideCursor(Qt.ArrowCursor)
				self.modo = MODO_NORMAL
				return
			
			if self.rubberBandDraggingRectangle:
				self.rubberBandDraggingRectangle = False
				objetos_seleccionados_actualmente = self.escena.selectedItems()
				
				if objetos_seleccionados_actualmente != self.escena.escena._ultimos_objetos_seleccionados:
					if objetos_seleccionados_actualmente == []:
						self.escena.objetosNoSeleccionados.emit()
					else:
						self.escena.objetoSeleccionado.emit()
					self.escena.escena._ultimos_objetos_seleccionados = objetos_seleccionados_actualmente
				
				return
			
			# De otro modo deseleccionar todos los objetos.
			if objeto is None:
				self.escena.objetosNoSeleccionados.emit()
		except: dump_exception()
			
		super().mouseReleaseEvent(event)

	def rightMouseButtonPress(self, event):
		super().mousePressEvent(event)

	def rightMouseButtonRelease(self, event):
		super().mouseReleaseEvent(event)
		
	def mouseMoveEvent(self, event):
		pos_esc = self.mapToScene(event.pos())
		
		if self.modo == MODO_DIBUJO:
			self.dibujado.actualizarDestino(pos_esc.x(), pos_esc.y())
			
		if self.modo == MODO_CORTE and self.linea_de_recorte is not None:
			self.linea_de_recorte.linea_puntos.append(pos_esc)
			self.linea_de_recorte.update()
		
		self.ultima_posicion_mouse_escena = pos_esc
		
		self.cambioPosEscena.emit(int(pos_esc.x()), int(pos_esc.y()))
		
		super().mouseMoveEvent(event)
		
		
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Delete:
			if not self.eventoedicion:
				self.eliminarSeleccionado()
			else:
				super().keyPressEvent(event)
		# elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
		#	self.escena.escena.guardarArchivo("graph.json")
		# elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
		#	self.escena.escena.abrirArchivo("graph.json")
		# elif event.key() == Qt.Key_1:
		#	self.escena.escena.historial.almacenarHistorial("Item A")
		# elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
		#	self.escena.escena.historial.deshacer()
		# elif event.key() == Qt.Key_Y and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
		#	self.escena.escena.historial.rehacer()
		#elif event.key() == Qt.Key_H:
		#	print("Historial:    len(%d)" % len(self.escena.escena.historial.listado_historial),
		#		  "    -- posicion actual", self.escena.escena.historial.pos_act_historial)
		#	ix = 0
		#	for objeto in self.escena.escena.historial.listado_historial:
		#		print("#", ix, "--", objeto['desc'])
		#		ix += 1
		#else:
		super().keyPressEvent(event)


	def ConexionesCortadas(self):
		for ix in range(len(self.linea_de_recorte.linea_puntos) - 1):
			p1 = self.linea_de_recorte.linea_puntos[ix]
			p2 = self.linea_de_recorte.linea_puntos[ix + 1]
		
			for conexion in self.escena.escena.Conexiones.copy():
				if conexion.GraficosDeConexion.cruzadocon(p1, p2):
					conexion.quitar()
		self.escena.escena.historial.almacenarHistorial("Conexión cortada borrada", setModified=True)
			
	def eliminarSeleccionado(self):
		for objeto in self.escena.selectedItems():
			if isinstance(objeto, GraficosdeConexion):
				objeto.linea.quitar()
			elif hasattr(objeto, "nodo"):
				objeto.nodo.quitar()
		self.escena.escena.historial.almacenarHistorial("Objeto seleccionado borrado", setModified=True)
		
	def debug_modifiers(self, event):
		out = ""
		if event.modifiers() & Qt.ShiftModifier: out += "Shift"
		if event.modifiers() & Qt.ControlModifier: out += "Ctrl"
		if event.modifiers() & Qt.AltModifier: out += "Alt"
		return out
		
	def ConseguirObjetoAlCliquear(self, event):
		# Devuelve el objeto sobre el que se ha clicado.
		posicion = event.pos()
		objeto = self.itemAt(posicion)
		return objeto
	
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
