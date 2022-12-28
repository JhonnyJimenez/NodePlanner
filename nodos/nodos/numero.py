from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class Número_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()


class Número_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "0", validante = VALIDANTE_NUMÉRICO)

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])

@registrar_nodo(NODO_ENTRADA_NÚMERO)
class Número(Entradas):
	icono = imagen
	codigo_op = NODO_ENTRADA_NÚMERO
	titulo_op = "Número"
	content_label_objname = "Número"

	ClaseGraficadeNodo = Número_Graficador
	ClasedelContenidodeNodo = Número_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [1]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.evaluacion_númerica(self.contenido.objeto_1)
		self.evaluarHijos()
