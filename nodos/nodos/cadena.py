from nodos.categorías.entradas import *


class ContenidodelNodoCadena(ContenidodelosNodosdeEntrada):
	def controles(self):
		super().controles()
		self.placeholder(1)

	def contenido(self):
		self.objeto_0 = Entrada(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = ''
				)

@registrar_nodo(NODO_ENTRADA_CADENA)
class NodoCadena(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_CADENA
	titulo_op = "Cadena"

	ClasedelContenidodeNodo = ContenidodelNodoCadena

	Entradas = []
	Salidas = [4]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)