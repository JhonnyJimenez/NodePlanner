from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoBooleana_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.calculo_de_altura_disponible()

class NodoBooleana_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_booleana(1)

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.checkState()

	def lista_a_desearializar(self, data):
		self.objeto_1.setCheckState(data['Objeto_1'])

@registrar_nodo(NODO_ENTRADA_BOOLEANA)
class NodoBooleana(Entradas):
	icono = imagen
	codigo_op = NODO_ENTRADA_BOOLEANA
	titulo_op = "Booleana"
	content_label_objname = "Booleana"

	ClaseGraficadeNodo = NodoBooleana_Graficador
	ClasedelContenidodeNodo = NodoBooleana_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [2]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.stateChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionBooleana(self.contenido.objeto_1)
		self.evaluarHijos()