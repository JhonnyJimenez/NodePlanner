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
		self.etiqueta_1 = self.etiqueta("", "Centro", altura = self.altura_disponible)

	def lista_a_serializar(self, res):
		pass

	def lista_a_desearializar(self, data):
		pass

# @registrar_nodo(CATEGORIA_SALIDAS)
class Salidas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_SALIDAS
	titulo_op = "Salida"
	content_label_objname = "Salidas"

	ClaseGraficadeNodo = Salidas_Graficador
	ClasedelContenidodeNodo = Salidas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [8], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)
		self.evaluar()

	def actualizacion(self):
		pass

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		nodo_de_entrada = self.obtenerEntrada(0)
		if not nodo_de_entrada:
			self.Nodograficas.setToolTip("No hay un nodo conectado.")
			self.marcarInvalido()
			self.contenido.etiqueta_1.setText("Sin datos.")
			return

		contrazocalo = self.obtenerContrazocalo(0)
		valor = nodo_de_entrada.valores[contrazocalo.indice]

		if valor == '':
			self.Nodograficas.setToolTip("No hay datos en el nodo conectado.")
			self.marcarIndefinido()
			self.contenido.etiqueta_1.setText("Sin datos.")
			return

		valor = self.solucion_booleana(valor)

		self.contenido.etiqueta_1.setText(valor)
		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")

		return valor