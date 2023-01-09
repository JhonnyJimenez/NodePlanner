from nodos.categorías.entradas import *


class ContenidodelNodoBooleano(ContenidodelosNodosdeEntrada):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Booleana', alineado = 3, llave = 'Objeto 1', zócalo = 0),
				]
		self.contenido_de_entradas = [
				Booleana(self, 'Valor', 'Objeto 1', 0)
				]


@registrar_nodo(NODO_ENTRADA_BOOLEANA)
class NodoBooleano(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_BOOLEANA
	titulo_op = "Booleana"

	ClasedelContenidodeNodo = ContenidodelNodoBooleano

	Entradas = []
	Salidas = [3]

	FormaDeEntradas = []
	FormaDeSalidas = ['Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)