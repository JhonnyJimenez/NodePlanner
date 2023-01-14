from np_enlistado_de_nodos import *
from nodos.categorías.entradas import ContenidodelosNodosdeEntrada, NodosdeEntrada

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada


class ContenidodelNodoCadena(ContenidodelosNodosdeEntrada):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Cadena', alineado = 3, llave = 'Entrada 1', zócalo = 0)
				]
		self.contenido_de_entradas = [
				Entrada(self, '', 'Entrada 1')
				]


@registrar_nodo(NODO_ENTRADA_CADENA)
class NodoCadena(NodosdeEntrada):
	codigo_op = NODO_ENTRADA_CADENA
	titulo_op = "Cadena"

	ClasedelContenidodeNodo = ContenidodelNodoCadena

	Entradas = []
	Salidas = [4]

	FormaDeEntradas = []
	FormaDeSalidas = ['Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)