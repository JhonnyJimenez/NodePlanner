from PyQt5.QtWidgets import QAction, QMenu, QGraphicsProxyWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDataStream, QIODevice, Qt

from lib.nodeeditor.Widget_de_nodos import EditorDeNodos
from lib.nodeeditor.Utilidades import dump_exception
from lib.nodeeditor.Conexiones import bezier, recta
from lib.nodeeditor.GraficosVista import MODO_DIBUJO

from np_enlistado_de_nodos import *
from nodos.categorías.salidas import Salidas

DEBUG = False
DEBUG_CONTEXT = False


class NodePlannerSubVentana(EditorDeNodos):
	def __init__(self):
		super().__init__()
		# self.setAttribute(Qt.WA_DeleteOnClose)

		self.definirtitulo()

		self.initNuevaOpciondeNodo()

		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		self.escena.historial.agregarrestauradodelhistorialisteners(self.alRestaurarHistorial)
		self.escena.agregarDragEnterListener(self.arrastrar)
		self.escena.agregarDropListener(self.soltar)
		self.escena.definirSelectordeClasesdeNodos(self.obtener_clase_del_nodo_de_datos)

		self._close_event_listeners = []

	def obtener_clase_del_nodo_de_datos(self, data):
		if 'Codigo_op' not in data:
			return None
		return obtener_clase_del_codigo_op(data['Codigo_op'])

	def hacerEvaluaciondeSalidas(self):
		# Evaluar todos los nodos de salida.
		for nodo in self.escena.Nodos:
			if isinstance(nodo, Salidas):
				nodo.evaluar()

	def alRestaurarHistorial(self):
		self.hacerEvaluaciondeSalidas()

	def leerarchivo(self, filename):
		if super().leerarchivo(filename):
			self.hacerEvaluaciondeSalidas()
			return True

		return False

	def initNuevaOpciondeNodo(self):
		self.opciones_de_nodos = {}
		keys = list(NODEPLANNER_NODOS.keys())
		keys.sort()
		for key in keys:
			nodo = NODEPLANNER_NODOS[key]
			self.opciones_de_nodos[nodo.codigo_op] = QAction(QIcon(nodo.icono), nodo.titulo_op)
			self.opciones_de_nodos[nodo.codigo_op].setData(nodo.codigo_op)

	def initMenuContextualNodos(self):
		menu_contextual = QMenu(self)
		keys = list(NODEPLANNER_NODOS.keys())
		keys.sort()
		for key in keys:
			menu_contextual.addAction(self.opciones_de_nodos[key])
		return menu_contextual

	def definirtitulo(self):
		self.setWindowTitle(self.obtenerNombreAmigablealUsuario())

	def agregarCloseEventListeners(self, callback):
		self._close_event_listeners.append(callback)

	def closeEvent(self, event):
		for callback in self._close_event_listeners:
			callback(self, event)

	def arrastrar(self, event):
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			event.acceptProposedAction()
		else:
			# print("... Arrastre de objeto denegado")
			event.setAccepted(False)

	def soltar(self, event):
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			eventData = event.mimeData().data(LISTBOX_MIMETYPE)
			dataStream = QDataStream(eventData, QIODevice.ReadOnly)
			pixmap = QPixmap()
			dataStream >> pixmap
			codigo_op = dataStream.readInt()
			text = dataStream.readQString()

			mouse_pos = event.pos()
			escena_pos = self.escena.GraficosEsc.views()[0].mapToScene(mouse_pos)

			if DEBUG:
				print("Objeto soltado: [%d] '%s'" % (codigo_op, text), "Mouse:", mouse_pos, "Escena:", escena_pos)

			try:
				nodo = obtener_clase_del_codigo_op(codigo_op)(self.escena)
				nodo.definirposicion(escena_pos.x(), escena_pos.y())
				self.escena.historial.almacenarHistorial(
					"Creación de un nodo: %s" % nodo.__class__.__name__, setModified = True
					)
			except Exception as e:
				dump_exception(e)

			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			# print("El archivo soltado fue ignorado: formato requerido: %d" % LISTBOX_MIMETYPE)
			event.ignore()

	def contextMenuEvent(self, event):
		try:
			objeto = self.escena.obtenerObjetoAl(event.pos())
			if DEBUG_CONTEXT:
				print(objeto)

			if type(objeto) == QGraphicsProxyWidget:
				objeto = objeto.widget()

			if hasattr(objeto, 'nodo') or hasattr(objeto, 'zocalo'):
				self.controlMenuContextualNodos(event)
			elif hasattr(objeto, 'linea'):
				self.controlMenuContextualLinea(event)
			# elif objeto is None:
			else:
				self.controlMenuContextualNuevoNodo(event)

			return super().contextMenuEvent(event)
		except Exception as e:
			dump_exception(e)

	def controlMenuContextualNodos(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: NODO")
		menu_contextual = QMenu(self)
		opcionIndefinido = menu_contextual.addAction("Marcar indefinido")
		opcionDescendenciaIndefinido = menu_contextual.addAction("Marcar descendencia indefinido")
		opcionInvalido = menu_contextual.addAction("Marcar inválido")
		opcionDesmarcarInvalido = menu_contextual.addAction("Desmarcar invalido")
		opcionEvaluado = menu_contextual.addAction("Marcar evaluado")
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		seleccionado = None
		objeto = self.escena.obtenerObjetoAl(event.pos())
		if type(objeto) == QGraphicsProxyWidget:
			objeto = objeto.widget()

		if hasattr(objeto, 'nodo'):
			seleccionado = objeto.nodo
		if hasattr(objeto, 'zocalo'):
			seleccionado = objeto.zocalo.nodo

		if DEBUG_CONTEXT:
			print("Objeto obtenido:", seleccionado)
		if seleccionado and accion == opcionIndefinido:
			seleccionado.marcarIndefinido()
		if seleccionado and accion == opcionDescendenciaIndefinido:
			seleccionado.marcarDescendenciaIndefinido()
		if seleccionado and accion == opcionInvalido:
			seleccionado.marcarInvalido()
		if seleccionado and accion == opcionDesmarcarInvalido:
			seleccionado.marcarInvalido(False)
		if seleccionado and accion == opcionEvaluado:
			val = seleccionado.evaluar()
			if DEBUG_CONTEXT:
				print("EVALUADO:", val)

	def controlMenuContextualLinea(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: LINEA")
		menu_contextual = QMenu(self)
		opcionBezier = menu_contextual.addAction("Línea bezier")
		opcionRecta = menu_contextual.addAction("Línea recta")
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		seleccionado = None
		objeto = self.escena.obtenerObjetoAl(event.pos())
		if hasattr(objeto, 'linea'):
			seleccionado = objeto.linea

		if seleccionado and accion == opcionBezier:
			seleccionado.tipo_de_conexion = bezier
		if seleccionado and accion == opcionRecta:
			seleccionado.tipo_de_conexion = recta

	# Funciones de apoyo.
	def definirZocaloObjetivoenelNodo(self, flag_ya_dibujado, nuevo_calcnodo):
		zocalo_objetivo = None
		if flag_ya_dibujado:
			if len(nuevo_calcnodo.entradas) > 0:
				zocalo_objetivo = nuevo_calcnodo.entradas[0]
		else:
			if len(nuevo_calcnodo.salidas) > 0:
				zocalo_objetivo = nuevo_calcnodo.salidas[0]
		return zocalo_objetivo

	def finalizarNuevoEstadodelNodo(self, nuevo_calcnodo):
		self.escena.hacerDeseleccionarObjetos()
		nuevo_calcnodo.Nodograficas.hacerSeleccion()
		nuevo_calcnodo.Nodograficas.seleccionado()

	def controlMenuContextualNuevoNodo(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: NUEVO NODO")
		menu_contextual = self.initMenuContextualNodos()
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		if accion is not None:
			nuevo_calcnodo = obtener_clase_del_codigo_op(accion.data())(self.escena)
			pos_escena = self.escena.obtenerVista().mapToScene(event.pos())
			nuevo_calcnodo.definirposicion(pos_escena.x(), pos_escena.y())
			if DEBUG_CONTEXT:
				print("Nodo seleccionado:", nuevo_calcnodo)

			if self.escena.obtenerVista().modo == MODO_DIBUJO:
				# Cuando se dibuja una conexion:
				zocalo_objetivo = self.definirZocaloObjetivoenelNodo(
					self.escena.obtenerVista().dibujado.zocalo_inicial_de_dibujado.esSalida, nuevo_calcnodo
					)
				if zocalo_objetivo is not None:
					self.escena.obtenerVista().dibujado.FinalizarDibujadoConexion(zocalo_objetivo.GraficosZocalos)
				self.finalizarNuevoEstadodelNodo()

			else:
				self.escena.historial.almacenarHistorial("Nodo %s creado" % nuevo_calcnodo.__class__.__name__)
