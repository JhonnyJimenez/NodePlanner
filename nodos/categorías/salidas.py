from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

from np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/visibility.svg"

class Salidas_Graficador(NodoBase_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 64
		self.calculo_de_altura_disponible()

	def initAssets(self):
		super().initAssets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF3C1D26"))

class Salidas_Contenido(NodoBase_Contenido):
	def contenidos(self):
		self.pantalla = self.etiqueta("", "Centro", altura = self.altura_disponible)

# @registrar_nodo(CATEGORIA_SALIDAS)
class Salidas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_SALIDAS
	titulo_op = "Salida"
	content_label_objname = "Salidas"

	ClaseGraficadeNodo = Salidas_Graficador
	ClasedelContenidodeNodo = Salidas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [3], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)
		self.evaluar()

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		nodo_de_entrada = self.obtenerEntrada(0)
		if not nodo_de_entrada:
			self.Nodograficas.setToolTip("No hay un nodo conectado.")
			self.marcarInvalido()
			self.contenido.pantalla.setText("Sin datos.")
			return

		contrazocalo = self.obtenerContrazocalo(0)
		valor = nodo_de_entrada.valores[contrazocalo.indice]

		if valor == '':
			self.Nodograficas.setToolTip("No hay datos en el nodo conectado.")
			self.marcarIndefinido()
			self.contenido.pantalla.setText("Sin datos.")
			return

		if type(valor) == Qt.CheckState:
			if valor == 0:
				valor = 'Falso'
			if valor == 1:
				valor = 'Indeterminado'
			if valor == 2:
				valor = 'Verdadero'

		self.contenido.pantalla.setText(valor)
		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")

		return valor