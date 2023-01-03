from nodos.categorías.entradas import *

class ContenidodelNodoNúmero(ContenidodelosNodosdeEntrada):
	def controles(self):
		super().controles()
		self.placeholder(1)

	def contenido(self):
		self.objeto_0 = Entrada(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = '0', validante = VALIDANTE_NUMÉRICO
				)

@registrar_nodo(NODO_ENTRADA_NÚMERO)
class NodoNúmero(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_NÚMERO
	titulo_op = "Número"

	ClasedelContenidodeNodo = ContenidodelNodoNúmero

	Entradas = []
	Salidas = [1]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)