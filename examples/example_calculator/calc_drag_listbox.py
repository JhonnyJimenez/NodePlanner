from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


imagen = "iconos/owoAwoo.png"

class Listbox(QListWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		# init
		self.setIconSize(QSize(32, 32))
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setDragEnabled(True)
		
		
		self.agregarMisObjetos()
		
	def agregarMisObjetos(self):
		self.agregarMiObjeto("Entrada", imagen)
		self.agregarMiObjeto("Salida", imagen)
		self.agregarMiObjeto("Sumar", imagen)
		self.agregarMiObjeto("Restar", imagen)
		self.agregarMiObjeto("Multiplicar", imagen)
		self.agregarMiObjeto("Dividir", imagen)
		
	def agregarMiObjeto(self, nombre, icono=None, codigo_operacion=0):
		objeto = QListWidgetItem(nombre, self) # Puede ser (icono, texto, parent, <int>type)
		pixmap = QPixmap(icono if icono is not None else ".")
		objeto.setIcon(QIcon(pixmap))
		objeto.setSizeHint(QSize(32, 32))
		
		objeto.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
		
		# Configuración de los datos
		objeto.setData(Qt.UserRole, pixmap)
		objeto.setData(Qt.UserRole + 1, codigo_operacion)