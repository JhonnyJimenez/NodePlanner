from PyQt5.QtWidgets import QLineEdit, QCheckBox
from PyQt5.QtGui import QFont

from np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/edit.svg"

class Entradas_Graficador(NodoBase_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 79

	def initAssets(self):
		super().initAssets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF83314A"))


class Entradas_Contenido(NodoBase_Contenido):
	def initui(self):
		super().initui()
		self.objetos()

	def objetos(self):
		self.entrada = self.linea("", 1)
		self.check = self.booleana("Valor", 2, True)

	def linea(self, valor, zocalo: int = None, validante = None):
		linea = QLineEdit(valor, self)
		linea.zocalo = zocalo - 1
		validante = validante

		linea.setGeometry(5, 5, self.anchoNodo - 14, 20)
		linea.setAlignment(Qt.AlignCenter)
		linea.setObjectName(self.nodo.content_label_objname)
		linea.setFont(QFont("Ubuntu"))
		linea.setValidator(validante)
		return linea

	def booleana(self, etiqueta,  zocalo: int = None, indeterminado: bool = False):
		booleana = QCheckBox(etiqueta, self)
		booleana.zocalo = zocalo - 1
		booleana.setTristate(indeterminado)
		booleana.setGeometry(5, 30, self.anchoNodo - 14, 20)
		booleana.setObjectName(self.nodo.content_label_objname)
		booleana.setFont(QFont("Ubuntu"))
		return booleana

# @registrar_nodo(CATEGORIA_ENTRADAS)
class Entradas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_ENTRADAS
	titulo_op = "Entrada"
	content_label_objname = "Entradas"

	ClaseGraficadeNodo = Entradas_Graficador
	ClasedelContenidodeNodo = Entradas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [0, 2]):
		super().__init__(escena, titulo, entradas, salidas)
		self.evaluar()
		self.actualizacion()

	def actualizacion(self):
		self.contenido.entrada.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.check.stateChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica()
		self.EvaluacionBooleana()
		self.evaluarHijos()

	def EvaluacionNumerica(self):
		self.valores[self.contenido.entrada.zocalo] = self.contenido.entrada.text()

		if self.valores[self.contenido.entrada.zocalo] == '':
			self.marcarInvalido()
		else:
			self.marcarIndefinido(False)
			self.marcarInvalido(False)
			self.Nodograficas.setToolTip("")

		return self.valores[self.contenido.entrada.zocalo]

	def EvaluacionBooleana(self):
		self.valores[self.contenido.check.zocalo] = self.contenido.check.checkState()
		self.marcarIndefinido(False)
		self.marcarInvalido(False)

		return self.valores[self.contenido.check.zocalo]