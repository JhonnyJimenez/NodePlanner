from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoNúmero_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.calculo_de_altura_disponible()


class NodoNúmero_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "0", validante = QDoubleValidator())

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])

@registrar_nodo(NODO_ENTRADA_NÚMERO)
class NodoNúmero(Entradas):
	icono = imagen
	codigo_op = NODO_ENTRADA_NÚMERO
	titulo_op = "Número"
	content_label_objname = "Número"

	ClaseGraficadeNodo = NodoNúmero_Graficador
	ClasedelContenidodeNodo = NodoNúmero_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [0]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica(self.contenido.objeto_1)
		self.evaluarHijos()