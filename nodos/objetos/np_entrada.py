from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner
from nodos.objetos.np_utilitarios import alineador, conversor_númerico_python, conversor_númerico_mpmath
from np_constantes import NOMBRE_DEL_PRODUCTO

VALIDANTE_NUMÉRICO = QRegExpValidator(QRegExp("^[-+]?[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?[0-9]+)?$"))
VALIDANTE_COMPLEJO = QRegExpValidator(
		QRegExp(
		"^[-+]?[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?[0-9]+)?( - | \+ )[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?["
		"0-9]+)?i?$"
		)
		)


class Entrada(ObjetodeNodePlanner):
	def __init__(
			self, elemento_padre = None, texto: str = NOMBRE_DEL_PRODUCTO, llave: str = None, alineado: str | int = 2,
			validante = None, tipo_de_validante = 1, tipo: int = 1, **kwargs
			):
		self.texto = texto
		self.alineado = alineado
		self.validante = validante
		self.tipo_de_validante = tipo_de_validante
		self.tipo = tipo
		super().__init__(elemento_padre, llave = llave, **kwargs)

	def definir_objeto(self):
		return QLineEdit(self.texto, self.elemento_padre)

	def estilo(self):
		alineador(self.objeto, self.alineado)

	def configuraciones_adicionales(self):
		if self.validante is not None:
			self.objeto.setValidator(self.validante)

	def señal(self):
		if self.tipo == 1:
			self.objeto.textChanged.connect(self.contenido)
			self.objeto.textChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)
		elif self.tipo == 2:
			self.objeto.editingFinished.connect(self.contenido)
			self.objeto.editingFinished.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def escribir_dato(self):
		if self.validante == VALIDANTE_NUMÉRICO:
			if self.tipo_de_validante == 2:
				return conversor_númerico_python(self.objeto.text())
			else:
				return conversor_númerico_mpmath(self.objeto.text())
		else:
			return self.objeto.text()

	def deserialización(self, dato):
		self.objeto.setText(dato)
