from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5.QtCore import QSize, Qt, QByteArray, QDataStream, QIODevice, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QDrag

from lib.nodeeditor.Utilidades import dump_exception

from np_enlistado_de_nodos import *


class Lista(QListWidget):
	def __init__(self, parent = None):
		super().__init__()
		self.initUI()

	def initUI(self):
		# init
		self.setIconSize(QSize(22, 22))
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setDragEnabled(True)

		self.agregarMisObjetos()

	def agregarMisObjetos(self):
		keys = list(NODEPLANNER_NODOS.keys())
		keys.sort()
		for key in keys:
			nodo = obtener_clase_del_codigo_op(key)
			self.agregarMiObjeto(nodo.titulo_op, nodo.icono, nodo.codigo_op)

	def agregarMiObjeto(self, nombre, icono = None, codigo_operacion = 0):
		objeto = QListWidgetItem(nombre, self)  # Puede ser (icono, texto, parent, <int>type)
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

			itemData = QByteArray()
			dataStream = QDataStream(itemData, QIODevice.WriteOnly)
			dataStream << pixmap
			dataStream.writeInt(codigo_operacion)
			dataStream.writeQString(objeto.text())

			mimeData = QMimeData()
			mimeData.setData(LISTBOX_MIMETYPE, itemData)

			drag = QDrag(self)
			drag.setMimeData(mimeData)
			drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
			drag.setPixmap(pixmap)

			drag.exec_(Qt.MoveAction)

		except Exception as e:
			dump_exception(e)
