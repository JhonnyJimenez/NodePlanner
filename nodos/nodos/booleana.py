from nodos.categorías.entradas import *


class ContenidodelNodoBooleano(ContenidodelosNodosdeEntrada):
	def controles(self):
		super().controles()
		self.placeholder(1)

	def contenido(self):
		self.objeto_0 = Booleana(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = 'Valor',
				valor_inicial = 2
				)

@registrar_nodo(NODO_ENTRADA_BOOLEANA)
class NodoBooleano(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_BOOLEANA
	titulo_op = "Booleana"

	ClasedelContenidodeNodo = ContenidodelNodoBooleano

	Entradas = []
	Salidas = [3]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)