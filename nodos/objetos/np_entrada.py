import math
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner

VALIDANTE_NUMÉRICO = QRegExpValidator(QRegExp("^[-+]?[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?[0-9]+)?$"))
VALIDANTE_COMPLEJO = QRegExpValidator(
		QRegExp(
		"^[-+]?[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?[0-9]+)?( - | \+ )[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?["
		"0-9]+)?i?$"
		)
		)


class Entrada(ObjetodeNodePlanner):
	def objeto(self):
		return QLineEdit

	def parámetros(self):
		return self.texto_inicial, self.elemento_padre

	def configuraciones_adicionales(self):
		self.objeto.setValidator(self.validante)

	def señal(self):
		self.objeto.textChanged.connect(self.contenido_del_objeto)
		self.objeto.textChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def conversor_númerico(self):
		try:
			valor_a_tratar = self.objeto.text().replace(" ", "")
			valor = float(valor_a_tratar)
			decimales, entero = math.modf(valor)

			if decimales == 0.0:
				return int(valor)
			else:
				return valor
		except ValueError:
			return 0

	def contenido_del_objeto(self):
		if self.validante == VALIDANTE_NUMÉRICO:
			self.elemento_padre.lista_de_información[self.índice] = self.conversor_númerico()
		else:
			self.elemento_padre.lista_de_información[self.índice] = self.objeto.text()

	def forma_de_deserialización(self):
		self.elemento_padre.lista_de_deserializamiento[self.índice] = self.objeto.setText