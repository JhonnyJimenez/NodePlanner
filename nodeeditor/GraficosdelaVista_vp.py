# Vista gráfica (Ventana principal).
from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from nodeeditor.GraficosDeZocalos import GraficosDeZocalos
from nodeeditor.GraficosdeConexion import GraficosdeConexion
from nodeeditor.Conexiones import Conexion, bezier
from nodeeditor.GraficosdeCortado import Recortado

MODO_NORMAL = 1
MODO_DIBUJO = 2
MODO_CORTE = 3

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True


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
		
		self.FactorAcercamiento = 1.25
		self.ZoomClamp = True
		self.Zoom = 10
		self.NiveldeZoom = 1
		self.RangodeZoom = [0, 10]
		
		# outline
		self.linea_de_recorte = Recortado()
		self.escena.addItem(self.linea_de_recorte)
		
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
		self.setDragMode(QGraphicsView.RubberBandDrag)

	def leftMouseButtonPress(self, event):
		# Obtener el objeto donde se cliqueó.
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		# Almacenamiento de la posición del último click izquierdo.
		self.ultimo_clic = self.mapToScene(event.pos())
		
		#if DEBUG:
		#	if self.debug_modifiers(event) == "":
		#		print('Click izquierdo presionando', objeto)
		#	else:
		#		print(self.debug_modifiers(event),'click izquierdo presionando', objeto)
		
		# Lógica.
		if hasattr(objeto, "nodo") or isinstance(objeto, GraficosdeConexion) or objeto is None:
			if event.modifiers() & Qt.ShiftModifier:
				event.ignore()
				evento_falso = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
										   Qt.LeftButton, event.buttons() | Qt.LeftButton,
										   event.modifiers() | Qt.ControlModifier)
				super().mousePressEvent(evento_falso)
				return
			
				
		if type(objeto) is GraficosDeZocalos:
			if self.modo == MODO_NORMAL:
				self.modo = MODO_DIBUJO
				self.ComenzarDibujadoConexion(objeto)
				return

		if self.modo == MODO_DIBUJO:
			res = self.FinalizarDibujadoConexion(objeto)
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
				res = self.FinalizarDibujadoConexion(objeto)
				if res: return
				
		if self.modo == MODO_CORTE:
			self.ConexionesCortadas()
			self.linea_de_recorte.linea_puntos = []
			self.linea_de_recorte.update()
			QApplication.setOverrideCursor(Qt.ArrowCursor)
			self.modo = MODO_NORMAL
			return
		
		# if self.dragMode() == QGraphicsView.RubberBandDrag:
		if self.rubberBandDraggingRectangle:
			self.escena.escena.historial.almacenarHistorial("Selection changed")
			self.rubberBandDraggingRectangle = False
		
		super().mouseReleaseEvent(event)

	def rightMouseButtonPress(self, event):
		super().mousePressEvent(event)
		
		objeto = self.ConseguirObjetoAlCliquear(event)
		
		if DEBUG:
			if isinstance(objeto, GraficosdeConexion): print('RMB DEBUG:', 'La', objeto.linea, 'conecta',
															 'el', objeto.linea.zocalo_origen, 'con el', objeto.linea.zocalo_final)
			if type(objeto) is GraficosDeZocalos: print('RMB DEBUG:', 'El', objeto.zocalo, 'tiene las', objeto.zocalo.Zocaloconexiones)
			
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
			self.dibujar_conexion.GraficosDeConexion.punto_destino(pos.x(), pos.y())
			self.dibujar_conexion.GraficosDeConexion.update()
			
		if self.modo == MODO_CORTE:
			pos = self.mapToScene(event.pos())
			self.linea_de_recorte.linea_puntos.append(pos)
			self.linea_de_recorte.update()
		
		self.ultima_posicion_mouse_escena = self.mapToScene(event.pos())
		
		self.cambioPosEscena.emit(
			int(self.ultima_posicion_mouse_escena.x()), int(self.ultima_posicion_mouse_escena.y()),
		)
		
		super().mouseMoveEvent(event)
		
		
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Delete:
			if not self.eventoedicion:
				self.eliminarSeleccionado()
			else:
				super().keyPressEvent(event)
		# elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
		#	self.escena.escena.guardarArchivo("graph.json.txt")
		# elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
		#	self.escena.escena.abrirArchivo("graph.json.txt")
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
		
			for conexion in self.escena.escena.Conexiones:
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
	
	def ComenzarDibujadoConexion(self, objeto):
		if DEBUG: print('Vista: CDibujadoConexion - Comienza a dibujar la conexión.')
		if DEBUG: print('Vista: CDibujadoConexion -  Zócalo inicial asignado a:', objeto.zocalo)
		# self.conexion_anterior = objeto.zocalo.Zocaloconexiones
		self.zocalo_inicial_de_dibujado = objeto.zocalo
		self.dibujar_conexion = Conexion(self.escena.escena, objeto.zocalo, None, bezier)
		if DEBUG: print('Vista: CDibujadoConexion - Dibujado:', self.dibujar_conexion)
	
	def FinalizarDibujadoConexion(self, objeto):
		# Devuelve verdadero si se salta el resto del código
		self.modo = MODO_NORMAL
		
		if DEBUG: print('Vista: FDibujadoConexion - Termina de dibujar la conexión.')
		self.dibujar_conexion.quitar()
		self.dibujar_conexion = None
		
		if type(objeto) is GraficosDeZocalos:
			if objeto.zocalo != self.zocalo_inicial_de_dibujado:
				# Si soltamos el dibujado sobre un zocalo distinto al de inicio
				# if DEBUG: print('Vista: FDibujadoConexion -  conexion anterior', self.conexion_anterior)
				
				# if objeto.zocalo.tieneconexiones():
				#	objeto.zocalo.Zocaloconexiones.quitar()
				# for conexion in objeto.zocalo.Zocaloconexiones:
				#	if DEBUG: print('Vista: FDibujadoConexion - Limpiando conexiones en el destino:', conexion)
				#	conexion.quitar_de_zocalos()
				#	if DEBUG: print('Vista: FDibujadoConexion - Limpiando conexiones en el destino:', conexion, 'quitada')
				
				if not objeto.zocalo.esmulticonexion:
					objeto.zocalo.quitar_todas_las_conexiones()
					
				if not self.zocalo_inicial_de_dibujado.esmulticonexion:
					self.zocalo_inicial_de_dibujado.quitar_todas_las_conexiones()
				
				# if DEBUG: print('Vista: FDibujadoConexion -  Zócalo final asignado', objeto.zocalo)
				# if self.conexion_anterior is not None: self.conexion_anterior.quitar()
				# if DEBUG: print('Vista: FDibujadoConexion - Conexion anterior eliminada')
				# self.dibujar_conexion.zocalo_origen = self.zocalo_inicial_de_dibujado
				# self.dibujar_conexion.zocalo_final = objeto.zocalo
				# self.dibujar_conexion.zocalo_origen.agregar_conexion(self.dibujar_conexion)
				# self.dibujar_conexion.zocalo_final.agregar_conexion(self.dibujar_conexion)
				# if DEBUG: print('Vista: FDibujadoConexion -  Zócalo inicial y final reasignados')
				# self.dibujar_conexion.posiciones_actualizadas()
				
				nueva_conexion = Conexion(self.escena.escena, self.zocalo_inicial_de_dibujado, objeto.zocalo, tipo_de_conexion=bezier)
				if DEBUG: print('Vista: FDibujadoConexion - Nueva conexión creada:', nueva_conexion, 'conecta', nueva_conexion.zocalo_origen, 'y', nueva_conexion.zocalo_final)
				
				
				self.escena.escena.historial.almacenarHistorial("Conexion creada mediante dibujado", setModified=True)
				return True
		
		
		# if DEBUG: print('Vista: FDibujadoConexion - Sobre configurar el zocalo al anterior:', self.conexion_anterior)
		# if self.conexion_anterior is not None:
		# 	self.conexion_anterior.zocalo_origen.Zocaloconexiones = self.conexion_anterior
		
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
