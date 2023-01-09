from nodos.categorías.entradas import *


class ContenidodelNodoNúmero(ContenidodelosNodosdeEntrada):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Número', alineado = 3, llave = 'Objeto 1', zócalo = 0)
				]
		self.contenido_de_entradas = [
				Entrada(self, '0', 'Objeto 1', validante = VALIDANTE_NUMÉRICO)
				]


@registrar_nodo(NODO_ENTRADA_NÚMERO)
class NodoNúmero(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_NÚMERO
	titulo_op = "Número"

	ClasedelContenidodeNodo = ContenidodelNodoNúmero

	Entradas = []
	Salidas = [1]

	FormaDeEntradas = []
	FormaDeSalidas = ['Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)