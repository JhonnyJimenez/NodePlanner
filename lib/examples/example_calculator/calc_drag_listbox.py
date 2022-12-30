from PyQt5.QtGui import QPixmap, QIcon, QDrag
from PyQt5.QtCore import QSize, Qt, QByteArray, QDataStream, QIODevice, QMimeData, QPoint
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem

from lib.examples.example_calculator.calc_config import *
from lib.nodeeditor.Utilidades import dump_exception


class Listbox(QListWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.init_ui()
		
	def init_ui(self):
		# init
		self.setIconSize(QSize(32, 32))
		self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
		self.setDragEnabled(True)
		
		
		self.agregar_mis_objetos()
		
	def agregar_mis_objetos(self):
		keys = list(CALC_NODOS.keys())
		keys.sort()
		for key in keys:
			nodo = obtener_clase_del_codigo_op(key)
			self.agregar_mi_objeto(nodo.titulo_op, nodo.icono, nodo.codigo_op)
		
	def agregar_mi_objeto(self, nombre, icono=None, codigo_operacion=0):
		objeto = QListWidgetItem(nombre, self) # Puede ser (icono, texto, parent, <int>type)
		pixmap = QPixmap(icono if icono is not None else ".")
		objeto.setIcon(QIcon(pixmap))
		objeto.setSizeHint(QSize(32, 32))
		
		objeto.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
		
		# Configuración de los datos
		objeto.setData(Qt.UserRole, pixmap)
		objeto.setData(Qt.UserRole + 1, codigo_operacion)
		
	def startDrag(self, *args, **kwargs):
		# print("ListBox::startDrag")
		
		try:
			objeto = self.currentItem()
			codigo_operacion = objeto.data(Qt.UserRole + 1)
			# print("Arrastrando objeto <%d>" % codigo_operacion, objeto)
			
			pixmap = QPixmap(objeto.data(Qt.UserRole)).scaled(32, 32, 1, 1)
			
			item_data = QByteArray()
			data_stream = QDataStream(item_data, QIODevice.WriteOnly)
			data_stream << pixmap
			data_stream.writeInt(codigo_operacion)
			data_stream.writeQString(objeto.text())
			
			mime_data = QMimeData()
			mime_data.setData(LISTBOX_MIMETYPE, item_data)
			
			drag = QDrag(self)
			drag.setMimeData(mime_data)
			drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
			drag.setPixmap(pixmap)
			
			drag.exec_(Qt.MoveAction)
			
		except Exception as e: dump_exception(e)