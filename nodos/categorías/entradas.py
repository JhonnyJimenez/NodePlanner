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
		self.objeto_1 = self.entrada_de_línea(1, "")
		self.objeto_2 = self.entrada_booleana(2, 0, "Valor")

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()
		res['Objeto_2'] = self.objeto_2.checkState()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])
		self.objeto_2.setCheckState(data['Objeto_2'])


# @registrar_nodo(CATEGORIA_ENTRADAS)
class Entradas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_ENTRADAS
	titulo_op = "Entrada"
	content_label_objname = "Entradas"

	ClaseGraficadeNodo = Entradas_Graficador
	ClasedelContenidodeNodo = Entradas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [1, 2]):
		super().__init__(escena, titulo, entradas, salidas)
		self.evaluar()
		self.actualizacion()

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_2.stateChanged.connect(self.DatosdeEntradaCambiados)

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica(self.contenido.objeto_1)
		self.EvaluacionBooleana(self.contenido.objeto_2)
		self.evaluarHijos()