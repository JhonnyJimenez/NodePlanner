from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *


class NodoNúmero_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.altoNodo = 54

class NodoNúmero_Contenido(Entradas_Contenido):
	def initui(self):
		super().initui()

	def objetos(self):
		self.entrada = self.linea("0", 1, QDoubleValidator())

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
		self.contenido.entrada.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica()
		self.evaluarHijos()