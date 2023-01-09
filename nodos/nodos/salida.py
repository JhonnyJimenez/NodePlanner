from nodos.categorías.salidas import *


@registrar_nodo(NODO_SALIDA)
class Salida(Salidas):
	codigo_op = NODO_SALIDA
	titulo_op = "Salida"

	Entradas = [0]
	Salidas = []

	FormaDeEntradas = ['Círculo']
	FormaDeSalidas = []

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)