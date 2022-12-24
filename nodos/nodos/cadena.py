from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoCadena_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.calculo_de_altura_disponible()


class NodoCadena_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "")

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])


@registrar_nodo(NODO_ENTRADA_CADENA)
class NodoCadena(Entradas):
	icono = imagen
	codigo_op = NODO_ENTRADA_CADENA
	titulo_op = "Cadena"
	content_label_objname = "Cadena"

	ClaseGraficadeNodo = NodoCadena_Graficador
	ClasedelContenidodeNodo = NodoCadena_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [1]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		# self.contenido.objeto_1.editingFinished.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica(self.contenido.objeto_1)
		self.evaluarHijos()