from PyQt5.QtGui import *
from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from nodeeditor.Widget_de_nodos import EditorDeNodos
from examples.example_calculator.calc_nodo_base import *
from nodeeditor.Conexiones import bezier, recta
from nodeeditor.Utilidades import dump_exception

DEBUG = False
DEBUG_CONTEXT = True


class SubVenCalc(EditorDeNodos):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self.definirtitulo()
		
		self.initNuevaOpciondeNodo()
		
		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		self.escena.agregarDragEnterListener(self.arrastrar)
		self.escena.agregarDropListener(self.soltar)
		self.escena.definirSelectordeClasesdeNodos(self.obtener_clase_del_nodo_de_datos)
		
		self._close_event_listeners = []
		
	def obtener_clase_del_nodo_de_datos(self, data):
		if 'Codigo_op' not in data: return None
		return obtener_clase_del_codigo_op(data['Codigo_op'])
	
	def initNuevaOpciondeNodo(self):
		self.opciones_de_nodos = {}
		keys = list(CALC_NODOS.keys())
		keys.sort()
		for key in keys:
			nodo = CALC_NODOS[key]
			self.opciones_de_nodos[nodo.codigo_op] = QAction(QIcon(nodo.icono), nodo.titulo_op)
			self.opciones_de_nodos[nodo.codigo_op].setData(nodo.codigo_op)
		
	def initMenuContextualNodos(self):
		menu_contextual = QMenu(self)
		keys = list(CALC_NODOS.keys())
		keys.sort()
		for key in keys: menu_contextual.addAction(self.opciones_de_nodos[key])
		return menu_contextual
	
	def definirtitulo(self):
		self.setWindowTitle(self.obtenerNombreAmigablealUsuario())
		
	def agregarCloseEventListeners(self, callback):
		self._close_event_listeners.append(callback)
		
	def closeEvent(self, event):
		for callback in self._close_event_listeners: callback(self, event)
		
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
			
			if DEBUG: print("Objeto soltado: [%d] '%s'" % (codigo_op, text), "Mouse:", mouse_pos, "Escena:", escena_pos)
			
			try:
				nodo = obtener_clase_del_codigo_op(codigo_op)(self.escena)
				nodo.definirposicion(escena_pos.x(), escena_pos.y())
				self.escena.historial.almacenarHistorial("Creación de un nodo: %s" % nodo.__class__.__name__)
			except Exception as e: dump_exception(e)
			
			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			# print("El archivo soltado fue ignorado: formato requerido: %d" % LISTBOX_MIMETYPE)
			event.ignore()
			
	def contextMenuEvent(self, event):
		try:
			objeto = self.escena.obtenerObjetoAl(event.pos())
			if DEBUG_CONTEXT: print(objeto)
			
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
		except Exception as e: dump_exception(e)
		
	def controlMenuContextualNodos(self, event):
		if DEBUG_CONTEXT: print("Menú contextual: NODO")
		menu_contextual = QMenu(self)
		opcionProblematico = menu_contextual.addAction("Marcar como problemático")
		opcionInvalido = menu_contextual.addAction("Marcar como invalido")
		opcionDesmarcarInvalido = menu_contextual.addAction("Desmarcar como invalido")
		opcionEvaluado = menu_contextual.addAction("Evaluado")
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))
		
		seleccionado = None
		objeto = self.escena.obtenerObjetoAl(event.pos())
		if type(objeto) == QGraphicsProxyWidget:
			objeto = objeto.widget()
		
		if hasattr(objeto, 'nodo'):
			seleccionado = objeto.nodo
		if hasattr(objeto, 'zocalo'):
			seleccionado = objeto.zocalo.nodo
		
		if DEBUG_CONTEXT: print("Objeto obtenido:", seleccionado)
		# ToDo: Funciones para las opciones del menú.
	
	def controlMenuContextualLinea(self, event):
		if DEBUG_CONTEXT: print("Menú contextual: LINEA")
		menu_contextual = QMenu(self)
		opcionBezier = menu_contextual.addAction("Línea bezier")
		opcionRecta = menu_contextual.addAction("Línea recta")
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))
		
		seleccionado = None
		objeto = self.escena.obtenerObjetoAl(event.pos())
		if hasattr(objeto, 'linea'):
			seleccionado = objeto.linea

		if seleccionado and accion == opcionBezier: seleccionado.tipo_de_conexion = bezier
		if seleccionado and accion == opcionRecta: seleccionado.tipo_de_conexion = recta
	
	def controlMenuContextualNuevoNodo(self, event):
		if DEBUG_CONTEXT: print("Menú contextual: NUEVO NODO")
		menu_contextual = self.initMenuContextualNodos()
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))
		
		if accion is not None:
			nuevo_calcnodo = obtener_clase_del_codigo_op(accion.data())(self.escena)
			pos_escena = self.escena.obtenerVista().mapToScene(event.pos())
			nuevo_calcnodo.definirposicion(pos_escena.x(), pos_escena.y())
			print("Nodo seleccionado:", nuevo_calcnodo)
		