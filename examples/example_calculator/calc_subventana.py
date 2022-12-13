from PyQt5.QtGui import *
from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from nodeeditor.Widget_de_nodos import EditorDeNodos
from examples.example_calculator.calc_nodo_base import CalcNodo
from nodeeditor.Utilidades import dump_exception


DEBUG = False


class SubVenCalc(EditorDeNodos):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self.definirtitulo()
		
		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		self.escena.agregarDragEnterListener(self.arrastrar)
		self.escena.agregarDropListener(self.soltar)
		self.escena.definirSelectordeClasesdeNodos(self.obtener_clase_del_nodo_de_datos)
		
		self._close_event_listeners = []
		
	def obtener_clase_del_nodo_de_datos(self, data):
		if 'Codigo_op' not in data: return None
		return obtener_clase_del_codigo_op(data['Codigo_op'])
	
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
			
			