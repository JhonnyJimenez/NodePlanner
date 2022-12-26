from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoDecimal_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()


class NodoDecimal_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "0.000", validante = QDoubleValidator())

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])

@registrar_nodo(NODO_ENTRADA_DECIMAL)
class NodoDecimal(Entradas):
	icono = imagen
	codigo_op = NODO_ENTRADA_DECIMAL
	titulo_op = "Valor"
	content_label_objname = "Valor"

	ClaseGraficadeNodo = NodoDecimal_Graficador
	ClasedelContenidodeNodo = NodoDecimal_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [2]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.Evaluacion_de_decimales(self.contenido.objeto_1)
		self.evaluarHijos()