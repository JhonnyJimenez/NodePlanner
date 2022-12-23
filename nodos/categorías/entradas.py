from np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/edit.svg"

class Entradas_Graficador(NodoBase_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 89
		self.calculo_de_altura_disponible()

	def initAssets(self):
		super().initAssets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF83314A"))


class Entradas_Contenido(NodoBase_Contenido):
	def contenidos(self):
		self.entrada = self.entrada_de_línea(1, "")
		self.check = self.entrada_booleana(2, 0, "Valor")


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

	def ediciones_de_espaciado(self):
		pass

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