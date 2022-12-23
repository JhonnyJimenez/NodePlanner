from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoBooleana_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 64
		self.calculo_de_altura_disponible()

class NodoBooleana_Contenido(Entradas_Contenido):
	def contenidos(self):
		self.check = self.entrada_booleana(1)

	def objetos(self):
		self.check = self.booleana("Valor", 1)
		self.check.setGeometry(5, 5, self.anchoNodo - 14, 20)

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
		self.contenido.check.stateChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionBooleana()
		self.evaluarHijos()