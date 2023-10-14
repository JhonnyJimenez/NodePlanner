from PyQt5.QtWidgets import QComboBox
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner


class Desplegable(ObjetodeNodePlanner):
	def __init__(
			self, elemento_padre = None, llave: str = None, lista = None, separadores = None,
			elementos_visibles = 6, **kwargs
			):
		self.actualizar_lista(lista)
		self.separadores = separadores
		self.elementos_visibles = elementos_visibles
		super().__init__(elemento_padre, llave = llave, **kwargs)

	def definir_objeto(self):
		return QComboBox(self.elemento_padre)

	def estilo(self):
		self.objeto.setStyleSheet('combobox-popup: 0; background: #808080')

	def configuraciones_adicionales(self):
		if self.lista not in (None, []):
			self.objeto.clear()
			self.objeto.addItems(self.lista)
			if self.separadores not in (None, []):
				for separador in self.separadores:
					self.objeto.insertSeparator(separador)

		if self.elementos_visibles is not None:
			self.objeto.setMaxVisibleItems(self.elementos_visibles
			                               + (len(self.separadores) if self.separadores is not None else 0)
			                               )

	def señal(self):
		self.objeto.currentTextChanged.connect(self.contenido)
		self.objeto.currentTextChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def escribir_dato(self):
		return self.objeto.currentText()

	def deserialización(self, dato):
		self.objeto.setCurrentText(dato)

	def actualizar_lista(self, lista):
		self.lista = lista