from PyQt5.QtGui import *
from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from nodeeditor.Widget_de_nodos import EditorDeNodos
from nodeeditor.Nodo import Nodo


class SubVenCalc(EditorDeNodos):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self.definirtitulo()
		
		self.escena.agregarElementosModificadosListener(self.definirtitulo)
		self.escena.agregarDragEnterListener(self.arrastrar)
		self.escena.agregarDropListener(self.soltar)
		
		
		self._close_event_listeners = []
		
	def definirtitulo(self):
		self.setWindowTitle(self.obtenerNombreAmigablealUsuario())
		
	def agregarCloseEventListeners(self, callback):
		self._close_event_listeners.append(callback)
		
	def closeEvent(self, event):
		for callback in self._close_event_listeners: callback(self, event)
		
	def arrastrar(self, event):
		# print("Subventana de calculadora: Arrastrando objeto")
		# print("Texto: '%s'" % event.mimeData().text())
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			event.acceptProposedAction()
		else:
			# print("... Arrastre de objeto denegado")
			event.setAccepted(False)
	
	def soltar(self, event):
		# print("Subventana de calculadora: Soltando objeto")
		# print("Texto: '%s'" % event.mimeData().text())
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			eventData = event.mimeData().data(LISTBOX_MIMETYPE)
			dataStream = QDataStream(eventData, QIODevice.ReadOnly)
			pixmap = QPixmap()
			dataStream >> pixmap
			codigo_operacion = dataStream.readInt()
			text = dataStream.readQString()
			
			mouse_pos = event.pos()
			escena_pos = self.escena.GraficosEsc.views()[0].mapToScene(mouse_pos)
			
			print("Objeto soltado: [%d] '%s'" % (codigo_operacion, text), "Mouse:", mouse_pos, "Escena:", escena_pos)
			
			# ¡Arréglame!
			nodo = Nodo(self.escena, text, entradas=[1, 1], salidas=[2])
			nodo.definirposicion(escena_pos.x(), escena_pos.y())
			self.escena.agregarnodo(nodo)
			
			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			# print("El archivo soltado fue ignorado: formato requerido: %d" % LISTBOX_MIMETYPE)
			event.ignore()
			
			