from PyQt5.QtWidgets import QComboBox
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner


class Desplegable(ObjetodeNodePlanner):
	def definir_objeto(self):
		self.objeto = self.objeto()(self.parámetros())

	def objeto(self):
		return QComboBox

	def parámetros(self):
		return self.elemento_padre

	def configuraciones_adicionales(self):
		if self.lista not in (None, []):
			self.objeto.addItems(self.lista)

		if self.separadores not in (None, []) and self.lista not in (None, []):
			for separador in self.separadores:
				self.objeto.insertSeparator(separador)

		if self.valor_inicial is not None:
			self.objeto.setMaxVisibleItems(self.valor_inicial
			                               + (len(self.separadores) if self.separadores is not None else 0)
			                               )

	def estilo(self):
		self.objeto.setStyleSheet('combobox-popup: 0; background: #808080')

	def señal(self):
		self.objeto.currentTextChanged.connect(self.contenido_del_objeto)
		self.objeto.currentTextChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def contenido_del_objeto(self):
		self.elemento_padre.lista_de_información[self.índice] = self.objeto.currentText()

	def forma_de_deserialización(self):
		self.elemento_padre.lista_de_deserializamiento[self.índice] = self.objeto.setCurrentText